import json
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_BASE_PATH = (
    BASE_DIR / "data" / "knowledge_base.json"
)


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_text(text):
    """Normalize text for retrieval."""

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# LOAD KNOWLEDGE BASE
# =========================================================

def load_knowledge_base():
    """Load FAQ data from the JSON knowledge base."""

    with open(
        KNOWLEDGE_BASE_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# =========================================================
# BUILD SEARCH INDEX
# =========================================================

def build_search_index(knowledge_base):
    """
    Build TF-IDF search index.

    Questions and keywords receive more importance
    than generic FAQ answer text.
    """

    documents = []

    for item in knowledge_base:

        question = normalize_text(
            item.get("question", "")
        )

        keywords = " ".join(
            normalize_text(keyword)
            for keyword in item.get(
                "keywords",
                []
            )
        )

        category = normalize_text(
            item.get("category", "")
        )

        document = (
            question + " "
            + question + " "
            + question + " "
            + keywords + " "
            + keywords + " "
            + category
        )

        documents.append(document)


    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        sublinear_tf=True
    )


    document_vectors = vectorizer.fit_transform(
        documents
    )


    return (
        vectorizer,
        document_vectors
    )


# =========================================================
# INTENT PHRASES
# =========================================================

INTENT_PHRASES = {

    # -----------------------------------------------------
    # BILLING
    # -----------------------------------------------------

    "duplicate_payment": [
        "charged twice",
        "charged two times",
        "billed twice",
        "billed two times",
        "duplicate charge",
        "duplicate payment",
        "payment duplicated",
        "payment was duplicated",
        "two charges",
        "charged double",
        "payment taken twice",
        "same payment twice",
        "payment twice",
        "charged more than once",
        "billed more than once",
        "duplicate billing",
    ],


    # -----------------------------------------------------
    # TECHNICAL
    # -----------------------------------------------------

    "notification_problem": [
        "not receiving notifications",
        "not getting notifications",
        "notifications not working",
        "notification does not work",
        "notification doesn't work",
        "not receiving alerts",
        "not getting alerts",
        "alerts not working",
        "notifications stopped",
        "notifications stopped appearing",
        "alerts stopped",
        "alerts stopped appearing",
    ],


    # -----------------------------------------------------
    # PASSWORD / LOGIN
    # -----------------------------------------------------

    "password_reset": [
        "forgot my password",
        "forgot password",
        "forgotten password",
        "reset password",
        "password reset",
        "cannot log in",
        "can't log in",
        "unable to log in",
        "cannot login",
        "can't login",
        "unable to login",
        "cannot sign in",
        "can't sign in",
        "unable to sign in",
    ],


    # -----------------------------------------------------
    # GENERAL ACCOUNT ACCESS
    # -----------------------------------------------------

    "account_access": [
        "cannot access my account",
        "can't access my account",
        "unable to access my account",

        "cannot enter my account",
        "can't enter my account",
        "unable to enter my account",

        "cannot get into my account",
        "can't get into my account",
        "unable to get into my account",

        "locked out",
        "account locked",

        "lost access to my account",
    ],
}


# =========================================================
# DETECT INTENT
# =========================================================

def detect_intent(query):

    text = normalize_text(query)

    detected = []

    for intent, phrases in INTENT_PHRASES.items():

        for phrase in phrases:

            if phrase in text:

                detected.append(intent)

                break


    return detected


# =========================================================
# SEARCH KNOWLEDGE BASE
# =========================================================

def search_knowledge_base(
    query,
    vectorizer,
    document_vectors,
    knowledge_base,
    top_k=3,
    category=None
):
    """
    Retrieve relevant FAQ entries.

    Uses:

    1. TF-IDF similarity
    2. Question matching
    3. Keyword matching
    4. Intent matching
    5. Category filtering
    6. Account-access override
    """

    normalized_query = normalize_text(
        query
    )


    # =====================================================
    # QUERY VECTOR
    # =====================================================

    query_vector = vectorizer.transform(
        [normalized_query]
    )


    similarities = cosine_similarity(
        query_vector,
        document_vectors
    ).flatten()


    # =====================================================
    # DETECT INTENT
    # =====================================================

    detected_intents = detect_intent(
        normalized_query
    )


    # =====================================================
    # GENERAL ACCOUNT ACCESS OVERRIDE
    # =====================================================

    general_account_access = any(
        phrase in normalized_query

        for phrase in [

            "cannot enter my account",
            "can't enter my account",
            "unable to enter my account",

            "cannot get into my account",
            "can't get into my account",
            "unable to get into my account",

            "cannot access my account",
            "can't access my account",
            "unable to access my account",

            "unable to sign in",
            "cannot sign in",
            "can't sign in",

            "unable to log in",
            "cannot log in",
            "can't log in",

            "unable to login",
            "cannot login",
            "can't login",
        ]
    )


    if general_account_access:

        detected_intents = [
            "account_access"
        ]


    # =====================================================
    # SCORE RESULTS
    # =====================================================

    scored_results = []


    for index, item in enumerate(
        knowledge_base
    ):

        item_category = item.get(
            "category",
            ""
        )


        # -------------------------------------------------
        # CATEGORY FILTER
        # -------------------------------------------------

        if category:

            if (
                item_category.lower()
                != category.lower()
            ):

                continue


        # -------------------------------------------------
        # TF-IDF SCORE
        # -------------------------------------------------

        tfidf_score = float(
            similarities[index]
        )


        # -------------------------------------------------
        # FAQ QUESTION
        # -------------------------------------------------

        question = normalize_text(
            item.get(
                "question",
                ""
            )
        )


        # -------------------------------------------------
        # FAQ KEYWORDS
        # -------------------------------------------------

        keywords = [
            normalize_text(keyword)

            for keyword in item.get(
                "keywords",
                []
            )
        ]


        # -------------------------------------------------
        # QUERY / QUESTION WORD MATCH
        # -------------------------------------------------

        query_words = set(
            normalized_query.split()
        )

        question_words = set(
            question.split()
        )


        shared_words = (
            query_words
            & question_words
        )


        question_score = 0.0


        if shared_words:

            question_score = min(
                len(shared_words) * 0.08,
                0.40
            )


        # -------------------------------------------------
        # KEYWORD MATCH
        # -------------------------------------------------

        keyword_score = 0.0


        for keyword in keywords:

            if not keyword:

                continue


            if keyword in normalized_query:

                keyword_score += 0.20

            else:

                keyword_words = set(
                    keyword.split()
                )


                if (
                    keyword_words
                    and keyword_words.issubset(
                        query_words
                    )
                ):

                    keyword_score += 0.20


        keyword_score = min(
            keyword_score,
            0.50
        )


        # -------------------------------------------------
        # FAQ SEARCH TEXT
        # -------------------------------------------------

        faq_text = (
            question
            + " "
            + " ".join(keywords)
        )


        # -------------------------------------------------
        # INTENT BOOST
        # -------------------------------------------------

        intent_boost = 0.0


        # =================================================
        # DUPLICATE PAYMENT
        # =================================================

        if "duplicate_payment" in detected_intents:

            duplicate_terms = [

                "charged twice",
                "charged two times",
                "billed twice",
                "billed two times",
                "duplicate charge",
                "duplicate payment",
                "payment duplicated",
                "two charges",
                "charged double",
                "payment taken twice",
                "same payment twice",
                "payment twice",
            ]


            if any(
                term in faq_text

                for term in duplicate_terms
            ):

                intent_boost = max(
                    intent_boost,
                    0.60
                )


        # =================================================
        # NOTIFICATIONS
        # =================================================

        if "notification_problem" in detected_intents:

            notification_terms = [

                "notification",
                "notifications",
                "alert",
                "alerts",
            ]


            if any(
                term in faq_text

                for term in notification_terms
            ):

                intent_boost = max(
                    intent_boost,
                    0.50
                )


        # =================================================
        # PASSWORD RESET
        # =================================================

        if "password_reset" in detected_intents:

            password_terms = [

                "password",
                "reset password",
                "login",
                "log in",
                "sign in",
            ]


            if any(
                term in faq_text

                for term in password_terms
            ):

                intent_boost = max(
                    intent_boost,
                    0.45
                )


        # =================================================
        # GENERAL ACCOUNT ACCESS
        # =================================================

        if "account_access" in detected_intents:

            access_terms = [

                "account",
                "access",
                "login",
                "log in",
                "sign in",
                "password",
            ]


            if any(
                term in faq_text

                for term in access_terms
            ):

                intent_boost = max(
                    intent_boost,
                    0.40
                )


            # ------------------------------------------------
            # IMPORTANT:
            # General sign-in/access problems should prefer
            # the password/login FAQ.
            # ------------------------------------------------

            if general_account_access:

                if (
                    "password" in faq_text
                    or "reset password" in faq_text
                    or "login" in faq_text
                    or "log in" in faq_text
                    or "sign in" in faq_text
                ):

                    intent_boost = max(
                        intent_boost,
                        0.65
                    )


        # =================================================
        # FINAL SCORE
        # =================================================

        final_score = (

            tfidf_score * 0.45

            + question_score

            + keyword_score

            + intent_boost
        )


        # =================================================
        # RESULT
        # =================================================

        scored_results.append(
            {
                "id": item["id"],
                "category": item["category"],
                "question": item["question"],
                "answer": item["answer"],
                "score": final_score,
            }
        )


    # =====================================================
    # SORT
    # =====================================================

    scored_results.sort(
        key=lambda item: item["score"],
        reverse=True
    )


    # =====================================================
    # RETURN TOP RESULTS
    # =====================================================

    return scored_results[:top_k]