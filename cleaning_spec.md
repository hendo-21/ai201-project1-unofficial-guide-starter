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