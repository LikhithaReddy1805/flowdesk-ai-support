from rag import (
    load_knowledge_base,
    build_search_index,
    search_knowledge_base
)

from classifier import classify_ticket


# ============================================================
# LOAD
# ============================================================

knowledge_base = load_knowledge_base()

vectorizer, document_vectors = build_search_index(
    knowledge_base
)


# ============================================================
# TEST QUERIES
# ============================================================

test_queries = [

    # --------------------------------------------------------
    # BILLING
    # --------------------------------------------------------

    "I was charged twice for my subscription.",

    "My payment was duplicated.",

    "Why did I get billed two times?",

    "There are two charges on my account.",

    "My card was charged twice.",

    "I think I made the same payment twice.",


    # --------------------------------------------------------
    # TECHNICAL
    # --------------------------------------------------------

    "Why am I not getting notifications?",

    "Notifications have stopped appearing.",


    # --------------------------------------------------------
    # ACCOUNT
    # --------------------------------------------------------

    "I forgot my password and cannot log in.",

    "I am unable to sign in.",

    "I cannot enter my account anymore.",
]


# ============================================================
# RUN TESTS
# ============================================================

for query in test_queries:

    print("\n" + "=" * 70)

    print("Query:")
    print(query)


    # --------------------------------------------------------
    # CLASSIFICATION
    # --------------------------------------------------------

    classification = classify_ticket(
        query
    )


    print(
        "Category:",
        classification["category"]
    )

    print(
        "Classification confidence:",
        classification["confidence"]
    )


    # --------------------------------------------------------
    # RAG
    # --------------------------------------------------------

    results = search_knowledge_base(
        query,
        vectorizer,
        document_vectors,
        knowledge_base,
        top_k=3,
        category=classification["category"]
    )


    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    if not results:

        print(
            "No relevant results found."
        )

        continue


    for result in results:

        print()

        print(
            result["id"],
            "|",
            result["category"],
            "|",
            f"{result['score']:.3f}"
        )

        print(
            result["question"]
        )

        print(
            "Answer:",
            result["answer"]
        )