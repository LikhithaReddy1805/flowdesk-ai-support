from classifier import classify_ticket
from rag import (
    load_knowledge_base,
    build_search_index,
    search_knowledge_base
)
from escalation import should_escalate


knowledge_base = load_knowledge_base()

vectorizer, document_vectors = build_search_index(
    knowledge_base
)


test_messages = [
    "I was charged twice for my subscription.",
    "I forgot my password and cannot log in.",
    "Can you tell me what the weather is today?"
]


for message in test_messages:

    classification = classify_ticket(message)

    retrieved_faqs = search_knowledge_base(
        message,
        vectorizer,
        document_vectors,
        knowledge_base
    )

    decision = should_escalate(
        classification,
        retrieved_faqs
    )

    print("\n--------------------------------")
    print("Message:", message)
    print("Category:", classification["category"])
    print("Classification confidence:", classification["confidence"])
    print("Retrieved FAQs:", len(retrieved_faqs))
    print("Escalate:", decision["escalate"])
    print("Reason:", decision["reason"])