"""chunk.py — Stage 2 (CHUNK): turn cleaned text into embedding-ready chunks.

clean.py writes one structured .txt file per source into documents/cleaned/.
Each file opens with a `# Source URL: ...` line and then a series of blocks:

  - RateMyDorm: one [REVIEW | dorm=... | date=... | room_type=...] block per review.
  - Reddit:     one [OP|REPLY | thread=... | date=... | score=... | depth=...] block
                per post/comment.
  - GuideToBU:  one `## Page > Section` heading per wiki subsection, followed by prose.

This stage splits those blocks into chunks ready for embedding. Per the
Chunking Strategy in planning.md, all three sources use sentence-aware packing
capped at MAX_WORDS words per chunk: sentences are packed greedily into a chunk
until the next sentence would exceed the cap, then a new chunk starts. Sentences
are never split mid-thought, so no overlap is needed. The 256-token limit of
all-MiniLM-L6-v2 is the binding constraint; the word cap leaves headroom for the
metadata prefix that is prepended to every chunk's text so context (dorm, date,
thread title, heading path) is semantically retrievable, not merely filterable.

  - chunk_rmd()    -> ratemydorm chunks
  - chunk_reddit() -> reddit chunks
  - chunk_guide()  -> guidetobu chunks

Run `python chunk.py` to chunk every file in documents/cleaned/ and write the
combined list to documents/chunks.json.
"""

import json
import re
from pathlib import Path

# Sentence-aware packing cap. 150-175 words sits comfortably under the 256-token
# limit of all-MiniLM-L6-v2 while leaving room for the metadata prefix.
MAX_WORDS = 175

# Reddit-only: drop chunks shorter than this. Guards against low-signal replies
# ("agreed", "this") that carry no retrievable content. Applies to the chunk
# body, before the metadata prefix is added.
REDDIT_MIN_CHARS = 100

# GuideToBU pages carry no per-page date, so we stamp a constant. This matches
# the normalized schema and keeps the date field present for every source.
GUIDE_DATE = "2025-01-01"

# A sentence boundary: end punctuation followed by whitespace. Imperfect on
# informal Reddit prose, but a too-long "sentence" simply becomes its own chunk
# rather than being cut mid-thought.
_SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+")


def _source_url(text: str) -> str | None:
    """Return the URL from the leading `# Source URL: ...` line, or None."""
    match = re.search(r"#\s*Source URL:\s*(\S+)", text)
    return match.group(1) if match else None


def _parse_tag(line: str) -> tuple[str, dict]:
    """Parse a block header like `[REVIEW | dorm=Warren Towers | date=2025-01-01]`.

    Returns the block kind ("REVIEW", "OP", "REPLY") and a dict of the
    pipe-separated key=value metadata fields.
    """
    inner = line.strip().lstrip("[").rstrip("]")
    parts = [p.strip() for p in inner.split("|")]
    kind = parts[0] if parts else ""
    meta = {}
    for part in parts[1:]:
        if "=" in part:
            key, value = part.split("=", 1)
            meta[key.strip()] = value.strip()
    return kind, meta


def _tagged_blocks(text: str):
    """Yield (kind, meta, body) for each `[...]`-tagged block in the text.

    Blocks are separated by blank lines; the body is everything after the
    header line, collapsed to a single line. clean.py already emits each body
    as one line, so this is a no-op for normal input but stays robust if not.
    """
    for raw in re.split(r"\n\s*\n", text):
        raw = raw.strip()
        if not raw.startswith("["):
            continue  # skip the `# Source URL:` header and any stray text
        lines = raw.split("\n")
        kind, meta = _parse_tag(lines[0])
        body = " ".join(line.strip() for line in lines[1:] if line.strip())
        yield kind, meta, body


def _split_sentences(text: str) -> list[str]:
    """Split text into sentence-ish units, treating newlines as hard breaks.

    Newlines are real boundaries in GuideToBU prose and table rows; for the
    single-line RateMyDorm/Reddit bodies they have no effect.
    """
    sentences = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        for sentence in _SENTENCE_BOUNDARY.split(line):
            sentence = sentence.strip()
            if sentence:
                sentences.append(sentence)
    return sentences


def _pack(text: str, cap: int = MAX_WORDS) -> list[str]:
    """Greedily pack sentences into chunks of at most `cap` words.

    A sentence is added to the current chunk unless doing so would push it over
    the cap, in which case the current chunk is flushed and the sentence starts
    a new one. A single sentence longer than `cap` becomes its own chunk rather
    than being split mid-thought.
    """
    chunks = []
    current = []
    count = 0
    for sentence in _split_sentences(text):
        words = len(sentence.split())
        if current and count + words > cap:
            chunks.append(" ".join(current))
            current = [sentence]
            count = words
        else:
            current.append(sentence)
            count += words
    if current:
        chunks.append(" ".join(current))
    return chunks


def _score_to_int(value: str | None):
    """Convert a Reddit score string to int, or None for hidden scores."""
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def chunk_rmd(text: str, source_url: str | None = None, start_index: int = 0) -> list[dict]:
    """Chunk one cleaned RateMyDorm document.

    Each review is packed independently (reviews are atomic and rarely exceed
    the cap). The dorm, date, and room type travel with every chunk as a text
    prefix. `start_index` lets the driver keep chunk_ids unique across the many
    RateMyDorm files that share the "ratemydorm" prefix.
    """
    if source_url is None:
        source_url = _source_url(text)

    chunks = []
    counter = start_index
    for _kind, meta, body in _tagged_blocks(text):
        dorm = meta.get("dorm", "unknown")
        date = meta.get("date", "")
        room_type = meta.get("room_type", "unknown")
        for piece in _pack(body):
            prefix = f"[RateMyDorm | Dorm: {dorm} | Date: {date} | Room: {room_type}]"
            chunks.append({
                "text": f"{prefix}\n{piece}",
                "chunk_id": f"ratemydorm_{counter}",
                "source_type": "ratemydorm",
                "source_url": source_url,
                "dorm": dorm,
                "date": date,
                "room_type": room_type,
                "rating": None,
            })
            counter += 1
    return chunks


def chunk_reddit(text: str, source_url: str | None = None, start_index: int = 0) -> list[dict]:
    """Chunk one cleaned Reddit thread document.

    Comments and the OP are packed independently. The thread title, date, and
    score travel with every chunk as a text prefix, since a comment carries no
    topic signal of its own. Chunks shorter than REDDIT_MIN_CHARS are dropped as
    low-signal. `start_index` keeps chunk_ids unique across all Reddit files.
    """
    if source_url is None:
        source_url = _source_url(text)

    chunks = []
    counter = start_index
    for _kind, meta, body in _tagged_blocks(text):
        thread_title = meta.get("thread", "")
        date = meta.get("date", "")
        score = _score_to_int(meta.get("score"))
        for piece in _pack(body):
            if len(piece) < REDDIT_MIN_CHARS:
                continue
            prefix = f"[Reddit | Thread: {thread_title} | Date: {date} | Score: {score}]"
            chunks.append({
                "text": f"{prefix}\n{piece}",
                "chunk_id": f"reddit_{counter}",
                "source_type": "reddit",
                "source_url": source_url,
                "dorm": None,
                "date": date,
                "thread_title": thread_title,
                "comment_score": score,
            })
            counter += 1
    return chunks


def chunk_guide(text: str, source_url: str | None = None, start_index: int = 0) -> list[dict]:
    """Chunk one cleaned GuideToBU wiki document.

    Each `## Page > Section` subsection is packed independently — section
    headers are the top-level boundary and are never split across chunks. The
    full heading path travels with every chunk as a text prefix. The dorm is
    normalized to the page name from the first heading so every chunk in a file
    shares one consistent dorm, even where a section heading varies in casing.
    `start_index` keeps chunk_ids unique across all GuideToBU files.
    """
    if source_url is None:
        source_url = _source_url(text)

    # Collect (heading_path, body) per subsection by scanning for `## ` headings.
    sections: list[tuple[str, str]] = []
    heading = None
    body_lines: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if heading is not None:
                sections.append((heading, "\n".join(body_lines)))
            heading = line[3:].strip()
            body_lines = []
        elif heading is not None:
            body_lines.append(line)
    if heading is not None:
        sections.append((heading, "\n".join(body_lines)))

    # Normalize dorm to the page name (text before the first " > ") of the first
    # section, so chunks in a file share one dorm value despite heading typos.
    page_dorm = sections[0][0].split(" > ")[0].strip() if sections else "unknown"

    chunks = []
    counter = start_index
    for heading_path, body in sections:
        for piece in _pack(body):
            prefix = f"[GuidetoBU | {heading_path}]"
            chunks.append({
                "text": f"{prefix}\n{piece}",
                "chunk_id": f"guidetobu_{counter}",
                "source_type": "guidetobu",
                "source_url": source_url,
                "dorm": page_dorm,
                "date": GUIDE_DATE,
                "heading_path": heading_path,
            })
            counter += 1
    return chunks


# Filename prefix in documents/cleaned/ -> (chunker, chunk_id source key).
CHUNKERS = {
    "reddit": (chunk_reddit, "reddit"),
    "rmd": (chunk_rmd, "ratemydorm"),
    "guidetobu": (chunk_guide, "guidetobu"),
}


def main():
    cleaned_dir = Path("documents/cleaned")
    out_path = Path("documents/chunks.json")

    all_chunks = []
    # Thread a per-source counter across files so chunk_ids stay globally unique.
    counters = {key: 0 for _, key in CHUNKERS.values()}

    for prefix, (chunker, key) in CHUNKERS.items():
        for txt_path in sorted(cleaned_dir.glob(f"{prefix}_*.txt")):
            text = txt_path.read_text(encoding="utf-8")
            chunks = chunker(text, start_index=counters[key])
            counters[key] += len(chunks)
            all_chunks.extend(chunks)
            print(f"{txt_path.name} -> {len(chunks)} chunk(s)")

    out_path.write_text(json.dumps(all_chunks, indent=2, ensure_ascii=False), encoding="utf-8")
    counts = ", ".join(f"{key}={n}" for key, n in counters.items())
    print(f"\nWrote {len(all_chunks)} chunk(s) to {out_path} ({counts})")


if __name__ == "__main__":
    main()
