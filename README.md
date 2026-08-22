# FlowDesk AI Support

FlowDesk AI Support is an AI-powered Tier-1 customer support application that automatically classifies customer queries, retrieves relevant information from a knowledge base, generates support responses, and escalates unsupported requests to human support.

## Features

- Customer support chat interface
- Automatic query classification
- Billing issue detection
- Technical issue detection
- Account access issue detection
- TF-IDF based FAQ retrieval
- Category-filtered knowledge-base search
- Gemini-powered support responses
- Confidence scoring
- Knowledge-base source display
- Human escalation for unsupported requests

## How It Works

Customer Query
      |
      v
Text Normalization
      |
      v
Ticket Classification
      |
      +----------------------+
      |                      |
      | Unknown              | Supported Category
      |                      |
      v                      v
Human Escalation       Knowledge Base Search
                             |
                             v
                       Relevant FAQ
                             |
                             v
                    AI Response Generation
                             |
                             v
                       Final Response

## Supported Categories

### Billing

Handles billing-related requests such as:

- Duplicate charges
- Duplicate payments
- Subscription billing
- Refund requests
- Payment-related issues

Example:

I was charged twice for my subscription.

Expected result:

Category: Billing
Confidence: 90%
FAQ: BILL-002

### Technical

Handles technical issues such as:

- Notifications not working
- File upload problems
- Application performance issues
- Browser-related questions

Example:

Why am I not receiving notifications?

Expected result:

Category: Technical
Confidence: 90%
FAQ: TECH-001

### Account Access

Handles account-related issues such as:

- Forgotten passwords
- Login problems
- Account access problems
- Account recovery

Example:

I cannot access my account anymore.

Expected result:

Category: Account Access
Confidence: 90%

## Human Escalation

If a request does not belong to one of the supported FlowDesk categories, the system does not return an unrelated FAQ.

Instead, it marks the request as unknown and escalates it to human support.

Example:

Can you tell me the weather today?

Result:

Category: Unknown
Confidence: 0%
Retrieved: 0 FAQ(s)

Human Escalation Required

This prevents irrelevant knowledge-base answers from being returned.

## Knowledge Base

The application uses a JSON-based FlowDesk knowledge base containing:

- FAQ ID
- Category
- Question
- Answer
- Keywords

Example:

BILL-002

Category:
Billing

Question:
I was charged twice for my subscription. What should I do?

## RAG Retrieval

The retrieval system uses:

- TF-IDF vectorization
- Unigram and bigram matching
- Cosine similarity
- Category filtering

The user's query is compared with the FAQ knowledge base and the most relevant entries are retrieved.

Example:

User:
I was charged twice

Retrieved FAQ:

BILL-002

I was charged twice for my subscription. What should I do?

## AI Response Generation

Gemini is used to generate natural-language customer support responses based on the retrieved FlowDesk knowledge-base content.

The AI is instructed to use the retrieved knowledge rather than inventing FlowDesk policies or information.

## Technology Stack

- Python
- Streamlit
- Scikit-learn
- TF-IDF
- Cosine Similarity
- Google Gemini API
- JSON
- HTML/CSS

## Project Structure

supervity-support-ai/
|
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ app.py
|
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ data/
|   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ knowledge_base.json
|
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ utils/
|   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ ai.py
|   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ classifier.py
|   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ rag.py
|   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ escalation.py
|   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ test_classifier.py
|   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ test_rag.py
|
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ .env
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ .gitignore
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ requirements.txt
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ README.md

## Installation

### 1. Create a virtual environment

python -m venv venv

### 2. Activate the virtual environment

Windows:

venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

## Environment Variables

Create a .env file in the project root and add:

GEMINI_API_KEY=your_api_key_here

Do not expose your API key publicly.

Do not commit the .env file to GitHub.

## Running the Application

Run the following command from the project root:

streamlit run app.py

The application will be available at:

http://localhost:8501

## Testing

### Classifier Test

cd utils
python test_classifier.py

The classifier tests Billing, Technical, Account Access, and Unknown queries.

### RAG Test

python test_rag.py

This verifies that relevant FAQ entries are retrieved for different customer queries.

## Example Test Cases

### Billing

Input:

I was charged twice

Expected:

Category: Billing
Confidence: 90%
FAQ: BILL-002

### Duplicate Payment

Input:

My payment was duplicated

Expected:

Category: Billing
FAQ: BILL-002

### Account Access

Input:

I cannot access my account anymore.

Expected:

Category: Account Access
Confidence: 90%

### Technical

Input:

Notifications are not working

Expected:

Category: Technical
FAQ: TECH-001

### Unknown Request

Input:

Can you tell me the weather today?

Expected:

Category: Unknown
Confidence: 0%
Retrieved: 0 FAQ(s)
Human Escalation Required

## Security

The Gemini API key is stored using an environment variable.

The following should not be committed to GitHub:

.env
venv/
__pycache__/

Use .gitignore to prevent accidental uploads.

## Project Status

The core FlowDesk AI Support workflow has been implemented and tested, including:

- Query classification
- Knowledge-base retrieval
- Category filtering
- AI-generated responses
- Confidence scoring
- Knowledge-base source display
- Unknown query handling
- Human escalation

## Project Goal

The goal of FlowDesk AI Support is to automate Tier-1 customer support tasks while ensuring that unsupported or uncertain requests are safely escalated to human support.

