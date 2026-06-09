"""retrieve.py — Stage 4 (RETRIEVE): find the most relevant chunks for a query.

embed.py (Stage 3) stored every chunk in a ChromaDB collection, embedded with
all-MiniLM-L6-v2. This stage takes a user's question, embeds it with that SAME
model, and asks ChromaDB for the chunks whose vectors are closest to it. Those
chunks become the context that generator.py (Stage 5) hands to the LLM.

We reuse get_collection() from embed.py so the query is embedded by the exact
same SentenceTransformer function the chunks were — querying with a different
model would compare vectors that don't live in the same space.

Run `python retrieve.py` to try a sample query against the stored collection.
"""

from embed import get_collection
from config import N_RESULTS, DISTANCE_THRESHOLD


# What we ask ChromaDB to return for each match. "documents" is the chunk text,
# "metadatas" carries the source fields embed.py stored, "distances" is the
# similarity score (cosine distance: smaller = more similar).
INCLUDE = ["documents", "metadatas", "distances"]

# The metadata field that names each result's source, mapped to the extra field
# we surface for that source (see the per-source output schema in the task spec).
# Reddit -> thread_title, GuidetoBU -> heading_path, RateMyDorm -> dorm.
SOURCE_DETAIL_FIELD = {
    "reddit": "thread_title",
    "guidetobu": "heading_path",
    "ratemydorm": "dorm",
}


def retrieve(query_texts: str, n_results: int = N_RESULTS, include=INCLUDE, threshold: float=DISTANCE_THRESHOLD) -> list[dict]:
    """Return the chunks most relevant to `query_texts`, closest first.

    Args:
        query_texts: the user's question.
        n_results: how many chunks to return (top-k).
        include: which fields ChromaDB should return per match.

    Returns:
        A list of result dicts, one per matched chunk. Every result has "text",
        "source_type", and "distance"; it also carries one source-specific field
        ("thread_title" for Reddit, "heading_path" for GuidetoBU, "dorm" for
        RateMyDorm), pulled from the chunk's stored metadata.
    """
    collection = get_collection()

    # ChromaDB embeds the query string with the collection's embedding function
    # and returns the n_results nearest chunks. query_texts takes a LIST of
    # queries, so we wrap our single query and read back the first (only) result set.
    response = collection.query(
        query_texts=[query_texts],
        n_results=n_results,
        include=include,
    )

    # Each key in the response is a list-of-lists: one inner list per query. We
    # sent one query, so we read index 0 to get this query's parallel lists.
    documents = response["documents"][0]    # type: ignore
    metadatas = response["metadatas"][0]    # type: ignore
    distances = response["distances"][0]    # type: ignore

    results = []
    for text, metadata, distance in zip(documents, metadatas, distances):
        if distance <= threshold:
            source_type = metadata.get("source_type")

            result = {
                "text": text,
                "source_type": source_type,
                "distance": distance,
            }

            # Add the one extra field that makes sense for this source type. If we
            # don't recognize the source, we simply skip the extra field.
            detail_field = SOURCE_DETAIL_FIELD.get(source_type) # type: ignore
            if detail_field is not None:
                result[detail_field] = metadata.get(detail_field)

            results.append(result)

    return results


def main():
    query = "How big are the beds in Warren Towers?"
    print(f"Query: {query}\n")

    results = retrieve(query)
    for rank, result in enumerate(results, start=1):
        print(f"[{rank}] {result['source_type']} (distance: {result['distance']:.4f})")
        print(f"    {result['text'][:200]}...\n")
    print("\n", results)


if __name__ == "__main__":
    main() 
