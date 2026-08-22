import html
import streamlit as st

from utils.classifier import classify_ticket

from utils.rag import (
    load_knowledge_base,
    build_search_index,
    search_knowledge_base
)

from utils.escalation import should_escalate
from utils.ai import generate_support_response


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FlowDesk AI Support",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

html,
body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: #050a14 !important;
    color: #f8fafc !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

footer {
    display: none !important;
}

.main .block-container {
    max-width: 1250px !important;
    padding: 22px 28px 110px 28px !important;
}


/* ============================================================
   HEADER
   ============================================================ */

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 15px 20px;

    background: linear-gradient(
        135deg,
        #0d172a,
        #0b1425
    );

    border: 1px solid #263d63;
    border-radius: 16px;

    box-shadow:
        0 0 25px rgba(37, 99, 235, 0.08);

    margin-bottom: 18px;
}

.brand {
    display: flex;
    align-items: center;
    gap: 14px;
}

.logo {
    width: 46px;
    height: 46px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 12px;

    background: linear-gradient(
        135deg,
        #6366f1,
        #06b6d4
    );

    color: white;
    font-size: 24px;

    box-shadow:
        0 0 20px rgba(99, 102, 241, 0.25);
}

.brand-title {
    color: #ffffff;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.3px;
}

.brand-subtitle {
    color: #a7b6cf;
    font-size: 13px;
    margin-top: 3px;
}

.online {
    display: flex;
    align-items: center;
    gap: 8px;

    color: #d5dfef;
    font-size: 13px;
    font-weight: 600;
}

.online-dot {
    width: 9px;
    height: 9px;

    background: #22c55e;

    border-radius: 50%;

    box-shadow:
        0 0 10px rgba(34, 197, 94, 0.7);
}


/* ============================================================
   WELCOME PANEL
   ============================================================ */

.welcome-panel {
    background: linear-gradient(
        135deg,
        #091426,
        #07101e
    );

    border: 1px solid #263d63;
    border-radius: 16px;

    padding: 30px 25px 25px;

    text-align: center;

    box-shadow:
        0 0 30px rgba(37, 99, 235, 0.05);

    margin-bottom: 16px;
}

.welcome-title {
    color: #ffffff;

    font-size: 38px;
    font-weight: 800;

    letter-spacing: -0.8px;

    margin-bottom: 10px;
}

.welcome-text {
    color: #b8c6da;

    font-size: 16px;
    line-height: 1.65;

    max-width: 850px;

    margin: 0 auto;
}


/* ============================================================
   CAPABILITY CARDS
   ============================================================ */

.capability {
    background: #0b1729;

    border: 1px solid #29436c;

    border-radius: 12px;

    padding: 12px 16px;

    text-align: left;

    min-height: 62px;
}

.capability-title {
    color: #f8fafc;

    font-size: 14px;
    font-weight: 750;
}

.capability-text {
    color: #a7b6cf;

    font-size: 11px;

    margin-top: 4px;
}


/* ============================================================
   EXAMPLES
   ============================================================ */

.example-title {
    color: #f1f5f9;

    font-size: 18px;
    font-weight: 750;

    margin-top: 18px;
    margin-bottom: 9px;
}

.example-subtitle {
    color: #91a2bb;

    font-size: 12px;

    margin-bottom: 10px;
}


/* ============================================================
   EXAMPLE BUTTONS
   ============================================================ */

.stButton > button {
    width: 100% !important;

    min-height: 58px !important;

    background: #0b1729 !important;

    color: #f1f5f9 !important;

    border: 1px solid #29436c !important;

    border-radius: 11px !important;

    font-size: 14px !important;

    font-weight: 650 !important;

    text-align: left !important;

    padding-left: 18px !important;

    transition: all 0.15s ease !important;
}

.stButton > button:hover {
    background: #111f36 !important;

    border-color: #4f7fd4 !important;

    color: #ffffff !important;

    transform: translateY(-1px);
}


/* ============================================================
   CHAT PANEL
   ============================================================ */

.chat-panel {
    background: #091321;

    border: 1px solid #263d63;

    border-radius: 16px;

    padding: 20px;

    margin-top: 20px;

    box-shadow:
        0 0 30px rgba(37, 99, 235, 0.04);
}


/* ============================================================
   USER MESSAGE
   ============================================================ */

.user-row {
    display: flex;

    justify-content: flex-end;

    margin: 15px 0;
}

.user-message {
    max-width: 75%;

    background: linear-gradient(
        135deg,
        #2563eb,
        #3b82f6
    );

    color: #ffffff;

    padding: 13px 17px;

    border-radius: 16px 16px 5px 16px;

    font-size: 16px;

    font-weight: 500;

    line-height: 1.55;

    box-shadow:
        0 5px 20px rgba(37, 99, 235, 0.15);
}


/* ============================================================
   AI MESSAGE
   ============================================================ */

.ai-row {
    display: flex;

    align-items: flex-start;

    margin: 15px 0;
}

.ai-icon {
    width: 38px;
    height: 38px;

    min-width: 38px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 10px;

    background: linear-gradient(
        135deg,
        #6366f1,
        #06b6d4
    );

    color: white;

    font-size: 19px;

    margin-right: 11px;
}

.ai-content {
    max-width: 82%;
}

.ai-message {
    background: #101c2f;

    border: 1px solid #29436c;

    color: #f1f5f9;

    padding: 15px 18px;

    border-radius: 16px 16px 16px 5px;

    font-size: 16px;

    line-height: 1.65;

    box-shadow:
        0 5px 20px rgba(0, 0, 0, 0.12);
}


/* ============================================================
   INFO BADGES
   ============================================================ */

.badges {
    display: flex;

    flex-wrap: wrap;

    gap: 8px;

    margin-top: 10px;
}

.badge {
    background: #0a1525;

    border: 1px solid #304b74;

    border-radius: 8px;

    padding: 7px 11px;

    color: #b6c5d9;

    font-size: 13px;

    font-weight: 500;
}

.badge strong {
    color: #ffffff;

    font-weight: 750;
}


/* ============================================================
   KNOWLEDGE SOURCE
   ============================================================ */

.source {
    background: #081525;

    border: 1px solid #39734d;

    border-radius: 10px;

    padding: 11px 13px;

    margin-top: 10px;
}

.source-title {
    color: #4ade80;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 0.4px;

    margin-bottom: 5px;
}

.source-id {
    color: #e2e8f0;

    font-size: 14px;

    font-weight: 750;
}

.source-question {
    color: #b7c6d9;

    font-size: 13px;

    line-height: 1.5;

    margin-top: 3px;
}


/* ============================================================
   RESOLVED
   ============================================================ */

.resolved {
    background: #08251a;

    border: 1px solid #2f9e62;

    border-radius: 10px;

    padding: 11px 14px;

    margin-top: 10px;

    color: #86efac;

    font-size: 13px;

    font-weight: 650;
}


/* ============================================================
   ESCALATION
   ============================================================ */

.escalation {
    background: #2a1218;

    border: 1px solid #b33a4b;

    border-radius: 10px;

    padding: 12px 14px;

    margin-top: 10px;
}

.escalation-title {
    color: #fb7185;

    font-size: 14px;

    font-weight: 800;
}

.escalation-reason {
    color: #fecdd3;

    font-size: 13px;

    line-height: 1.55;

    margin-top: 4px;
}


/* ============================================================
   CHAT INPUT
   ============================================================ */

[data-testid="stChatInput"] {
    background: #0d192b !important;

    border: 1px solid #35537d !important;

    border-radius: 13px !important;

    margin-top: 12px !important;

    box-shadow:
        0 0 20px rgba(37, 99, 235, 0.08);
}

[data-testid="stChatInput"] textarea {
    background: #0d192b !important;

    color: #ffffff !important;

    font-size: 16px !important;

    line-height: 1.5 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #91a2bb !important;

    opacity: 1 !important;
}


/* ============================================================
   CLEAR BUTTON
   ============================================================ */

.clear-button > button {
    min-height: 38px !important;

    font-size: 12px !important;

    text-align: center !important;

    color: #a7b6cf !important;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 700px) {

    .main .block-container {
        padding: 12px 12px 100px 12px !important;
    }

    .header {
        padding: 12px;
    }

    .brand-title {
        font-size: 17px;
    }

    .brand-subtitle {
        font-size: 9px;
    }

    .welcome-title {
        font-size: 29px;
    }

    .welcome-text {
        font-size: 13px;
    }

    .user-message,
    .ai-content {
        max-width: 90%;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# INITIALIZE BACKEND
# ============================================================

@st.cache_resource
def initialize_system():

    knowledge_base = load_knowledge_base()

    vectorizer, document_vectors = build_search_index(
        knowledge_base
    )

    return (
        knowledge_base,
        vectorizer,
        document_vectors
    )


knowledge_base, vectorizer, document_vectors = initialize_system()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# ============================================================
# HEADER
# ============================================================

st.html("""
<div class="header">

    <div class="brand">

        <div class="logo">
            ⚡
        </div>

        <div>

            <div class="brand-title">
                FlowDesk AI Support
            </div>

            <div class="brand-subtitle">
                Customer Support AI Employee • Tier-1 Triage
            </div>

        </div>

    </div>

    <div class="online">

        <div class="online-dot"></div>

        AI Online

    </div>

</div>
""")


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.messages:

    st.html("""
    <div class="welcome-panel">

        <div class="welcome-title">
            How can we help?
        </div>

        <div class="welcome-text">
            Ask about billing, technical issues, or account access.
            FlowDesk AI classifies your request, searches the
            knowledge base, and escalates when human assistance
            is required.
        </div>

    </div>
    """)


    # ========================================================
    # CAPABILITY CARDS
    # ========================================================

    c1, c2, c3 = st.columns(3)

    with c1:

        st.html("""
        <div class="capability">

            <div class="capability-title">
                📚 Knowledge Base
            </div>

            <div class="capability-text">
                Answers grounded in FlowDesk FAQs
            </div>

        </div>
        """)


    with c2:

        st.html("""
        <div class="capability">

            <div class="capability-title">
                🧠 Smart Classification
            </div>

            <div class="capability-text">
                Billing • Technical • Account Access
            </div>

        </div>
        """)


    with c3:

        st.html("""
        <div class="capability">

            <div class="capability-title">
                👤 Human Escalation
            </div>

            <div class="capability-text">
                Escalates when confidence is low
            </div>

        </div>
        """)


    # ========================================================
    # EXAMPLES
    # ========================================================

    st.html("""
    <div class="example-title">
        Try an example
    </div>

    <div class="example-subtitle">
        Select an issue to test the support workflow
    </div>
    """)


    c1, c2, c3 = st.columns(3)


    with c1:

        if st.button(
            "💳  Charged twice\nBilling issue",
            use_container_width=True
        ):

            st.session_state.pending_question = (
                "I was charged twice for my subscription."
            )

            st.rerun()


    with c2:

        if st.button(
            "🔧  Notifications not working\nTechnical issue",
            use_container_width=True
        ):

            st.session_state.pending_question = (
                "I am not receiving notifications."
            )

            st.rerun()


    with c3:

        if st.button(
            "🔐  Can't access account\nAccount access issue",
            use_container_width=True
        ):

            st.session_state.pending_question = (
                "I can't get into my account."
            )

            st.rerun()


# ============================================================
# PROCESS QUESTION
# ============================================================

def process_question(user_message):

    # ========================================================
    # CLASSIFICATION
    # ========================================================

    classification = classify_ticket(
        user_message
    )

    category = classification.get(
        "category",
        "unknown"
    )


    # ========================================================
    # UNKNOWN REQUEST
    #
    # IMPORTANT:
    # DO NOT SEARCH THE KNOWLEDGE BASE.
    #
    # This prevents questions such as:
    # "What is the weather?"
    #
    # from retrieving an unrelated FlowDesk FAQ.
    # ========================================================

    if category == "unknown":

        results = []

        decision = {
            "escalate": True,

            "reason": (
                "The request could not be confidently "
                "classified into a supported category."
            )
        }

        answer = (
            "I'm sorry, but this request is outside "
            "the FlowDesk support categories I can "
            "handle. I've escalated your request to "
            "a human support agent."
        )

        return (
            answer,
            classification,
            results,
            decision
        )


    # ========================================================
    # RAG SEARCH
    # ========================================================

    results = search_knowledge_base(

        user_message,

        vectorizer,

        document_vectors,

        knowledge_base,

        top_k=3,

        category=category
    )


    # ========================================================
    # REMOVE WEAK RESULTS
    # ========================================================

    useful_results = []

    for result in results:

        score = float(
            result.get(
                "score",
                0
            )
        )

        if score >= 0.20:

            useful_results.append(
                result
            )


    results = useful_results


    # ========================================================
    # NO RELEVANT RESULT
    # ========================================================

    if not results:

        decision = {
            "escalate": True,

            "reason": (
                "No sufficiently relevant information "
                "was found in the FlowDesk knowledge base."
            )
        }

        answer = (
            "I couldn't find enough information in "
            "the FlowDesk knowledge base to answer "
            "this accurately. I've escalated your "
            "request to a human support agent."
        )

        return (
            answer,
            classification,
            results,
            decision
        )


    # ========================================================
    # ESCALATION CHECK
    # ========================================================

    decision = should_escalate(

        classification,

        results
    )


    # ========================================================
    # GENERATE RESPONSE
    # ========================================================

    answer = generate_support_response(

        user_message,

        results
    )


    # ========================================================
    # RETURN
    # ========================================================

    return (
        answer,
        classification,
        results,
        decision
    )


# ============================================================
# DISPLAY CHAT
# ============================================================

if st.session_state.messages:

    st.html("""
    <div class="chat-panel">
    """)


    for message in st.session_state.messages:


        # ====================================================
        # USER MESSAGE
        # ====================================================

        if message["role"] == "user":

            safe_message = html.escape(
                message["content"]
            )

            st.html(f"""
            <div class="user-row">

                <div class="user-message">
                    {safe_message}
                </div>

            </div>
            """)


        # ====================================================
        # AI MESSAGE
        # ====================================================

        else:

            safe_answer = html.escape(
                message["content"]
            )

            classification = message.get(
                "classification"
            )

            results = message.get(
                "results",
                []
            )

            decision = message.get(
                "decision"
            )


            st.html(f"""
            <div class="ai-row">

                <div class="ai-icon">
                    ⚡
                </div>

                <div class="ai-content">

                    <div class="ai-message">
                        {safe_answer}
                    </div>
            """)


            # =================================================
            # CLASSIFICATION
            # =================================================

            if classification:

                category = classification.get(
                    "category",
                    "unknown"
                )

                confidence = classification.get(
                    "confidence",
                    0
                )

                confidence_percent = int(
                    confidence * 100
                )


                st.html(f"""
                <div class="badges">

                    <div class="badge">

                        Category:

                        <strong>
                            {html.escape(category.title())}
                        </strong>

                    </div>


                    <div class="badge">

                        Confidence:

                        <strong>
                            {confidence_percent}%
                        </strong>

                    </div>


                    <div class="badge">

                        Retrieved:

                        <strong>
                            {len(results)} FAQ(s)
                        </strong>

                    </div>

                </div>
                """)


            # =================================================
            # KNOWLEDGE SOURCE
            # =================================================

            if results:

                best = results[0]

                faq_id = html.escape(
                    str(
                        best.get(
                            "id",
                            "Unknown"
                        )
                    )
                )

                question = html.escape(
                    str(
                        best.get(
                            "question",
                            ""
                        )
                    )
                )

                score = float(
                    best.get(
                        "score",
                        0
                    )
                )


                # Convert score to UI percentage
                #
                # TF-IDF score can be > 1 because
                # the current retrieval implementation
                # may use boosted values.

                relevance_percent = min(
                    100,
                    max(
                        0,
                        int(score * 100)
                    )
                )


                st.html(f"""
                <div class="source">

                    <div class="source-title">
                        ✓ KNOWLEDGE BASE SOURCE
                    </div>

                    <div class="source-id">

                        {faq_id}

                        • Match {relevance_percent}%

                    </div>

                    <div class="source-question">
                        {question}
                    </div>

                </div>
                """)


            # =================================================
            # ESCALATION / RESOLUTION
            # =================================================

            if decision:

                if decision.get("escalate"):

                    reason = html.escape(
                        str(
                            decision.get(
                                "reason",
                                "Human support is required."
                            )
                        )
                    )


                    st.html(f"""
                    <div class="escalation">

                        <div class="escalation-title">
                            ⚠ Human Escalation Required
                        </div>

                        <div class="escalation-reason">
                            {reason}
                        </div>

                    </div>
                    """)

                else:

                    st.html("""
                    <div class="resolved">
                        ✓ Resolved using the FlowDesk knowledge base
                    </div>
                    """)


            st.html("""
                </div>
            </div>
            """)


    st.html("""
    </div>
    """)


# ============================================================
# SAMPLE QUESTION
# ============================================================

if st.session_state.pending_question:

    question = st.session_state.pending_question

    st.session_state.pending_question = None


    # Add user message

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })


    # Process

    (
        answer,
        classification,
        results,
        decision
    ) = process_question(
        question
    )


    # Add AI message

    st.session_state.messages.append({

        "role": "assistant",

        "content": answer,

        "classification": classification,

        "results": results,

        "decision": decision

    })


    st.rerun()


# ============================================================
# CHAT INPUT
# ============================================================

user_message = st.chat_input(
    "Describe your issue..."
)


if user_message:

    # Add user message

    st.session_state.messages.append({

        "role": "user",

        "content": user_message

    })


    # Process

    (
        answer,
        classification,
        results,
        decision
    ) = process_question(
        user_message
    )


    # Add AI response

    st.session_state.messages.append({

        "role": "assistant",

        "content": answer,

        "classification": classification,

        "results": results,

        "decision": decision

    })


    st.rerun()


# ============================================================
# CLEAR CHAT
# ============================================================

if st.session_state.messages:

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    c1, c2, c3 = st.columns(
        [1, 1, 1]
    )


    with c2:

        if st.button(
            "Clear conversation",
            use_container_width=True
        ):

            st.session_state.messages = []

            st.rerun()