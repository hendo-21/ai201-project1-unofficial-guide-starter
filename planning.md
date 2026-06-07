# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
Undergrad housing experiences at Boston University. Boston University’s campus is highly urbanized, stretching horizontally across a two-mile corridor along Commonwealth Avenue and spanning several distinct Boston neighborhoods. As a result of the housing diversity, and quality of on-campus housing, many students opt to stay within student housing for their entire four years. Official BU housing materials provide basic amenity checklists and emphasize proximity to academic landmarks, but they sanitize the day-to-day realities of campus living. Location, the diversity of housing types, neighborhood logistics, and non-University supported community amenities dictate a student’s daily routine just as much as the room itself. Finding the right student housing requires careful review of community forums and unofficial wikis.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit | Housing Advice | https://www.reddit.com/r/BostonU/comments/1t8s6yp/my_rankingadvice_for_freshman_housing/ |
| 2 | Reddit | Housing Ranking | https://www.reddit.com/r/BostonU/comments/1r1zs2n/bu_housing_ranking/ |
| 3 | Reddit | Best/worst dorms | https://www.reddit.com/r/BostonU/comments/sq6o3e/bestworst_dorms/ |
| 4 | Reddit | Best Freshman Dorms | https://www.reddit.com/r/BostonU/comments/1qgtrjm/best_freshman_dorms/ |
| 5 | Reddit | Upper classman housing reccs | https://www.reddit.com/r/BostonU/comments/vlegas/best_and_worst_dormssuites_to_live_in_as_a/ |
| 6 | Reddit | South campus reccs | https://www.reddit.com/r/BostonU/comments/axn40w/which_bay_statesouth_campus_dorms_should_i_aim/ |
| 7 | RateMyDorm | Dorm-specifc reviews | https://www.ratemydorm.com/dorms/boston-university |
| 8 | Reddit | Fenway Guide| https://www.reddit.com/r/BostonU/comments/1r37ax7/fenway_living_experience_as_a_freshman/ |
| 9 | Reddit | East, West, Central Comp | https://www.reddit.com/r/BostonU/comments/1jkkcxl/deciding_between_warren_fenway_and_the_towers/ |
| 10 | GuidetoBU Wiki| Detailed Community Housing Summaries by Dorm | https://guidetobu.com/housing/ |
| 11 | GuidetoBU Wiki | Dorm Power rankings | https://guidetobu.com/housing/bu-housing/ |
| 12 | GuidetoBU Wiki | Apartment Style Living | https://guidetobu.com/housing/bu-apartment-style-housing/ |
| 13 | GuidetoBU Wiki| Restaurants Near Campus | https://guidetobu.com/food/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
