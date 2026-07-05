# AI Codebase Assistant

AI Codebase Assistant is a Retrieval-Augmented Generation (RAG) application that helps developers understand unfamiliar codebases by answering natural language questions about uploaded project files.

Users can upload a project as a ZIP file, and the application indexes the source code using vector embeddings to generate context-aware responses powered by Google Gemini.

---

## Live Demo

https://ai-codebase-assistant-uu6k.onrender.com/

**Note:** The application is hosted on Render's free tier. The first request may take 1–2 minutes while the server starts.

---

## Features

- Upload an entire project as a ZIP file
- Automatic extraction and processing of source code
- Semantic search using FAISS vector database
- AI-powered question answering using Google Gemini
- Intelligent question routing
  - Answers metadata queries locally
  - Uses RAG for conceptual code understanding
- Project overview generation
- Programming language detection
- Project structure explorer
- Referenced source file viewer with syntax highlighting
- Conversation history
- Confidence score for retrieved results

---

## Tech Stack

### Frontend

- Streamlit

### Backend

- Python

### AI & Machine Learning

- Google Gemini
- LangChain
- FAISS
- Sentence Transformers

### Libraries

- PyPDF
- tiktoken
- python-dotenv

---

## Project Structure

```text
AI-Codebase-Assistant/
│
├── app.py
├── config.py
├── requirements.txt
├── components/
├── services/
├── utils/
├── prompts/
├── assets/
└── uploads/
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Mahelaka29/AI-Codebase-Assistant.git
```

Move into the project directory:

```bash
cd AI-Codebase-Assistant
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GOOGLE_API_KEY=your_api_key
```

Run the application:

```bash
streamlit run app.py
```

---

## How It Works

1. Upload a project as a ZIP file.
2. The application extracts the source code.
3. Source files are divided into semantic chunks.
4. Sentence Transformers generate vector embeddings.
5. Embeddings are stored in a FAISS vector database.
6. Relevant code is retrieved based on the user's query.
7. Google Gemini generates context-aware answers using the retrieved code.

Metadata-related questions are answered locally without invoking the language model, improving response speed and reducing unnecessary API usage.

---

## Sample Questions

- What does this project do?
- Explain the authentication flow.
- Where is the database connection established?
- Describe the project architecture.
- How is user authentication implemented?
- Which files handle API requests?
- Explain this function.
- Where is the main business logic located?

---

## Future Improvements

- GitHub repository import
- Multi-repository support
- Conversation memory
- Repository comparison
- Code dependency visualization
- Support for additional language models
- Docker deployment

---

## Author

**Mahelaka Bano**

LinkedIn: https://linkedin.com/in/mahelakamansoori

GitHub: https://github.com/Mahelaka29