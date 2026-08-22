import re


# ============================================================
# CATEGORY PATTERNS
# ============================================================

CATEGORY_PATTERNS = {

    # ========================================================
    # BILLING
    # ========================================================

    "billing": {

        "strong": [

            "charged twice",
            "charged two times",
            "billed twice",
            "billed two times",

            "duplicate charge",
            "duplicate payment",
            "payment duplicated",
            "payment was duplicated",
            "duplicate transaction",

            "two charges",
            "charged double",
            "payment taken twice",

            # Refund + duplicate payment variations
            "duplicate payment refund",
            "refund for duplicate payment",
            "refund duplicate payment",
            "duplicate charge refund",
            "refund for duplicate charge",
            "charged twice refund",
            "payment twice refund",

            "refund for being charged twice",
            "refund for duplicate charge",
            "refund for duplicate transaction",

        ],

        "normal": [

            "bill",
            "billing",
            "billed",

            "charge",
            "charged",

            "payment",
            "paid",

            "price",
            "pricing",

            "refund",
            "refunds",

            "invoice",

            "subscription",
            "subscriptions",

            "cost",
            "money",

            "transaction",
            "transactions",

        ],
    },


    # ========================================================
    # TECHNICAL
    # ========================================================

    "technical": {

        "strong": [

            "not receiving notifications",
            "not getting notifications",
            "notifications not working",

            "notification doesn't work",
            "notification does not work",

            "not receiving alerts",
            "not getting alerts",

            "alerts not working",

            "upload failed",
            "upload failure",

            "application crashed",
            "application crash",

            "browser not working",
            "browser issue",

        ],

        "normal": [

            "bug",
            "error",
            "broken",
            "slow",
            "loading",

            "upload",
            "uploads",

            "notification",
            "notifications",

            "alert",
            "alerts",

            "browser",
            "browsers",

            "crash",
            "crashed",

            "technical",

            "not working",
            "doesn't work",
            "does not work",

            "failed",
            "failure",

            "issue",
            "problem",

        ],
    },


    # ========================================================
    # ACCOUNT ACCESS
    # ========================================================

    "account access": {

        "strong": [

            "forgot my password",
            "forgot password",

            "can't log in",
            "cannot log in",

            "can't login",
            "cannot login",

            "can not log in",
            "can not login",

            "can't access my account",
            "cannot access my account",

            "unable to access my account",
            "unable to access account",

            "can't enter my account",
            "cannot enter my account",

            "unable to enter my account",

            "locked out",
            "account locked",

            "forgot my login credentials",

            "can't get into my account",
            "cannot get into my account",

            "unable to get into my account",

            "cannot sign in",
            "unable to sign in",

            "can't sign in",
            "can't signin",

            "cannot signin",
            "unable to signin",

        ],

        "normal": [

            "password",

            "login",
            "log in",
            "signin",
            "sign in",

            "logged out",

            "account",
            "access",

            "locked",
            "lockout",

            "email",

            "two factor",
            "2fa",

            "authentication",

            "credentials",

        ],
    },
}


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    """
    Normalize user input before classification.
    """

    if not text:
        return ""

    text = str(text).lower()

    # Preserve letters/numbers/spaces.
    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    # Collapse repeated spaces.
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# CLASSIFIER
# ============================================================

def classify_ticket(message):

    """
    Classify a customer support message.

    Returns:

        {
            "category": "...",
            "confidence": 0.90,
            "scores": {...}
        }
    """

    text = normalize_text(message)


    # ========================================================
    # INITIAL SCORES
    # ========================================================

    scores = {

        "billing": 0.0,

        "technical": 0.0,

        "account access": 0.0,

    }


    # Keep track of matched patterns.

    strong_matches = {

        "billing": [],

        "technical": [],

        "account access": [],

    }


    normal_matches = {

        "billing": [],

        "technical": [],

        "account access": [],

    }


    # ========================================================
    # MATCH PATTERNS
    # ========================================================

    for category, patterns in CATEGORY_PATTERNS.items():

        # ----------------------------------------------------
        # STRONG MATCHES
        # ----------------------------------------------------

        for phrase in patterns["strong"]:

            if phrase in text:

                scores[category] += 4.0

                strong_matches[category].append(
                    phrase
                )


        # ----------------------------------------------------
        # NORMAL MATCHES
        # ----------------------------------------------------

        for keyword in patterns["normal"]:

            if keyword in text:

                scores[category] += 1.0

                normal_matches[category].append(
                    keyword
                )


    # ========================================================
    # SPECIAL CASES
    # ========================================================

    # --------------------------------------------------------
    # Duplicate + refund = strongly billing
    # --------------------------------------------------------

    has_duplicate = any(
        phrase in text
        for phrase in [
            "duplicate",
            "charged twice",
            "charged two times",
            "billed twice",
            "billed two times",
            "two charges",
            "payment twice",
        ]
    )

    has_refund = (
        "refund" in text
        or "refunds" in text
    )

    if has_duplicate and has_refund:

        scores["billing"] += 5.0

        strong_matches["billing"].append(
            "duplicate refund request"
        )


    # --------------------------------------------------------
    # Account access intent
    # --------------------------------------------------------

    access_intent_phrases = [

        "cannot access my account",
        "unable to access my account",

        "cannot enter my account",
        "unable to enter my account",

        "cannot get into my account",
        "unable to get into my account",

        "cannot sign in",
        "unable to sign in",

        "cannot login",
        "unable to login",

    ]

    if any(
        phrase in text
        for phrase in access_intent_phrases
    ):

        scores["account access"] += 3.0

        strong_matches["account access"].append(
            "account access intent"
        )


    # ========================================================
    # FIND BEST CATEGORY
    # ========================================================

    best_category = max(
        scores,
        key=scores.get
    )

    best_score = scores[
        best_category
    ]


    # ========================================================
    # UNKNOWN
    # ========================================================

    if best_score == 0:

        return {

            "category": "unknown",

            "confidence": 0.0,

            "scores": scores,

        }


    # ========================================================
    # SECOND BEST CATEGORY
    # ========================================================

    sorted_scores = sorted(
        scores.values(),
        reverse=True
    )

    second_score = sorted_scores[1]


    # ========================================================
    # CONFIDENCE
    # ========================================================

    if strong_matches[best_category]:

        confidence = 0.90

    elif best_score >= 3:

        confidence = 0.80

    else:

        confidence = 0.65


    # ========================================================
    # COMPETING CATEGORY
    # ========================================================

    if (
        second_score > 0
        and second_score >= best_score * 0.75
    ):

        confidence = 0.45


    # ========================================================
    # RETURN
    # ========================================================

    return {

        "category": best_category,

        "confidence": confidence,

        "scores": scores,

    }