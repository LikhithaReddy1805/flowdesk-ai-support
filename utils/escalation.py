def should_escalate(classification, retrieved_faqs):
    """
    Decide whether a support request should be escalated
    to a human agent.

    Escalate when:
    1. The request is unknown.
    2. Classification confidence is too low.
    3. No relevant knowledge-base answer was found.
    """

    category = classification.get(
        "category",
        "unknown"
    )

    confidence = classification.get(
        "confidence",
        0.0
    )


    # =====================================================
    # UNKNOWN CATEGORY
    # =====================================================

    if category == "unknown":

        return {
            "escalate": True,
            "reason": (
                "The request could not be confidently "
                "classified into a supported category."
            )
        }


    # =====================================================
    # LOW CLASSIFICATION CONFIDENCE
    # =====================================================

    if confidence < 0.50:

        return {
            "escalate": True,
            "reason": (
                "The request was not classified with "
                "sufficient confidence."
            )
        }


    # =====================================================
    # NO KNOWLEDGE-BASE RESULTS
    # =====================================================

    if not retrieved_faqs:

        return {
            "escalate": True,
            "reason": (
                "No relevant knowledge-base information "
                "was found for this request."
            )
        }


    # =====================================================
    # VERY LOW RAG RELEVANCE
    # =====================================================

    best_score = retrieved_faqs[0].get(
        "score",
        0.0
    )


    if best_score < 0.10:

        return {
            "escalate": True,
            "reason": (
                "The request was classified, but no "
                "sufficiently relevant knowledge-base "
                "answer was found."
            )
        }


    # =====================================================
    # ANSWER CAN BE GENERATED
    # =====================================================

    return {
        "escalate": False,
        "reason": (
            "The request was confidently classified "
            "and relevant knowledge was found."
        )
    }