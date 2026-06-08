"""clean.py — Stage 1 (INGEST): turn raw HTML into clean, structured text.

Raw HTML pages live in documents/html-backups/, one per source. Each source
type has its own cleaner that throws away page boilerplate (sidebars, footer,
scripts, styles) and keeps only what we want to embed later, as plain-text
blocks with the key metadata kept inline so it travels with the chunk:

  - clean_reddit() — old.reddit threads: the OP and every comment, with the
    thread title, date, score, and reply depth.
  - clean_rmd()    — RateMyDorm pages: one block per review, with the dorm
    name, date, and room type.
  - clean_guide()  — GuideToBU wiki pages (TODO).

Run `python clean.py` to clean every supported *.html in documents/html-backups/
and write a matching .txt file into documents/cleaned/.
"""

import re
from datetime import datetime, timedelta
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

    The thread title rides along in every block (thread=...) so each block is
    self-contained for the chunk stage. Output looks like:

        [OP | thread=Best/worst dorms : BostonU | date=2026-05-10 | score=20]
        ...post text...

        [REPLY | thread=Best/worst dorms : BostonU | date=2026-05-10 | score=3 | depth=0]
        ...comment text...

        [REPLY | thread=Best/worst dorms : BostonU | date=2026-05-10 | score=None | depth=1]
        ...nested comment text...
    """
    soup = BeautifulSoup(html, "lxml")

    # 1. Strip boilerplate BEFORE extracting, so it can't leak into our text.
    for junk in soup.select("div.side, div.footer"):
        junk.decompose()
    for junk in soup(["script", "style"]):
        junk.decompose()

    blocks = []

    # 2. Thread title comes from <head><title>. It is prepended to every block.
    title = soup.title.get_text(strip=True) if soup.title else ""

    # 3. The original post (OP) is the one "link" thing on the page.
    op = soup.select_one("div.thing.link")
    if op is not None:
        date = _date(op.select_one("p.tagline"))
        score = op.get("data-score", "None")
        body = _body(op.select_one("div.expando div.usertext-body div.md"))
        blocks.append(f"[OP | thread={title} | date={date} | score={score}]\n{body}")

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

        blocks.append(
            f"[REPLY | thread={title} | date={date} | score={score} | depth={depth}]\n{body}"
        )

    return "\n\n".join(blocks) + "\n"


def _relative_to_date(text):
    """Turn a relative time like "3 months ago" into an approximate YYYY-MM-DD.

    RateMyDorm only tells us how long ago a review was posted, so we count back
    from today's date. This is deliberately rough: per the spec, any
    "N years ago" collapses to January 1st of that year, and months land on the
    1st of the resolved month.
    """
    now = datetime.now()
    match = re.search(r"(\d+|a|an)\s+(second|minute|hour|day|week|month|year)", text.lower())
    if not match:
        return now.strftime("%Y-%m-%d")  # "just now", "today", or unrecognized

    n = 1 if match.group(1) in ("a", "an") else int(match.group(1))
    unit = match.group(2)
    if unit == "year":
        return f"{now.year - n:04d}-01-01"
    if unit == "month":
        months = (now.year * 12 + now.month - 1) - n  # count months from year 0
        return f"{months // 12:04d}-{months % 12 + 1:02d}-01"
    days = {"second": 0, "minute": 0, "hour": 0, "day": 1, "week": 7}[unit] * n
    return (now - timedelta(days=days)).strftime("%Y-%m-%d")


def _room_type(card):
    """Extract the room type from a review card, e.g. "double" or "single".

    The text reads "Lived in a double"; we drop the "Lived in a " prefix and
    keep the rest as-is. Returns "unknown" if the field is blank or missing.
    """
    div = card.select_one("div.font-medium.text-gray-600")
    text = " ".join(div.get_text(" ").split()) if div else ""
    prefix = "Lived in a "
    if text.startswith(prefix):
        return text[len(prefix):].strip() or "unknown"
    return "unknown"


def clean_rmd(html: str) -> str:
    """Clean one RateMyDorm page into structured text.

    Output is one block per review:

        [REVIEW | dorm=Warren Towers | date=2025-08-01 | room_type=double]
        ...review text...
    """
    soup = BeautifulSoup(html, "lxml")

    # 1. Strip boilerplate BEFORE extracting. The two sidebars use Tailwind
    #    classes containing ":" and "/", so we match each by a distinctive
    #    class fragment: "xl:hidden" (mobile) and "xl:order-2" (desktop).
    for junk in soup(["nav", "footer", "script", "style"]):
        junk.decompose()
    for junk in soup.select('div[class*="xl:hidden"], div[class*="xl:order-2"]'):
        junk.decompose()

    # 2. Dorm name from the page heading, e.g. "Warren Towers Reviews".
    h1 = soup.select_one('h1[itemtype="https://schema.org/Residence"]')
    dorm = re.sub(r"\s*Reviews$", "", " ".join(h1.get_text(" ").split())) if h1 else "unknown"

    # 3. One block per review. Each review sits in its own <section> alongside
    #    its timestamp and room type, so we read those from the same section.
    blocks = []
    for review in soup.select('p[itemtype="https://schema.org/Review"]'):
        body = _body(review)
        if not body:
            continue  # skip blank reviews
        card = review.find_parent("section")
        timestamp = card.select_one("p.block.text-gray-600.text-sm.font-medium") if card else None
        date = _relative_to_date(timestamp.get_text(strip=True)) if timestamp else ""
        room_type = _room_type(card) if card else "unknown"
        blocks.append(f"[REVIEW | dorm={dorm} | date={date} | room_type={room_type}]\n{body}")

    return "\n\n".join(blocks) + "\n"


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
    input_dir = Path("documents/html-backups")
    output_dir = Path("documents/cleaned")
    output_dir.mkdir(exist_ok=True)

    for prefix, cleaner in CLEANERS.items():
        for html_path in sorted(input_dir.glob(f"{prefix}_*.html")):
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
