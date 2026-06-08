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

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

Source: RateMyDorm
Sentence-aware splitting, capped at 150-175 words per chunk. Reviews are atomic and pertain to a specific dormitory, so a single review will rarely exceed this cap. Where a review does exceed it, the splitter completes the current sentence before starting a new chunk, preserving the integrity of each thought. A dorm name, date, and room type are prepended to each chunk before embedding. Reviews are grouped by dorm name in the source document.

Source: GuideToBu Wiki
1 section per chunk, using sentence-aware splitting with a 150-175 word cap enforced greedily within each section. Wiki pages are divided cleanly into subsections containing focused prose on the section subject. The splitter packs sentences into a chunk until the next sentence would exceed the cap, then starts a new chunk. A heading path for page, section, subsection is prepended to each chunk before embedding.

Source: Reddit
Sentence-aware splitting, capped at 150-175 words per chunk, minimum 100 characters. While most comments fall within the cap naturally, longer comments, particularly structured replies covering multiple dorms, can exceed it. The splitter completes the current sentence before starting a new chunk, ensuring no opinion is cut mid-thought. The thread title, date, and score is prepended to every chunk before embedding, since comments do not carry their own topic signal. The minimum character count guards against short replies that contain no meaningful content such as "agreed" or "this."


**Overlap:**

Source: RateMyDorm
None required between chunks. Sentence-aware splitting ensures no chunk ends mid-thought, so overlap is not needed to preserve meaning across boundaries.

Source: GuideToBu Wiki
None required between chunks. As with RateMyDorm, sentence-aware splitting guarantees clean boundaries. Section headers serve as the top-level boundary and are never split across chunks.

Source: Reddit
None required between chunks. Sentence-aware splitting ensures clean boundaries. The thread title prepended to every chunk preserves topic context across splits of the same comment.

**Reasoning:**

A hybrid approach is warranted because the three source types differ fundamentally in structure, authorial voice, and information density. A single chunk size would either fragment review content or under-split narrative prose. Sentence-aware splitting is applied uniformly across all three sources. The primary motivation is the 256 token limit of all-MiniLM-L6-v2, which silently truncates input beyond that threshold. A 150-175 word cap per chunk provides headroom for prepended metadata prefixes while staying within the model's limit. Splitting on sentence boundaries rather than raw character or word counts ensures no chunk ends mid-thought, preserving the integrity of each opinion or prose passage. Context like dorm name, star rating, heading path, or thread title must travel with the chunk as text to be semantically retrievable, not just filterable. Where a comment, review, or wiki section is split into multiple chunks, the prepended metadata prefix on each chunk preserves the topic context that a mid-content split would otherwise orphan. This makes the metadata prefix load-bearing for split chunks, not merely a convenience for single-chunk documents.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model: `all-MiniLM-L6-v2`**

A lightweight sentence-transformers model that runs locally with no API key or rate limits. It maps text to 384-dimensional vectors, with good performance on short to medium passages. Tradeoffs accepted: 
- Lower accuracy than larger models (e.g., OpenAI's `text-embedding-3-large`), but no cost and no latency from network calls.
- Compressed representation of meaning, but narrow domain means core content meaning should be preserved.

**Top-k: 8**

Given the diversity of document sources, it may be worth expanding to 8-10 if source diversity is limited.

**Production tradeoff reflection:**

- Embedding quality: a larger model would likely handle semantic nuances of a review to review closely related but ultimately distinct embeddings.
- Multilingual support: BU has a huge number of international students. Injesting feedback on student housing in different languages would add to the diversity of perspectives to the corpus.
- Domain expertise: a model tuned to have a greater understanding of BU housing slang and abbreviations would make more useful embeddings.
- Context length: I would consider opting for a model with a larger context window if I implemented conversation history. This could be a usefule feature as a student could reasonably wish to describe their needs and priorities and query the tool with that context maintained. This could get large as each retrieved chunk is included with the conversation history at each turn. I would also consider expanding top-k to ensure source diversity, which could fill up the context window pre-prompt.
- Re-ranking: For more accurate results, retrieve a higher top-k and then rerank results and only pass top 5 ranked results to the LLM.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | How big are the beds in Warren Towers? | Twin XL bed (80 inches -- bring extra-long twin sheets) |
| 2 | What are the room options for Stuvi2? | Stuvi2 offers single, double, and triple room configurations. |
| 3 | What do students say about living in West campus and taking classes at CAS? | Students consistently say that the walk from West campus for classes in CAS is long and crowded. |
| 4 | What's the guest policy at Stuvi2?  | The system should acknowledge that it doesn't have the information, as it's an official policy not present in these community docs. |
| 5 | What's the standout feature of living at Fenway? | Students consistently praise the quality of the dining hall, despite the distance to west campus. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Given the breadth of BU housing, many dorms share the same street name, but with a different number address. Students often have their own names for these residences, so comments talking about the same place might not register as related.

2. Reddit and RateMyDorm will likely dominate the number of chunks in the database. This might result in top k not surfacing relevant information from the GuideToBU Wiki as it more frequently pulls from the other two sources. Users might miss out on the valuable content offered by the GuideToBU Wiki.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```
User query
    │
    ▼
[1] INGEST          ──► Extract html from sources, clean html tags to produce txt file.
    extract.py
    clean.py
    │
    ▼
[2] CHUNK          ──► Sentance-aware splitting per source type.
    chunk.py           Metadata prepended to each chunk before embedding.
    │
    ▼
[3] EMBED + STORE   ──► Embed chunks into vector store.
    embed.py            Embedding model: `all-MiniLM-L6-v2` | Vector Store: `ChromaDB`
    │
    ▼

[4] RETRIEVE        ──► Query is embedded and matched against stored chunks
    retriever.py        Embedding model: `all-MiniLM-L6-v2` | Vector Store: `ChromaDB`
    │
    ▼
[5] GENERATE        ──► Retrieved chunks are passed as context to an LLM, which produces a grounded, cited answer
    generator.py        LLM: Groq `llama-3.3-70b-versatile`
    │
    ▼
[6] UI              ──► Gradio chat interface serves the response to the user
    app.py
```

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

I'll give Claude my set of source documents saved as raw HTML, the architecture section, and `cleaning_spec.md`. I'll ask it to implement `clean_reddit()` and `clean_rmd()` to remove boilerplate, extract metadata, and translate tags to structural text markers. I will manually inspect the cleaned output for each source type against the raw HTML to verify that boilerplate has been removed, structural markers are preserved, and metadata fields like ratings and heading paths have been correctly extracted.

I'll give Claude my chunking strategy section, the normalized chunk dict schema, and an example of cleaned output from each source type. I'll give Claude my chunking strategy section and ask it to implement `chunk_reddit()`, `chunk_rmd()`, and `chunk_guide()` with my specified source-specific sentance-splitting strategy, minimum character count, and maximum word counts. I'll manually inspect 5 chunks per source type to verify the metadata prefix is correctly prepended, dorm names are normalized, and no boilerplate text survived cleaning.

**Milestone 4 — Embedding and retrieval:**

I'll give Claude my chunk functions, the normalized dict schema, and the architecture section. I'll ask it to implement `embed_and_store()` to embed each chunk's text field using all-MiniLM-L6-v2 and store the resulting vector alongside the chunk metadata in ChromaDB. I'll verify by checking ChromaDB's stored count matches my total chunk count, and spot-checking that stored metadata fields match the source chunks.

I'll give Claude my embed_and_store() implementation and the architecture section. I'll ask it to implement `retrieve()` to encode the user query using the same embedding model, query ChromaDB for the top k most similar chunks, and return results including chunk text, metadata, and distance scores. 

I'll give Claude my `retrieve()` function and the normalized dict schema. I'll ask it to write 5-10 unit tests covering distance score ranges, chunk content validity, metadata field presence and accuracy, and correct behavior when the collection is empty.

**Milestone 5 — Generation and interface:**

I'll give Claude my `retrieve()` implementation, the architecture section, and my Groq API credentials. I'll ask it to implement `generate()` that takes the user query and retrieved chunks, constructs a prompt instructing the LLM to answer using only the provided context, cite sources and call the Groq API.

I'll give Claude my `generate()` function and ask it to implement a Gradio interface displays the user query, generated answer, and source citations for each response. I'll verify by running the UI locally and confirming citations render correctly and responses are grounded in retrieved content.
