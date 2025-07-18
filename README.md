# 🚀 LLM-Powered Intelligent Query Retrieval System

## Unlock Your Data's Potential with Smart, Conversational AI!

This project introduces a cutting-edge **Intelligent Query Retrieval System** that transforms how you interact with your documents. Powered by advanced Large Language Models (LLMs), it enables natural language conversations with your knowledge base, delivering precise and contextually relevant answers through semantic search and a sophisticated decision engine.

--- 

## ✨ Key Features

*   **🧠 Intelligent Query Processing:** Understands and processes complex natural language queries with the power of LLMs.
*   **🔍 Semantic Search:** Leverages FAISS for lightning-fast and highly relevant semantic search across document embeddings.
*   **📚 Dynamic Document Indexing:** Easily index various document types (PDFs, TXT files) to build your searchable knowledge base.
*   **🎯 Precision Decision Engine:** Refines search results and provides accurate, actionable answers.
*   **🌐 Scalable & Modern Architecture:** Built with a robust FastAPI backend and a sleek Next.js frontend for a seamless user experience.

## 🏗️ Project Structure

*   `app/`: The heart of the FastAPI application, managing API routes for authentication, document handling, and query processing.
*   `core/`: Essential functionalities including configuration, document indexing logic, and security.
*   `documents/`: Your personal knowledge hub – place your PDF and TXT documents here for indexing. (Ignored by Git)
*   `faiss_index/`: Where the magic happens! Stores the generated FAISS index for blazing-fast semantic searches. (Generated, Ignored by Git)
*   `frontend/`: The intuitive Next.js user interface that brings the system to life.
*   `prompts/`: Templates for the LLM prompts that guide the decision engine.
*   `utils/`: A toolkit of helper functions: document chunking, decision engine logic, file operations, Gemini API client, and semantic search utilities.
*   `config.ini`: Your personalized configuration file for API keys, paths, and settings. (Crucial for setup, Ignored by Git)
*   `requirements.txt`: All Python dependencies for the backend.
*   `package.json`: All Node.js dependencies for the frontend.

## 🚀 Getting Started

Follow these steps to get your Intelligent Query Retrieval System up and running in no time!

### Prerequisites

*   **Python 3.9+**
*   **Node.js (LTS recommended)** and **npm** or **Yarn**

### Backend Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/LLM-Powered-Intelligent-Query-Retrieval-System.git
    cd LLM-Powered-Intelligent-Query-Retrieval-System
    ```
    *(Remember to replace `https://github.com/your-username/LLM-Powered-Intelligent-Query-Retrieval-System.git` with the actual repository URL!)*

2.  **Set up your Python environment:**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Populate your knowledge base:**
    Drop your PDF and TXT documents into the `documents/` directory. These are your source materials for the system!

4.  **Generate FAISS Index & Document Chunks:**
    The `faiss_index/` and `data/sample_chunks/` directories are automatically generated during the indexing process. Run your main indexing script (e.g., `python main.py` or a dedicated indexing script) to create these essential components.

### Frontend Setup

1.  **Navigate to the frontend:**
    ```bash
    cd frontend
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    # or
    yarn install
    ```

3.  **Build the frontend application:**
    This step generates the `.next/` directory, preparing your UI for action.
    ```bash
    npm run build
    # or
    yarn build
    ```

### ⚙️ Configuration (Environment Variables)

**Crucial Step:** Configure your environment variables. This project uses environment variables for sensitive information like API keys and dynamic paths. These variables are intentionally not committed to version control.

*   **`GEMINI_API_KEY`**: Your Google Gemini API key.
*   **`DOCUMENTS_DIR`**: Path to your documents directory (e.g., `documents/`).
*   **`FAISS_INDEX_DIR`**: Path to your FAISS index directory (e.g., `faiss_index/`).
*   **`CHUNK_DATA_DIR`**: Path to your chunked data directory (e.g., `data/sample_chunks/`).

**How to set environment variables:**

**For Windows (Command Prompt):**
```bash
set GEMINI_API_KEY=YOUR_GEMINI_API_KEY
set DOCUMENTS_DIR=documents/
set FAISS_INDEX_DIR=faiss_index/
set CHUNK_DATA_DIR=data/sample_chunks/
```
**For Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
$env:DOCUMENTS_DIR="documents/"
$env:FAISS_INDEX_DIR="faiss_index/"
$env:CHUNK_DATA_DIR="data/sample_chunks/"
```
**For macOS/Linux:**
```bash
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
export DOCUMENTS_DIR="documents/"
export FAISS_INDEX_DIR="faiss_index/"
export CHUNK_DATA_DIR="data/sample_chunks/"
```

*   **Replace `YOUR_GEMINI_API_KEY`** with your actual Google Gemini API key.
*   **Verify paths:** Ensure `DOCUMENTS_DIR`, `FAISS_INDEX_DIR`, and `CHUNK_DATA_DIR` are correctly set relative to the project root.
*   For persistent environment variables, refer to your operating system's documentation.

## ▶️ Running the Application

### Start the Backend (API Server)

From the project root directory:

```bash
# Activate your virtual environment first if not already active
# On Windows: venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate

uvicorn app.main:app --reload --port 8000
```
Your FastAPI backend will be humming, typically accessible at `http://localhost:8000`.

### Start the Frontend (User Interface)

From the `frontend/` directory:

```bash
npm run dev
# or
yarn dev
```
Your Next.js frontend will launch, usually available at `http://localhost:3000`.

## ✅ Testing

*   **Backend Tests:** Dive into the Python tests using `pytest` (if configured).
*   **Frontend Tests:** Explore the frontend tests with `jest` or your preferred testing framework.

## 🤝 Contributing

We welcome your contributions! Please follow our standard Git workflow: fork the repository, create a new branch for your awesome features or bug fixes, and submit a pull request. Let's build something amazing together!

## 📄 License

This project is proudly licensed under the MIT License. See the `LICENSE` file for full details.

---

*Made with ❤️ by Your Name/Organization*