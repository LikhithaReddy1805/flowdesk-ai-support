from rag import load_knowledge_base
from rag import build_search_index
from rag import search_knowledge_base

from ai import generate_support_response


# Load the knowledge base
knowledge_base = load_knowledge_base()

# Build the search index
vectorizer, document_vectors = build_search_index(
    knowledge_base
)

# Test question
user_message = "I was charged twice for my subscription."

# Search the knowledge base
results = search_knowledge_base(
    user_message,
    vectorizer,
    document_vectors,
    knowledge_base
)

# Generate AI response
answer = generate_support_response(
    user_message,
    results
)

print("\nAI RESPONSE:\n")
print(answer)