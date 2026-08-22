import os

from google import genai
from google.genai import types


# ============================================================
# GEMINI CLIENT
# ============================================================

API_KEY = os.getenv("GEMINI_API_KEY")


client = None

if API_KEY:
    client = genai.Client(
        api_key=API_KEY
    )


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "gemini-3.6-flash"


# ============================================================
# FALLBACK RESPONSE
# ============================================================

def fallback_response(results):

    if not results:

        return (
            "I could not find enough information in the "
            "FlowDesk knowledge base to answer this request. "
            "Please contact FlowDesk Support for assistance."
        )


    best = results[0]

    answer = best.get(
        "answer",
        ""
    )

    if answer:

        return answer


    return (
        "I found a relevant FlowDesk knowledge-base entry, "
        "but I could not generate a response automatically. "
        "Please contact FlowDesk Support for assistance."
    )


# ============================================================
# GENERATE SUPPORT RESPONSE
# ============================================================

def generate_support_response(
    user_message,
    results
):

    # --------------------------------------------------------
    # No results
    # --------------------------------------------------------

    if not results:

        return (
            "I could not find enough information in the "
            "FlowDesk knowledge base to answer this request. "
            "Please contact FlowDesk Support for assistance."
        )


    # --------------------------------------------------------
    # If Gemini is not configured
    # --------------------------------------------------------

    if client is None:

        return fallback_response(
            results
        )


    # --------------------------------------------------------
    # Build knowledge context
    # --------------------------------------------------------

    knowledge = []

    for item in results:

        question = item.get(
            "question",
            ""
        )

        answer = item.get(
            "answer",
            ""
        )

        knowledge.append(
            f"FAQ Question: {question}\n"
            f"FAQ Answer: {answer}"
        )


    knowledge_context = "\n\n".join(
        knowledge
    )


    # --------------------------------------------------------
    # Prompt
    # --------------------------------------------------------

    prompt = f"""
You are FlowDesk's Tier-1 customer support AI.

Answer the customer's question using ONLY the
FlowDesk knowledge base provided below.

Do not invent policies, prices, procedures,
features, or information.

If the knowledge base does not contain enough
information, say that human support is required.

Keep the answer concise, professional, and helpful.

Customer question:
{user_message}

FlowDesk knowledge base:
{knowledge_context}
"""


    # --------------------------------------------------------
    # Gemini request
    # --------------------------------------------------------

    try:

        response = client.models.generate_content(

            model=MODEL_NAME,

            contents=prompt,

            config=types.GenerateContentConfig(

                temperature=0.2,

                max_output_tokens=300

            )

        )


        if response and response.text:

            return response.text.strip()


        return fallback_response(
            results
        )


    # --------------------------------------------------------
    # QUOTA / RATE LIMIT
    # --------------------------------------------------------

    except Exception as error:

        error_text = str(error).lower()


        if (
            "429" in error_text
            or "resource_exhausted" in error_text
            or "quota" in error_text
        ):

            return fallback_response(
                results
            )


        # ----------------------------------------------------
        # Other Gemini errors
        # ----------------------------------------------------

        return fallback_response(
            results
        )