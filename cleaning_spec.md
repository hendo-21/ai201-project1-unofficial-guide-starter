## Reddit

Extract OP content and every reply.

<div class="usertext-body may-blank-within md-container " ><div class="md">

**OP:**

Thread title:
<head>
    <title> ← extract text content

Timestamp:
<p class="top-matter">
<p class="tagline">
    <time datetime="2026-02-11T16:23:11+00:00">  ← extract datetime attribute - YYYY-MM-DD only

Score:
<div class="midcol unvoted">
    <div class="thing" data-score="6">  ← extract data-score attribute

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
    <div class="thing" data-score="6">  ← extract data-score attribute

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