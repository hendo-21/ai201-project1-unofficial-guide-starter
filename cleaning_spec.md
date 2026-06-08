## Reddit

**OP:**

Thread title:
<head>
    <title> ← extract text content

Timestamp:
<p class="top-matter">
<p class="tagline">
    <time datetime="2026-02-11T16:23:11+00:00">  ← extract datetime attribute - YYYY-MM-DD only

Score:
<div class="thing link" data-score="6">  ← extract data-score attribute
    (the OP is the one "link" thing on the page; data-score sits on it
     directly, NOT inside <div class="midcol unvoted">)

Text:
<div class="expando">
    <div class="usertext-body">
        <div class="md"> ← target this, not the sidebar md
            <p> ← there are multiple paragraph tags; include all of them.

Depth:
<div class="entry unvoted"> indicates OP content.

**Replies:**

Timestamp:
<p class="tagline">
    <time datetime="2026-02-11T16:23:11+00:00">  ← extract datetime attribute - YYYY-MM-DD only

Score:
<p class="tagline">
    <span class="score unvoted" title="5">  ← extract the title attribute
    (it's a <span>, not a <div>; the count is in title, not data-score.
     A score-hidden comment has no .score.unvoted span -> record score as "None")

Text:
<div class="commentarea">
    <div class="usertext-body">
        <div class="md">  ← target this, not the sidebar md
            <p>  ← extract text content

Depth:
<div class="entry unvoted"> indicate reply content.
Comments nested inside <div class="child"> indicate reply depth.
Top-level comments have no <div class="child"> ancestor.

Strip before extracting:
<div class="side">      ← subreddit sidebar
<div class="footer">    ← page footer
<script> and <style>    ← all script and style tags

Strip after extracting text:
- <image> tags  ← old.reddit renders an inline image as an <a> link whose
  visible text is the literal string "<image>"; drop those anchors (and any
  real <img> tags) so the placeholder doesn't end up in the body text.

Skip these comments entirely (do not emit a block):
- deleted/removed comments: <div class="md"> body text is "[deleted]" or "[removed]"
- comments with no paragraph text after cleaning

**Output format:**
One block per comment:
[OP | thread={thread_title} | date={YYYY-MM-DD} | score={score}]
{post_text}

[REPLY | thread={thread_title} | date={YYYY-MM-DD} | score={score} | depth={depth}]
{comment_text}


## RateMyDorm

Dorm name:
<h1 itemtype="https://schema.org/Residence"> ← extract text, strip trailing " Reviews"

Timestamp:
<p class="block text-gray-600 text-sm font-medium"> ← relative string e.g. "3 months ago"
Convert to YYYY-MM-DD using datetime.now() at script execution time.
Approximate only — "3 years ago" resolves to YYYY-01-01.

Review:
<p itemtype="https://schema.org/Review"> ← extract text content

Room type:
<div class="font-medium text-gray-600"> ← text following "Lived in a"
Store as-is (e.g. "double", "single", "quad"). Use "unknown" if absent.

Strip before extracting:
<nav>                   ← site navigation
<footer>                ← page footer
<script> and <style>    ← all script and style tags
<div class="xl:order-2 xl:ml-8 xl:w-2/4 space-y-8 2xl:w-5/12">  ← desktop sidebar
<div class="xl:hidden"> ← mobile sidebar (duplicate of desktop sidebar)

**Output format:**
One block per review:
[REVIEW | dorm={dorm_name} | date={YYYY-MM-DD} | room_type={room_type}]

## GuideToBU