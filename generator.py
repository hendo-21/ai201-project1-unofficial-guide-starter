from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

from retrieve import retrieve

_client = Groq(api_key=GROQ_API_KEY)

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

# Maps the source_type that retrieve.py stores on every chunk to (1) a
# user-friendly name and (2) the one detail field worth surfacing for that
# source. Keying off source_type (always present) keeps citation accurate.
SOURCES = {
    "reddit":     ("Reddit",       "thread_title"),
    "guidetobu":  ("Guide to BU",  "heading_path"),
    "ratemydorm": ("Rate My Dorm", "dorm"),
}

def generate_response(query: str, retrieved_chunks: list) -> tuple:
    """
    Answer `query` using ONLY the text in `retrieved_chunks`, then append the
    sources those chunks came from.

    Prompt structure:
    +-------------------------------------------------------------+
    | 1. Prompt Prefix                                            |
    +-------------------------------------------------------------+
    | 2. Retrieved Context Chunks                                 |
    |    - Clearly labeled and separated with XML tags or markers |
    +-------------------------------------------------------------+
    | 3. Final Constraints Reminder                               |
    +-------------------------------------------------------------+
    | 4. User query                                               |
    +-------------------------------------------------------------+
    | 5. Sources cited                                            |
    +-------------------------------------------------------------+

    Parts 1-4 are sent to the LLM as the prompt. Part 5 (the source list) is
    built from the chunk metadata in code and appended to the model's answer.
    """

    # No chunks made it past the retrieval distance threshold, so there is
    # nothing to ground an answer in. Bail out before calling the LLM.
    if not retrieved_chunks:
        answer = (
            "I couldn't find anything relevant in the available documents. "
            "Try rephrasing your question — or check that your ingestion pipeline is working."
        )
        return answer, ''
    # [2] Wrap each chunk in a tag so the model can tell them apart and see
    #     exactly which text it is allowed to use.
    context = _construct_context(retrieved_chunks)

    # The user turn carries the grounding context, then the constraint reminder
    # (placed AFTER the context so it's the LAST instruction the model reads),
    # then the actual question. The persona/rules live in the system message.
    user_message = (
        f"Context:\n{context}\n\n"
        f"{FINAL_CONSTRAINTS_REMINDER}\n\n"
        f"Question: {query}"
    )

    completion = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": PROMPT_PREFIX},
            {"role": "user", "content": user_message},
        ],
        # Low temperature keeps the answer close to the provided context
        # instead of inventing details.
        temperature=0.2,
    )
    answer = (completion.choices[0].message.content or "").strip()

    # If the model followed the reminder and said it has no relevant info, don't
    # tack a "Sources" list onto an answer that doesn't actually cite anything.
    if "couldn't find any relevant information" in answer:
        return answer, ''

    # Return sources string with response for app to display in sources window
    return answer, _construct_sources_cited(retrieved_chunks)


def _construct_context(retrieved_chunks: list) -> str:
    """
    Wrap each retrieved chunk in an XML-style tag so the LLM can clearly tell
    the chunks apart and see which source each one came from.
    """
    blocks = []
    for chunk in retrieved_chunks:
        source = chunk.get("source_type")
        text = chunk.get("text")
        blocks.append(f'<chunk source="{source}">\n{text}\n</chunk>')
    return "\n\n".join(blocks)


def _construct_sources_cited(retrieved_chunks: list) -> str:
    """
    Build a "Sources:" list from the retrieved chunks' metadata.

    For each chunk we read its source_type, look up the friendly name and the
    detail field to surface (see SOURCES), and format a line like
    '· Reddit | <thread title>'. Duplicate lines are skipped so a source cited
    by several chunks only appears once.
    """
    lines = []
    for chunk in retrieved_chunks:
        source_type = chunk.get("source_type")
        label, detail_field = SOURCES.get(source_type, (source_type, None))

        detail_value = chunk.get(detail_field) if detail_field else None
        line = f"· {label} | {detail_value}" if detail_value else f"· {label}"

        if line not in lines:
            lines.append(line)

    return "Sources:\n" + "\n".join(lines)

if __name__ == '__main__':
    query = "What is planned for the Warren Towers renovation?"
    chunks = retrieve(query)
    res = generate_response(query, chunks)
    print(f"\n{res}\n")
