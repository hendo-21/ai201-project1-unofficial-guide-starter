"""clean.py — Stage 1 (INGEST): turn raw HTML into clean, structured text.

Each reddit_*.html file in documents/ is one thread page saved from
old.reddit.com. clean_reddit() throws away the page boilerplate (sidebar,
footer, scripts, styles) and keeps only what we want to embed later:

  - the thread title  (the chunk stage prepends this to every chunk)
  - the original post  (OP)
  - every comment, with how deeply it is nested as a reply

For the OP and each comment we also keep three pieces of metadata as plain
text — date, score, and depth — so they travel with the chunk and stay
searchable instead of being thrown away with the tags.

Run `python clean.py` to clean every reddit_*.html in documents/ and write a
matching .txt file into documents/cleaned/.
"""

from pathlib import Path

from bs4 import BeautifulSoup

# old.reddit marks deleted/removed comments with this body text. We skip them.
DELETED = {"[deleted]", "[removed]"}


def _date(tag):
    """Return the YYYY-MM-DD part of the first <time datetime=...> inside tag.

    A datetime looks like "2026-05-10T00:46:37+00:00"; we keep the date only.
    Returns "" if there is no timestamp.
    """
    if tag is None:
        return ""
    time = tag.select_one("time[datetime]")
    if time is None:
        return ""
    return time["datetime"][:10]


def _body(md):
    """Return the text of a markdown body block as a single clean line.

    `md` is a <div class="md"> element (the comment/post text). We pull out
    all the text and normalize every whitespace run (spaces, tabs, and the
    newlines between Reddit's paragraphs) down to a single space, so the
    whole body is one tidy line. Returns "" if md is empty or missing.
    """
    if md is None:
        return ""
    # Drop images so they don't leave stray text in the body. old.reddit
    # renders an inline image as a link whose visible text is literally
    # "<image>", so we remove those anchors as well as any real <img> tags.
    for img in md.find_all(["img", "image"]):
        img.decompose()
    for a in md.find_all("a"):
        if a.get_text(strip=True) == "<image>":
            a.decompose()
    # str.split() with no args splits on any whitespace run; joining with a
    # single space collapses all of it.
    return " ".join(md.get_text(" ").split())


def clean_reddit(html: str) -> str:
    """Clean one old.reddit thread page into structured text.

    Output looks like:

        THREAD: Best/worst dorms : BostonU

        [OP | date=2026-05-10 | score=20 | depth=0]
        ...post text...

        [REPLY | date=2026-05-10 | score=3 | depth=0]
        ...comment text...

        [REPLY | date=2026-05-10 | score=None | depth=1]
        ...nested comment text...
    """
    soup = BeautifulSoup(html, "lxml")

    # 1. Strip boilerplate BEFORE extracting, so it can't leak into our text.
    for junk in soup.select("div.side, div.footer"):
        junk.decompose()
    for junk in soup(["script", "style"]):
        junk.decompose()

    blocks = []

    # 2. Thread title comes from <head><title>.
    title = soup.title.get_text(strip=True) if soup.title else ""
    blocks.append(f"THREAD: {title}")

    # 3. The original post (OP) is the one "link" thing on the page.
    op = soup.select_one("div.thing.link")
    if op is not None:
        date = _date(op.select_one("p.tagline"))
        score = op.get("data-score", "None")
        body = _body(op.select_one("div.expando div.usertext-body div.md"))
        blocks.append(f"[OP | date={date} | score={score} | depth=0]\n{body}")

    # 4. Comments, in the order they appear on the page.
    comment_area = soup.select_one("div.commentarea")
    entries = comment_area.select("div.entry.unvoted") if comment_area else []
    for entry in entries:
        body = _body(entry.select_one("div.usertext-body div.md"))
        if not body or body in DELETED:
            continue  # skip empty and deleted/removed comments

        tagline = entry.select_one("p.tagline")
        date = _date(tagline)

        # The real score lives on the "unvoted" span; its count is the title
        # attribute. Hidden-score comments have no such span -> "None".
        score_tag = tagline.select_one(".score.unvoted") if tagline else None
        score = score_tag["title"] if score_tag and score_tag.has_attr("title") else "None"

        # Depth = how many "child" wrappers this comment is nested inside.
        # A top-level comment has no div.child ancestor, so depth = 0.
        depth = len(entry.find_parents("div", class_="child"))

        blocks.append(f"[REPLY | date={date} | score={score} | depth={depth}]\n{body}")

    return "\n\n".join(blocks) + "\n"


def clean_rmd(html: str) -> str:
    """Clean one RateMyDorm page into structured text.

    TODO: implement once the RateMyDorm cleaning spec is provided.
    """
    raise NotImplementedError("clean_rmd() not implemented yet")


def clean_guide(html: str) -> str:
    """Clean one GuideToBU wiki page into structured text.

    TODO: implement once the GuideToBU cleaning spec is provided.
    """
    raise NotImplementedError("clean_guide() not implemented yet")


# Each source type has its own HTML layout, so it gets its own cleaner.
# The key is the filename prefix in documents/ (e.g. reddit_p1.html).
CLEANERS = {
    "reddit": clean_reddit,
    "rmd": clean_rmd,
    "guide": clean_guide,
}


def main():
    documents = Path("documents")
    output_dir = Path("documents/cleaned")
    output_dir.mkdir(exist_ok=True)

    for prefix, cleaner in CLEANERS.items():
        for html_path in sorted(documents.glob(f"{prefix}_*.html")):
            try:
                cleaned = cleaner(html_path.read_text(encoding="utf-8"))
            except NotImplementedError:
                print(f"{html_path.name} -> skipped ({prefix} cleaner not implemented yet)")
                continue
            out_path = output_dir / f"{html_path.stem}.txt"
            out_path.write_text(cleaned, encoding="utf-8")
            print(f"{html_path.name} -> {out_path}")


if __name__ == "__main__":
    main()
