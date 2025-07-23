# 🚀 LLM-Powered Intelligent Query Retrieval System

<p align="center">
  <img src="https://user-images.githubusercontent.com/89354109/236128015-5c01a7c6-2365-4245-a352-b0387c4e8444.png" alt="Project Banner" width="800">
</p>

## Unlock Your Data's Potential with Smart, Conversational AI!

This project introduces a cutting-edge **Intelligent Query Retrieval System** that transforms how you interact with your documents. Powered by advanced Large Language Models (LLMs), it enables natural language conversations with your knowledge base, delivering precise and contextually relevant answers through semantic search and a sophisticated decision engine.

---

## ✨ How It Works

The system follows a simple yet powerful workflow:

1.  **Indexing:** Documents in the `documents/` directory are processed, chunked, and converted into vector embeddings using a sentence transformer model. These embeddings are stored in a FAISS index for efficient similarity search.
2.  **Querying:** A user submits a query through the command-line interface or the web application.
3.  **Semantic Search:** The system searches the FAISS index to find the most relevant document chunks based on the query's semantic meaning.
4.  **Decision Engine:** The retrieved chunks and the original query are passed to a Large Language Model (LLM) with a specialized prompt. The LLM analyzes the context and generates a precise, human-readable answer.

---

## 🏗️ Project Structure

*   `app/`: The heart of the FastAPI application, managing API routes for authentication, document handling, and query processing.
*   `core/`: Essential functionalities including configuration, document indexing logic, and security.
*   `documents/`: Your personal knowledge hub – place your PDF and TXT documents here for indexing.
*   `faiss_index/`: Stores the generated FAISS index for blazing-fast semantic searches.
*   `frontend/`: The intuitive Next.js user interface that brings the system to life.
*   `prompts/`: Templates for the LLM prompts that guide the decision engine.
*   `utils/`: A toolkit of helper functions: document chunking, decision engine logic, file operations, Gemini API client, and semantic search utilities.
*   `config.ini`: Configuration file for paths and model settings.
*   `requirements.txt`: All Python dependencies for the backend.
*   `package.json`: All Node.js dependencies for the frontend.

---

## 🚀 Getting Started

Follow these steps to get your Intelligent Query Retrieval System up and running.

### Prerequisites

*   **Python 3.9+**
*   **Node.js (LTS recommended)** and **npm** or **Yarn**

### Backend Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Set up your Python environment:**
    ```bash
    python -m venv .venv
    # On Windows:
    .venv/Scripts/activate
    # On macOS/Linux:
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the project root and add the following variables. This file is ignored by Git to keep your secrets safe.

    ```env
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    GOOGLE_CLIENT_ID="YOUR_GOOGLE_CLIENT_ID"
    GOOGLE_CLIENT_SECRET="YOUR_GOOGLE_CLIENT_SECRET"
    GOOGLE_REDIRECT_URI="http://localhost:8000/auth/callback"
    SECRET_KEY="YOUR_SECRET_KEY"
    ```

    *   Replace the placeholder values with your actual credentials.
    *   The `SECRET_KEY` can be any long, random string.

4.  **Populate Your Knowledge Base:**
    Place your PDF and TXT documents into the `documents/` directory.

5.  **Generate FAISS Index:**
    Run the preprocessing script to index your documents:
    ```bash
    python preprocess.py
    ```

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

---

## ▶️ Running the Application

You can run this project as a command-line tool or as a full-stack web application.

### Command-Line Interface (CLI)

To interact with your documents directly from the terminal, run `main.py`:

```bash
python main.py
```

### Web Application

To launch the full web application, you need to start both the backend and frontend servers.

1.  **Start the Backend (API Server):**
    From the project root directory:
    ```bash
    uvicorn app.main:app --reload --port 8000
    ```

2.  **Start the Frontend (User Interface):**
    From the `frontend/` directory:
    ```bash
    npm run dev
    ```
    The application will be available at `http://localhost:3000`.

---

## ✅ Testing

*   **Backend Tests:** Run Python tests using `pytest`.
*   **Frontend Tests:** Run frontend tests using `npm test`.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository, create a new branch for your features or bug fixes, and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
