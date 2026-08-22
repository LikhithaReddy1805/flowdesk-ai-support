from classifier import classify_ticket


test_messages = [

    # Billing variations
    "I was charged twice for my subscription.",
    "My payment was duplicated.",
    "Why did I get billed two times?",
    "There are two charges on my account.",

    # Technical variations
    "Why am I not receiving notifications?",
    "I'm not getting any alerts.",
    "The notification feature doesn't work.",

    # Account access variations
    "I can't get into my account.",
    "I forgot my login credentials.",
    "I'm locked out of my account.",

    # Out of scope
    "Can you tell me the weather today?"
]


for message in test_messages:

    result = classify_ticket(message)

    print("\n--------------------------------")
    print("Message:", message)
    print("Category:", result["category"])
    print("Confidence:", result["confidence"])
    print("Scores:", result["scores"])