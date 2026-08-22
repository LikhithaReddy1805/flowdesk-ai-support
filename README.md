# FlowDesk AI Support 🤖

FlowDesk AI Support is an AI-powered Tier-1 customer support application that automatically classifies customer queries, retrieves relevant information from a knowledge base, generates support responses, and escalates unsupported requests to human support.

The system combines **query classification, TF-IDF-based RAG retrieval, category filtering, cosine similarity, and Google Gemini** to provide relevant and context-aware customer support.

## 🚀 Features

* 💬 Customer support chat interface
* 🧠 Automatic query classification
* 💳 Billing issue detection
* 🔧 Technical issue detection
* 🔐 Account access issue detection
* 🔎 TF-IDF-based FAQ retrieval
* 📚 Category-filtered knowledge-base search
* 🤖 Gemini-powered support responses
* 📊 Confidence scoring
* 📖 Knowledge-base source display
* 👤 Human escalation for unsupported requests
* 🛡️ Safe handling of unknown queries

## 🔄 How It Works

```text
                    Customer Query
                          |
                          v
                  Text Normalization
                          |
                          v
                  Query Classification
                          |
              +-----------+-----------+
              |                       |
           Unknown              Supported Category
              |                       |
              v                       v
      Human Escalation         Knowledge Base Search
                                      |
                                      v
                                Relevant FAQ
                                      |
                                      v
                            AI Response Generation
                                      |
                                      v
                                Final Response
```

## 📂 Supported Categories

### 💳 Billing

Handles billing-related customer requests such as:

* Duplicate charges
* Duplicate payments
* Subscription billing
* Refund requests
* Payment-related issues

**Example query:**

```text
I was charged twice for my subscription.
```

**Expected result:**

```text
Category: Billing
Confidence: 90%
FAQ: BILL-002
```

### 🔧 Technical

Handles technical issues such as:

* Notifications not working
* File upload problems
* Application performance issues
* Browser-related questions

**Example query:**

```text
Why am I not receiving notifications?
```

**Expected result:**

```text
Category: Technical
Confidence: 90%
FAQ: TECH-001
```

### 🔐 Account Access

Handles account-related issues such as:

* Forgotten passwords
* Login problems
* Account access problems
* Account recovery

**Example query:**

```text
I cannot access my account anymore.
```

**Expected result:**

```text
Category: Account Access
Confidence: 90%
```

## 👤 Human Escalation

If a customer request does not belong to any supported FlowDesk category, the system does **not** return an unrelated FAQ.

Instead, the request is classified as **Unknown** and escalated to human support.

**Example:**

```text
Can you tell me the weather today?
```

**Result:**

```text
Category: Unknown
Confidence: 0%
Retrieved: 0 FAQ(s)

Human Escalation Required
```

This prevents irrelevant knowledge-base answers from being returned to customers.

## 📚 Knowledge Base

FlowDesk uses a JSON-based knowledge base containing FAQ information.

Each FAQ contains:

* FAQ ID
* Category
* Question
* Answer
* Keywords

### Example

```text
FAQ ID: BILL-002

Category:
Billing

Question:
I was charged twice for my subscription. What should I do?
```

The knowledge base is stored in:

```text
data/knowledge_base.json
```

## 🔎 RAG Retrieval

The retrieval system uses a lightweight **Retrieval-Augmented Generation (RAG)** approach.

### Retrieval Pipeline

```text
Customer Query
      |
      v
Text Processing
      |
      v
TF-IDF Vectorization
      |
      v
Unigram + Bigram Matching
      |
      v
Category Filtering
      |
      v
Cosine Similarity
      |
      v
Most Relevant FAQ
```

### Technologies Used

* TF-IDF Vectorization
* Unigram matching
* Bigram matching
* Cosine similarity
* Category filtering

The user's query is compared against the FlowDesk FAQ knowledge base, and the most relevant FAQ entries are retrieved.

**Example:**

```text
User:
I was charged twice

Retrieved FAQ:
BILL-002

I was charged twice for my subscription.
What should I do?
```

## 🤖 AI Response Generation

Google Gemini is used to generate natural-language customer support responses.

The retrieved knowledge-base information is provided to Gemini as context.

The AI is instructed to:

* Use the retrieved FlowDesk knowledge
* Answer the customer's question clearly
* Avoid inventing FlowDesk policies
* Avoid generating unsupported information
* Escalate when the available knowledge is insufficient

This helps keep generated responses grounded in the application's knowledge base.

## 🛠️ Technology Stack

| Technology        | Purpose                    |
| ----------------- | -------------------------- |
| Python            | Backend application logic  |
| Streamlit         | Customer support interface |
| Scikit-learn      | Machine learning utilities |
| TF-IDF            | FAQ retrieval              |
| Cosine Similarity | Query-to-FAQ matching      |
| Google Gemini API | AI response generation     |
| JSON              | Knowledge-base storage     |
| HTML/CSS          | UI customization           |

## 📁 Project Structure

```text
supervity-support-ai/
│
├── app.py
│
├── data/
│   └── knowledge_base.json
│
├── utils/
│   ├── ai.py
│   ├── classifier.py
│   ├── rag.py
│   ├── escalation.py
│   ├── test_classifier.py
│   └── test_rag.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/LikhithaReddy1805/supervity-support-ai.git
```

Navigate to the project:

```bash
cd supervity-support-ai
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

### ⚠️ Security

Never expose your Gemini API key publicly.

Do **not** commit the following files or directories to GitHub:

```text
.env
venv/
__pycache__/
```

Make sure they are included in `.gitignore`.

Example `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
```

## ▶️ Running the Application

From the project root, run:

```bash
streamlit run app.py
```

The application will start at:

```text
http://localhost:8501
```

Open the URL in your browser to access the FlowDesk AI Support interface.

## 🧪 Testing

FlowDesk includes tests for both the classifier and RAG retrieval system.

### Classifier Test

From the project root:

```bash
cd utils
python test_classifier.py
```

The classifier tests:

* Billing
* Technical
* Account Access
* Unknown queries

### RAG Test

From the `utils` directory:

```bash
python test_rag.py
```

The RAG test verifies that relevant FAQ entries are retrieved for different customer queries.

## 🧪 Example Test Cases

### Billing

**Input:**

```text
I was charged twice
```

**Expected:**

```text
Category: Billing
Confidence: 90%
FAQ: BILL-002
```

### Duplicate Payment

**Input:**

```text
My payment was duplicated
```

**Expected:**

```text
Category: Billing
FAQ: BILL-002
```

### Account Access

**Input:**

```text
I cannot access my account anymore.
```

**Expected:**

```text
Category: Account Access
Confidence: 90%
```

### Technical

**Input:**

```text
Notifications are not working
```

**Expected:**

```text
Category: Technical
FAQ: TECH-001
```

### Unknown Request

**Input:**

```text
Can you tell me the weather today?
```

**Expected:**

```text
Category: Unknown
Confidence: 0%
Retrieved: 0 FAQ(s)

Human Escalation Required
```

## 🛡️ Security

The Gemini API key is stored using an environment variable rather than being hardcoded in the application.

Sensitive files should never be committed to GitHub.

```text
.env
venv/
__pycache__/
```

## 📈 Project Status

The core FlowDesk AI Support workflow has been implemented and tested.

### Implemented

* [x] Query classification
* [x] Billing classification
* [x] Technical classification
* [x] Account Access classification
* [x] Unknown query detection
* [x] Knowledge-base retrieval
* [x] TF-IDF vectorization
* [x] Cosine similarity
* [x] Category filtering
* [x] AI-generated support responses
* [x] Confidence scoring
* [x] Knowledge-base source display
* [x] Unknown query handling
* [x] Human escalation
* [x] Streamlit support interface

## 🎯 Project Goal

The goal of **FlowDesk AI Support** is to automate common Tier-1 customer support tasks while ensuring that unsupported or uncertain requests are safely escalated to human support.

The application demonstrates how traditional information retrieval techniques such as **TF-IDF and cosine similarity** can be combined with modern **Generative AI** to build a practical customer support system.

## 🔮 Future Improvements

Potential future enhancements include:

* Multi-turn conversation memory
* More support categories
* Improved intent classification using transformer models
* Vector database integration
* Semantic embeddings for retrieval
* Conversation history
* Agent dashboard for escalated tickets
* Ticket creation and tracking
* Feedback-based response improvement
* Analytics dashboard
* Authentication and role-based access
* Production deployment

## 👩‍💻 Author

**Likhitha Reddy**

Computer Science Engineering Graduate

GitHub: `https://github.com/LikhithaReddy1805`

LinkedIn: `https://linkedin.com/in/likhitha-reddy-b`

---
