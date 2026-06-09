# The Unofficial Guide — Project 1

---

## Domain

Undergrad housing experiences at Boston University. Boston University’s campus is highly urbanized, stretching horizontally across a two-mile corridor along Commonwealth Avenue and spanning several distinct Boston neighborhoods. As a result of the housing diversity, and quality of on-campus housing, many students opt to stay within student housing for their entire four years. Official BU housing materials provide basic amenity checklists and emphasize proximity to academic landmarks, but they sanitize the day-to-day realities of campus living. Location, the diversity of housing types, neighborhood logistics, and non-University supported community amenities dictate a student’s daily routine just as much as the room itself. Finding the right student housing requires careful review of community forums and unofficial wikis.

---

## Document Sources

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit | Housing Advice | https://www.reddit.com/r/BostonU/comments/1t8s6yp/my_rankingadvice_for_freshman_housing/ |
| 2 | Reddit | Housing Ranking | https://www.reddit.com/r/BostonU/comments/1r1zs2n/bu_housing_ranking/ |
| 3 | Reddit | Best/worst dorms | https://www.reddit.com/r/BostonU/comments/sq6o3e/bestworst_dorms/ |
| 4 | Reddit | Best Freshman Dorms | https://www.reddit.com/r/BostonU/comments/1qgtrjm/best_freshman_dorms/ |
| 5 | Reddit | Upper classman housing reccs | https://www.reddit.com/r/BostonU/comments/vlegas/best_and_worst_dormssuites_to_live_in_as_a/ |
| 6 | Reddit | South campus reccs | https://www.reddit.com/r/BostonU/comments/axn40w/which_bay_statesouth_campus_dorms_should_i_aim/ |
| 7 | Reddit | Fenway Guide| https://www.reddit.com/r/BostonU/comments/1r37ax7/fenway_living_experience_as_a_freshman/ |
| 8 | Reddit | East, West, Central Comp | https://www.reddit.com/r/BostonU/comments/1jkkcxl/deciding_between_warren_fenway_and_the_towers/ |
| 9 | RateMyDorm | Warren Towers student reviews | https://www.ratemydorm.com/reviews/boston-university/boston-university-warre |
| 10 | RateMyDorm | Buick St student reviews | https://www.ratemydorm.com/reviews/boston-university/boston-university-10-buick-street |
| 11 | RateMyDorm | The Towers student reviews | https://www.ratemydorm.com/reviews/boston-university/boston-university-the-towers |
| 12 | RateMyDorm | 33 Harry Aganis student reviews | https://www.ratemydorm.com/reviews/boston-university/boston-university-33-harry-agganis-way |
| 13 | RateMyDorm | South Campus Apts student reviews | https://www.ratemydorm.com/reviews/boston-university/boston-university-south-campus-apartments |
| 14 | RateMyDorm | South Campus Brownstones student reviews | https://www.ratemydorm.com/reviews/boston-university/boston-university-south-campus-brownstones |
| 15 | RateMyDorm | Bay St student reviews | https://www.ratemydorm.com/reviews/boston-university/boston-university-bay-state-road-brownstones |
| 16 | RateMyDorm | Fenway student reviews | https://www.ratemydorm.com/reviews/boston-university/boston-university-fenway-campus-162-riverway |
| 17 | RateMyDorm | Myles-Standish student reviews | https://www.ratemydorm.com/reviews/boston-university/boston-university-myles-standish-hall |
| 18 | RateMyDorm | Kilachand Hall reviews | https://www.ratemydorm.com/reviews/boston-university/boston-university-kilachand-hall |
| 19 | RateMyDorm | 575 Comm Ave student reviews | https://www.ratemydorm.com/reviews/boston-university/boston-university-575-commonwealth-avenue |
| 20 | RateMyDorm | East Campus student reviews | https://www.ratemydorm.com/reviews/boston-university/boston-university-east-campus-apartments |
| 21 | RateMyDorm | Diensen Hall student reviews | https://www.ratemydorm.com/reviews/boston-university/boston-university-danielsen-hall |
| 22 | RateMyDorm | 1019 Comm Ave student reviews | https://www.ratemydorm.com/reviews/boston-university/boston-university-1019-commonwealth-avenue |
| 23 | GuidetoBU Wiki| Warren Towers Unofficial guide | https://guidetobu.com/housing/warren-towers/ |
| 24 | GuidetoBU Wiki| West Campus Unofficial guide | https://guidetobu.com/housing/west-campus-bu/ |
| 25 | GuidetoBU Wiki| Stuvi2 Unofficial guide | https://guidetobu.com/housing/stuvi2/ |
| 26 | GuidetoBU Wiki| Myles-Standish Unofficial guide | https://guidetobu.com/housing/myles-standish-hall/ |
| 27 | GuidetoBU Wiki| Danielsen Hall Unofficial guide | https://guidetobu.com/housing/danielsen-hall/ |
| 28 | GuidetoBU Wiki| Bay State Unofficial guide | https://guidetobu.com/housing/bay-state-road-bu/ |


---

## Chunking Strategy

**Chunk size:**

Source: RateMyDorm
Sentence-aware splitting, capped at 150-175 words per chunk. Reviews are atomic and pertain to a specific dormitory, so a single review will rarely exceed this cap. Where a review does exceed it, the splitter completes the current sentence before starting a new chunk, preserving the integrity of each thought. A dorm name, date, and room type are prepended to each chunk before embedding. Reviews are grouped by dorm name in the source document.

Source: GuideToBu Wiki
1 section per chunk, using sentence-aware splitting with a 150-175 word cap enforced greedily within each section. Wiki pages are divided cleanly into subsections containing focused prose on the section subject. The splitter packs sentences into a chunk until the next sentence would exceed the cap, then starts a new chunk. A heading path for page and section is prepended to each chunk before embedding.

Source: Reddit
Sentence-aware splitting, capped at 150-175 words per chunk, minimum 100 characters. While most comments fall within the cap naturally, longer comments, particularly structured replies covering multiple dorms, can exceed it. The splitter completes the current sentence before starting a new chunk, ensuring no opinion is cut mid-thought. The thread title, date, and score is prepended to every chunk before embedding, since comments do not carry their own topic signal. The minimum character count guards against short replies that contain no meaningful content such as "agreed" or "this."

**Overlap:**

Source: RateMyDorm
None required between chunks. Sentence-aware splitting ensures no chunk ends mid-thought, so overlap is not needed to preserve meaning across boundaries.

Source: GuideToBu Wiki
None required between chunks. As with RateMyDorm, sentence-aware splitting guarantees clean boundaries. Section headers serve as the top-level boundary and are never split across chunks.

Source: Reddit
None required between chunks. Sentence-aware splitting ensures clean boundaries. The thread title prepended to every chunk preserves topic context across splits of the same comment.

**Why these choices fit your documents:**

A hybrid approach is warranted because the three source types differ fundamentally in structure, voice, and information density. A single chunk size would either fragment review content or under-split narrative prose. Therefore, sentence-aware splitting is applied uniformly across all three sources, with some caveats. All source material is relatively short in length, even the Guide To BU Wiki pages, however there are outliers in each source set. The embedding model used, `all-MiniLM-L6-v2`, has a 256 token limit, which silently truncates input beyond that threshold. The 150-175 word cap per chunk guards against this and provides headroom for prepended metadata prefixes while staying within the model's limit. Splitting on sentence boundaries rather than raw character or word counts ensures no chunk ends mid-thought, preserving the integrity of each opinion or prose passage. Context like dorm name, heading path, and thread title travels with the chunk as text to add semantic depth (helpful for short Reddit comments/reviews on RateMyDorm). Where a comment, review, or wiki section is split into multiple chunks, the prepended metadata prefix on each chunk preserves the topic context that a mid-content split might otherwise orphan. This makes the metadata prefix load-bearing for split chunks.

**Preprocessing actions taken:**

I wrote a `cleaning_spec.md` to support in directing Claude Code to write two cleaning functions. These cleaning functions took raw HTML from Reddit and Rate My Dorm, constructed comment/review blocks, and placed them in `.txt` files by source url. In the spec, I identified the CSS selectors where the necessary text and metadata was located so that Claude could extract and format it as needed. The Guide To BU Wiki URLs were more copy-paste friendly, so those were processed by hand. Unfortunately, the stripping process used a lot of tokens given the size of the HTML files, so next time I would likely do some pre-processing of those documents before handing them of to Claude. 

**Example Chunks:**

```
Source: Reddit | https://www.reddit.com/r/BostonU/comments/1t8s6yp/my_rankingadvice_for_freshman_housing/
Chunk:
  {
    "also the closest T is kenmore which is a bit of a walk and its underground so you have to pay kilachand: great location right near marcis and central campus. i havent personally seen the dorms however im pretty sure they have ac and private bathrooms. and you dont have to be in the honors college to live there hojo: i havent seen a room however most are triples and doubles are hard to come by. personally im not the biggest fan of the vibes of hojo it feels like a creepy musty old hotel however it has a great location in central campus bay state road brownstones: each brownstone is different however from the ones ive seen they are oftentimes very spacious. its hard with housing as a freshman becaudse you dont know where on bay state you will be because it goes pretty far down. towers: solid option good location and is on baystate road so more peaceful and quiet than warren on comm ave.",

    "source_url": "https://www.reddit.com/r/BostonU/comments/1t8s6yp/my_rankingadvice_for_freshman_housing/",
  }

  Source: Reddit | https://www.reddit.com/r/BostonU/comments/1qgtrjm/best_freshman_dorms/
  Chunk:
  {
    "text": "but, i don't understand why these small town people think warren and west are trash. warren gave me the best first year oof my lives and in still friends with them today. these cringe kids have to stop acting they going to be thrown in Azkaba.",
    "chunk_id": "reddit_35",
    "source_type": "reddit",
    "source_url": "https://www.reddit.com/r/BostonU/comments/1qgtrjm/best_freshman_dorms/",
    "dorm": null,
    "date": "2026-01-19",
    "thread_title": "Best Freshman dorms? : BostonU",
    "comment_score": 10
  }

  Source: Rate My Dorm | https://www.ratemydorm.com/reviews/boston-university/boston-university-1019-commonwealth-avenue
  Chunk:
  {
    "text": "Definitely a good place to live sophomore year or even for underclassmen if you can get it. If you dont mind its one bathroom for average 6 people, 3 doubles in a suite so if you want a single you are out of luck with 1019. Overall pretty nice place but very far west so if you have classes say in Questrom thats rough.",
    "chunk_id": "ratemydorm_1",
    "source_type": "ratemydorm",
    "source_url": "https://www.ratemydorm.com/reviews/boston-university/boston-university-1019-commonwealth-avenue",
    "dorm": "1019 Commonwealth Avenue",
    "date": "2023-01-01",
    "room_type": "unknown",
    "rating": null
  }

  Source: Rate My Dorm | https://www.ratemydorm.com/reviews/boston-university/boston-university-bay-state-road-brownstones
  Chunk
  {
    "text": "Ours had two common areas, beautiful hardwood flooring in the room, laundry in the basement. A few problems, though: one tiny shared closet, shared bathroom (1 between 6 girls), construction starting right outside the window for the past two years now starting at 7am",
    "chunk_id": "ratemydorm_30",
    "source_type": "ratemydorm",
    "source_url": "https://www.ratemydorm.com/reviews/boston-university/boston-university-bay-state-road-brownstones",
    "dorm": "Bay State Road Brownstones",
    "date": "2021-01-01",
    "room_type": "double",
    "rating": null
  }

  Source: Guide To BU Wiki | https://guidetobu.com/housing/bay-state-road-bu/
  Chunk:
  {
    "text": "Living on Bay State Road comes with a host of convenient amenities and benefits that enhance the overall college experience: Proximity to Campus: With the BU central campus just a short walk away, Bay State residents have easy access to classrooms, dining halls, and other university resources. Green Spaces: The tree-lined streets and Charles River Esplanade provide ample opportunities for outdoor recreation, study sessions, and enjoying the beautiful Boston scenery. Vibrant Off-Campus Community: Beyond the dorms, Bay State Road is home to a thriving off-campus community, with local shops, restaurants, and social hubs that cater to BU students. Public Transportation: The MBTA Green Line's B branch runs directly through the Bay State area, making it a breeze to get around campus and explore the city. Amenities and Resources: Many of the Bay State dorms offer on-site amenities like fitness centers, study lounges, and community kitchens to enhance the residential experience.",
    "chunk_id": "guidetobu_2",
    "source_type": "guidetobu",
    "source_url": "https://guidetobu.com/housing/bay-state-road-bu/",
    "dorm": "Bay State Road",
    "date": "2025-01-01",
    "heading_path": "Bay State Road > Amenities and Perks of Bay State Road Living"
  }

  Source: Guide To BU Wiki | https://guidetobu.com/housing/danielsen-hall/
  Chunk:
  {
    "text": "[GuidetoBU | Danielsen Hall > Things to Consider About Danielsen Hall]\nCarefully weigh the pros and cons to see if Danielsen is the right housing choice for you.",
    "chunk_id": "guidetobu_18",
    "source_type": "guidetobu",
    "source_url": "https://guidetobu.com/housing/danielsen-hall/",
    "dorm": "Danielsen Hall",
    "date": "2025-01-01",
    "heading_path": "Danielsen Hall > Things to Consider About Danielsen Hall"
  },

```

## Sample Chunks and Source Attribution

Below are 5 labeled sample chunks extracted from the knowledge base, displaying the parsed text and their respective source document names.

### Chunk 1
* **Source URL:** https://www.reddit.com/r/BostonU/comments/1t8s6yp/my_rankingadvice_for_freshman_housing/
* **Chunk Text:**
  > "[Reddit | Thread: My ranking/advice for freshman housing : BostonU | Date: 2026-05-10 | Score: 20]\ nalso the closest T is kenmore which is a bit of a walk and its underground so you have to pay kilachand: great location right near marcis and central campus. i havent personally seen the dorms however im pretty sure they have ac and private bathrooms. and you dont have to be in the honors college to live there hojo: i havent seen a room however most are triples and doubles are hard to come by. personally im not the biggest fan of the vibes of hojo it feels like a creepy musty old hotel however it has a great location in central campus bay state road brownstones: each brownstone is different however from the ones ive seen they are oftentimes very spacious. its hard with housing as a freshman becaudse you dont know where on bay state you will be because it goes pretty far down. towers: solid option good location and is on baystate road so more peaceful and quiet than warren on comm ave."



### Chunk 2
* **Source URL:** https://www.reddit.com/r/BostonU/comments/1qgtrjm/best_freshman_dorms/
* **Chunk Text:**
  > "[Reddit | Thread: Best Freshman dorms? : BostonU | Date: 2026-01-19 | Score: 10]\nbut, i don't understand why these small town people think warren and west are trash. warren gave me the best first year oof my lives and in still friends with them today. these cringe kids have to stop acting they going to be thrown in Azkaba."


### Chunk 3
* **Source URL:** https://www.ratemydorm.com/reviews/boston-university/boston-university-1019-commonwealth-avenue
* **Chunk Text:**
  > "[RateMyDorm | Dorm: 1019 Commonwealth Avenue | Date: 2023-01-01 | Room: unknown]\nDefinitely a good place to live sophomore year or even for underclassmen if you can get it. If you dont mind its one bathroom for average 6 people, 3 doubles in a suite so if you want a single you are out of luck with 1019. Overall pretty nice place but very far west so if you have classes say in Questrom thats rough."


### Chunk 4
* **Source URL:** https://www.ratemydorm.com/reviews/boston-university/boston-university-bay-state-road-brownstones
* **Chunk Text:**
  > "[RateMyDorm | Dorm: Bay State Road Brownstones | Date: 2021-01-01 | Room: double]\nOurs had two common areas, beautiful hardwood flooring in the room, laundry in the basement. A few problems, though: one tiny shared closet, shared bathroom (1 between 6 girls), construction starting right outside the window for the past two years now starting at 7am"


### Chunk 5
* **Source URL:** https://guidetobu.com/housing/bay-state-road-bu/
* **Chunk Text:**
  > "[GuidetoBU | Bay State Road > Amenities and Perks of Bay State Road Living]\nLiving on Bay State Road comes with a host of convenient amenities and benefits that enhance the overall college experience: Proximity to Campus: With the BU central campus just a short walk away, Bay State residents have easy access to classrooms, dining halls, and other university resources. Green Spaces: The tree-lined streets and Charles River Esplanade provide ample opportunities for outdoor recreation, study sessions, and enjoying the beautiful Boston scenery. Vibrant Off-Campus Community: Beyond the dorms, Bay State Road is home to a thriving off-campus community, with local shops, restaurants, and social hubs that cater to BU students. Public Transportation: The MBTA Green Line's B branch runs directly through the Bay State area, making it a breeze to get around campus and explore the city. Amenities and Resources: Many of the Bay State dorms offer on-site amenities like fitness centers, study lounges, and community kitchens to enhance the residential experience."


**Final chunk count: 428**

---

## Test Retrieval Examples:

*Note: The retrieval pipeline is configured to return $k=8$ chunks. For readability, only the top-ranked chunks are shown below.*


#### Retrieval Test Example 1
* **Query**: "Does Warren Towers have AC?"
* **Top Returned Chunks**:
  1. *(Score: 0.32)* "[GuidetoBU | Warren Towers > The AC Situation (Pre-Renovation)] Warren Towers has no air conditioning in unrenovated towers. This is consistently cited as the #1 complaint. BU provides a fan, but the first month of school (late August through September) can be brutal -- Boston regularly hits the 80s and occasionally the 90s. As one student on RateMyDorm put it: "The rooms have no AC so it can get hot (only for like the first month of school but they give u a fan so there's that)." The heating system in winter creates the opposite problem: "The heating at Warren is always really high, like sweltering, sweaty, gross high," reported a student on Roomsurf. The baseboard heating has no individual room controls. Window AC units are not permitted in traditional residence halls. Post-renovation: All sleeping rooms and lounges in renovated towers will have air conditioning. Tower A (Fall 2026) will be the first to get it."
  2. *(Score: 0.48)* "[GuidetoBU | Warren Towers > The $550 Million Renovation: Everything Changes] Sustainability: The renovation targets LEED Gold certification and, combined with BU Wind offsets, aims to be net-zero greenhouse gas emissions. What this means for you: If you move into Tower A in Fall 2026, you'll experience a completely different building than what older reviews describe. If assigned to Tower B (2026-2027) or Tower C (2025-2027), you'll still experience the unrenovated Warren for one or two more years. BU Today described the pre-renovation Warren as having "beige cinderblock walls, uninspired common areas and, worst of all, no air conditioning." The renovation addresses every major student complaint."
* **Relevance Explanation**: The first chunk is highly relevant as indicated by it's low distance score and because it answers the query directly, and with the context that renovated towers have AC. The second chunk, though with a relatively poor distance score, provides specific details about when air-conditioning will arrive in other towers.


#### Retrieval Test Example 2
* **Query**: "What's the best way to get from Fenway to the rest of campus?"
* **Top Returned Chunks**:
  1. *(Score: 0.27)* "Reddit | Thread: FENWAY LIVING EXPERIENCE AS A FRESHMAN : BostonU | Date: 2026-02-12 | Score: 14] The big negatives: The closest T stops are longwood/Fenway (d line) each about a 5 minute walk, and St Mary’s (c line) about a 9 minute walk, and having to switch at kenmore (it’s honestly just more time efficient to walk to main campus, I ABUSE the b line on comm ave tho). The walk. The distance. The having to plan out your commute anywhere. Separation from main campus amenities like the fitrec, library, and other dining hall choices. Overall, I’ve really enjoyed living in Fenway campus and especially Peabody, I was hella disappointed getting placed here but I honestly think it’s one of the best experiences I’ve had and it made my freshman year memorable and fun! Feel free to reach out with any questions TLDR; not good but not bad, walk is definitely annoying but dorms are solid and dining hall is good, accessible to a lot of places."
  2. *(Score: 0.30)* "[Reddit | Thread: My ranking/advice for freshman housing : BostonU | Date: 2026-05-10 | Score: 20] there is a fenway bus and its possible to get over to main campus through T however you would need to make a transfer at kenmore. overall fenwayt dorms and food seem very nice however its a bit far from main campus so that is definitely something to keep in mind. i dont know if bu plans on keeping fenway freshman only indefinitely because then that might mean fenway freshman will get a good housing number for sohphore housing since they cant do same room or internal selection. danielson: danielson is lowkey musty and old and a 10 min walk from marcis it is the farthest building on the east side of campus. however the rooms are big and my friend's had a walk in closet but im not sure if all rooms have one. also there are individual private bathrooms. it is extremely close to newbury street so super convient to go downtown."
* **Relevance Explanation**: Both chunks provide specific details about how to reach parts of the campus using public transportation, directly answering the query.


#### Retrieval Test Example 3
* **Query**: "Does Myles Standish Hall offer singles?"
* **Top Returned Chunks**:
  1. *(Score: 0.36)* "[RateMyDorm | Dorm: Myles Standish Hall | Date: 2021-01-01 | Room: single] Some of the singles are smaller than others so it is a little bit of a gamble but it is a very nice dorm."
  2. *(Score: 0.38)* "[RateMyDorm | Dorm: Myles Standish Hall | Date: 2023-01-01 | Room: unknown] Currently living here as a junior at BU, unfortunately got stuck in the smallest room in a suite with my best friends, but at least theres that. We currently are in an 8 person suite with 3 doubles and 2 singles. Myles is great but on the very far east side of campus so if you dont have class in Questrom its a long walk, but good news is theres a bus that comes straight to your front door just not as frequently as other places on campus."
* **Relevance Explanation**: The first chunk's prepended metadata includes the room type as a single, confirming that the answer to the query is yes. Additionally, both chunks mention room configurations.

## Embedding Model

**Model used: `all-MiniLM-L6-v2`**

A lightweight sentence-transformers model that runs locally with no API key or rate limits. It maps text to 384-dimensional vectors, with good performance on short to medium passages. Tradeoffs accepted: 
- Lower accuracy than larger models (e.g., OpenAI's `text-embedding-3-large`), but no cost and no latency from network calls.
- Compressed representation of meaning, but narrow domain means core content meaning should be preserved.

**Production tradeoff reflection:**

- Embedding quality: a larger model would likely handle semantic nuances of a review to review closely related but ultimately distinct embeddings.
- Multilingual support: BU has a huge number of international students. Injesting feedback on student housing in different languages would add to the diversity of perspectives to the corpus.
- Domain expertise: a model tuned to have a greater understanding of BU housing slang and abbreviations would make more useful embeddings.
- Context length: I would consider opting for a model with a larger context window if I implemented conversation history. This could be a useful feature as a student could reasonably wish to describe their needs and priorities and query the tool with that context maintained. This could get large as each retrieved chunk is included with the conversation history at each turn. I would also consider expanding top-k to ensure source diversity, which could fill up the context window pre-prompt.
- Re-ranking: For more accurate results, retrieve a higher top-k and then rerank results and only pass top 5 ranked results to the LLM.

---

## Grounded Generation

#### Example system responses with source attribution

**Example 1:**
* **User Query:** "What is planned for the Warren Towers renovation?"
* **System Response:** "According to the Guide to BU, the Warren Towers renovation is a $550 million, multi-year project that will completely transform the building. The renovationtargets LEED Gold certification and aims to be net-zero greenhouse gas emissions. Specific changes include the addition of full air conditioning in all rooms and lounges, all-gender, single-user bathrooms, triple-glazed, operable windows, electronic card-entry locks, dimmable LED lighting, new furniture, entirely new plumbing, and improved insulation. The renovation will also address fire safety and accessibility, with a new sprinkler system, fire alarm, and ADA-compliant widened doors. The project is scheduled to be completed in phases, with Tower A reopening in Fall 2026, Tower B in Fall 2027, and Tower C in Fall 2028.
Sources:
· Guide to BU | Warren Towers > The $550 Million Renovation: Everything Changes
· Rate My Dorm | Warren Towers
· Reddit | What dorm should I choose? : BostonU
· Guide to BU | Warren towers > The Honest Review: What Students Love & Hate" 

**Example 2:**
* **User Query:** "Which dorms are best for upperclassmen?"
* **System Response:** "According to the Reddit thread 'best and worst dorms/suites to live in as a sophomore transfer?', students recommend Hojo or Bay State for upperclassmen. Reviews on RateMyDorm do not specifically mention upperclassmen preferences, but the Reddit thread suggests that Hojo has private bathrooms and is relatively close to CAS, making it a quiet and convenient option. Bay State is also mentioned as a desirable option, although it may be more difficult to get into. Students on Reddit note that Towers may also be an option, but it may have fewer social opportunities for freshmen, which could be a plus for upperclassmen looking for a quieter environment.
Sources:
· Rate My Dorm | StuVi1 (10 Buick St)
· Rate My Dorm | Kilachand Hall
· Reddit | Best/worst dorms : BostonU
· Reddit | What dorm should I choose? : BostonU
· Reddit | best and worst dorms/suites to live in as a sophomore transfer? : BostonU
· Rate My Dorm | Warren Towers
· Reddit | Best Freshman dorms? : BostonU
· Reddit | BU Housing Ranking?? : BostonU" 

**Example system response for out-of-scope query**
* **User Query:** "What's the official overnight guest policy for Stuvi2?"
* **System Response:** "I couldn't find anything relevant in the available documents. Try rephrasing your question — or check that your ingestion pipeline is working."

**System prompt grounding instruction:**

Responses are grounded in two ways. First, deterministically by returning an error string if the retrieval function did not retrieve any relevant chunks (distance score > 0.6). Second, with specific instructions on how to attribute sources and handle chunks lacking relevant context. These are placed before and after the chunk context to ensure the LLM adhere to them. These are the prompts:

```
PROMPT_PREFIX = (
    "You are an expert student housing assistant for Boston University (BU). "
    "Your job is to answer the user's question using ONLY the provided text chunks. "
    "Adhere strictly to these instructions:\n"
    "1. Base your answer entirely on the provided text chunks. Do not use any outside knowledge.\n"
    "2. Naturally attribute the perspectives you use in your response (e.g., 'Students on Reddit noted...', 'According to the Guide to BU...', 'Reviews on RateMyDorm suggest...').\n"
    "3. Keep your tone helpful, informative, and objective."
)

FINAL_CONSTRAINTS_REMINDER = (
    "CRITICAL REMINDER: Evaluate the context provided above carefully. "
    "If the context is missing, empty, or does not contain enough specific information "
    "to answer the question accurately, you must ignore your persona and reply EXACTLY with: "
    "'I'm sorry, I couldn't find any relevant information about that housing option.' "
    "Do not attempt to guess, extrapolate, or look for information outside of the provided text."
)
```

The system prompt is formatted as follows:

```
    Prompt structure:
    +-------------------------------------------------------------+
    | 1. Prompt Prefix                                            |
    +-------------------------------------------------------------+
    | 2. Retrieved Context Chunks                                 |
    +-------------------------------------------------------------+
    | 3. Final Constraints Reminder                               |
    +-------------------------------------------------------------+
    | 4. User query                                               |
    +-------------------------------------------------------------+
```

**How source attribution is surfaced in the response:**

By including the source as metadata within the chunk text, the LLM is able to to naturally attribute its generated perspective to the source referenced within the chunk. Additionally, metadata is extracted from the received chunks, which is then used to deterministically generate a human-readable list of cited sources with relevant source information (source type and location of info within source) that is returned along with the response to the system prompt.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | How big are the beds in Warren Towers? | Sources cite double or twin XL beds | Couldn't find relevant information | Off-target | Inaccurate | 
| 2 | What are the room options for Stuvi2? | Single, double, and triple room configurations with private bathrooms. | The response correctly mentioned the room types but failed to highlight private bathrooms. Response lacked detail overall.| Partially relevant | Partialy Accurate |
| 3 | What do students say about living in West campus and taking classes at CAS? | Students consistently say that the walk from West campus for classes in CAS is long and crowded. | Response identifies the walk time, transportation options, and that the distance to CAS can feel great. |  Relevant | Accurate |
| 4 | What's the guest policy at Stuvi2?  | The system should acknowledge that it doesn't have the information, as it's an official policy not present in these community docs. | System acknowledges it can't find that information. | Relevant | Accurate |
| 5 | What's the standout feature of living at Fenway? | Students consistently praise the quality of the dining hall, despite the distance to west campus. | Response calls out the dining hall specifically, and includes celebrated food options. It also surfaces other community benefits. | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:**

How big are the beds in Warren Towers?

**What the system returned:**

Gradio interface returned: "I'm sorry, I couldn't find any relevant information about the size of the beds in Warren Towers." But the actual answer was in the first chunk returned by the `retrieve()` function that returns a list of top-k related chunks.

**Root cause (tied to a specific pipeline stage):**

I think there could be a couple root causes.

First, in my `generator` function I added a secondary guard against insufficient context within the provided sources. I included the following prompt after the chunks when constructing the LLM generation prompt:

```
FINAL_CONSTRAINTS_REMINDER = (
    "CRITICAL REMINDER: Evaluate the context provided above carefully. "
    "If the context is missing, empty, or does not contain enough specific information "
    "to answer the question accurately, you must ignore your persona and reply EXACTLY with: "
    "'I'm sorry, I couldn't find any relevant information about that housing option.' "
    "Do not attempt to guess, extrapolate, or look for information outside of the provided text."
)
```
I beleive Groq reviewed the chunks and determined that overall the content was noisy and determined returning the error was the best response. I could also try increasing the temperature of the response.

I think the second issue is a chunking issue. The source where this information is located (Guide To BU Wiki) has short but dense sections that sometimes contain multiple different themes of related information. It's possible that the chunks for this one source are too noisy. The chunks returned for this query have a distance > 0.48, which hints at relatively poor retrieval, despite the answer to the question being in the third sentence of the first chunk.

**What you would change to fix it:**

I would first try updating the `FINAL_CONSTRAINS_REMINDER` prompt to relax the constraints slightly. I would have to verify responses to other prompts to ensure that bad responses then start filtering through.

For the second issue, I would chunk content from the Guide To BU Wiki more aggressively. I think chunking by section header was too lenient, despite the short length of the sections. Reviewing the sections more closely, they contain greater breadth of information than the Reddit or RateMyDorm posts. Rather than greedily add sentences to chunks of 150-175 words (8-10 sentences), I would reduce the word count to 50-75% of that value. I would carry the change over to Reddit and Rate My Dorm sources as well, which do not seem to exhibit the same issue, but I believe that's because long posts on those sources is more anomalous. 

---

## Interface Design & Sample Interaction

### Interface Fields

*   **Input Fields:**
    *   **Your question (`gr.Textbox`)**: A text input box where users type their natural language questions.
    *   **Ask (`gr.Button`)**: A trigger button to submit the question. Pressing `Enter` inside the input box also submits the query.
*   **Output Fields:**
    *   **Answer (`gr.Textbox`)**: An 8-line text area displaying the final generated response from the LLM.
    *   **Retrieved from (`gr.Textbox`)**: A 4-line text area displaying the specific document sources and chunk metadata used to ground the answer.

### Sample Interaction Transcript

**User Question:** 
> "Which dorms are best for meeting people and making friends?"

**Answer:**
> "According to the provided documents, students have mentioned that certain dorms are better for meeting people and making friends. Reviews on RateMyDorm suggest that StuVi2 has a "super social atmosphere", which could be beneficial for making friends. On Reddit, a student noted that Warren is one of the most social dorms, and that it's easier to make friends there, even though the dorms themselves are not the best. Another Reddit user mentioned that Warren, along with other communal dorms, are the most social and that everywhere else is "too quiet and hard to make friends". However, it's also mentioned that Brownstones and Hojo (575 Comm Ave) might not be the best options for freshmen looking to make friends, as they tend to have more upperclassmen and established friend groups."

**Retrieved from:**
> "Sources:
· Rate My Dorm | Hojo (575 Comm Ave)
· Reddit | Best/worst dorms : BostonU
· Rate My Dorm | The Towers
· Reddit | What dorm should I choose? : BostonU
· Reddit | best and worst dorms/suites to live in as a sophomore transfer? : BostonU
· Rate My Dorm | StuVi2 (33 Harry Agganis Way)
· Reddit | BU Housing Ranking?? : BostonU
· Rate My Dorm | 1019 Commonwealth Avenue"

---

## Spec Reflection

**One way the spec helped you during implementation:**

The spec was essential to my implementation because it allowed me to direct Claude Code at an implementation task and linking to critical context by just referencing functions, file paths, and specs within the planning.md files. I supplemented the spec for cleaning, but otherwise I was able to use what I wrote to direct Claude's implementations iteratively. With the help of AI chat to reinforce concepts, I was able to come up with a well-defined and specific chunking strategy in particular, which I believe made implementation go smoothly.

**One way your implementation diverged from the spec, and why:**

I had to increase my top-k number from 5 to 8 because I was finding that the retriever was returning chunks with correct results but distances of ~0.4-0.5, which struck me as surprisingly poor given the answer was in the text. It's possible that the imbalance of chunks per source was a contributing factor (reddit=101, ratemydorm=250, guidetobu=77). Increasing top-k to 8 ensured that chunks containing the answer were retrieved.

---

## AI Usage

**Instance 1**

- *What I gave the AI:*
I gave the AI my cleaning_spec.md file that contains instructions for cleaning source HTML files. 

- *What it produced:*
It noticed written patterns for Reddit comments that ended in a new line rather than punctuation which it said indicates the comment had not been fully expanded in the HTML and Reddit had truncated it. It recommended a spec change to skip comments not ending in punctuation. I initially accepted the change which produced .txt files missing Reddit thread comments.

- *What I changed or overrode:*
I verified that the HTML files contained the fully expanded reply, and removed that instruction from the spec with the justification that Reddit replies contain informal language lacking punctuation.

**Instance 2**

- *What I gave the AI:*
I gave the AI my architecture section, `retrieve.py` and a scaffolded `generator.py` file and asked it to finish implementing `generate_response()` and `construct_sources_cited()` functions. 

- *What it produced:*
In `construct_sources_cited` it looped over a dict which stored the source-specific detail name (e.g. reddit = "thread_title", ratemydorm = "dorm" etc.) to identify a chunk's source through an equality check, which it then used to construct the sources cited list. 

- *What I changed or overrode:*
This seemed like an indirect way of obtaining that information, given that the attribute `source_type` exists in the metadata for each chunk in the list returned by `retrieve.py`. I overrode this and instructed it to look up the source using `source_type`.
