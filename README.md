# LLM-Powered Intelligent Query Retrieval System

This project implements an advanced Intelligent Query Retrieval System powered by Large Language Models (LLMs). It allows users to interact with a knowledge base of documents through natural language queries, leveraging semantic search and a decision engine to provide accurate and relevant responses.

## Features

*   **Intelligent Query Processing:** Utilizes LLMs to understand and process complex natural language queries.
*   **Semantic Search:** Employs FAISS for efficient semantic search over document embeddings, ensuring high relevance in retrieval.
*   **Document Indexing:** Supports indexing of various document types (e.g., PDF, TXT) into a searchable knowledge base.
*   **Decision Engine:** Integrates a decision engine to refine search results and provide precise answers.
*   **Scalable Architecture:** Built with FastAPI for the backend and Next.js for a responsive frontend.

## Project Structure

*   `app/`: Contains the FastAPI application, including API routes for authentication, document management, and query processing.
*   `core/`: Houses core functionalities such as configuration management, document indexing logic, and security utilities.
*   `documents/`: Placeholder for user-provided documents (PDFs, TXT files) that will be indexed.
*   `faiss_index/`: Stores the generated FAISS index for semantic search. This directory is created during the indexing process.
*   `frontend/`: The Next.js application providing the user interface for interaction with the system.
*   `prompts/`: Contains templates for LLM prompts used by the decision engine.
*   `utils/`: A collection of utility functions, including document chunking, decision engine logic, file operations, Gemini API client, and semantic search helpers.
*   `config.ini`: Configuration file for API keys, paths, and other settings. (See Configuration section)
*   `requirements.txt`: Python dependencies for the backend.
*   `package.json`: Node.js dependencies for the frontend.

## Setup and Installation

Follow these steps to set up and run the project locally.

### Prerequisites

*   **Python 3.9+**
*   **Node.js (LTS recommended)** and **npm** or **Yarn**

### Backend Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/LLM-Powered-Intelligent-Query-Retrieval-System.git
    cd LLM-Powered-Intelligent-Query-Retrieval-System
    ```
    *(Replace `https://github.com/your-username/LLM-Powered-Intelligent-Query-Retrieval-System.git` with the actual repository URL)*

2.  **Create a Python virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Prepare your documents:**
    Place your PDF and TXT documents into the `documents/` directory. These files are not tracked by Git and should be added by the user.

4.  **Generate FAISS Index and Document Chunks:**
    The `faiss_index/` directory and `data/sample_chunks/` are generated during the indexing process. You will need to run the indexing script (e.g., `python main.py` or a specific indexing script if available) to create these.

### Frontend Setup

1.  **Navigate to the frontend directory:**
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
    The `.next/` directory is generated during the build process.
    ```bash
    npm run build
    # or
    yarn build
    ```

### Configuration (`config.ini`)

Create a `config.ini` file in the root directory of the project. This file is excluded from version control and should contain your sensitive API keys and other local settings.

Example `config.ini`:

```ini
[GEMINI]
API_KEY = YOUR_GEMINI_API_KEY

[PATHS]
DOCUMENTS_DIR = documents/
FAISS_INDEX_DIR = faiss_index/
CHUNK_DATA_DIR = data/sample_chunks/
```

*   Replace `YOUR_GEMINI_API_KEY` with your actual Google Gemini API key.
*   Ensure the `DOCUMENTS_DIR`, `FAISS_INDEX_DIR`, and `CHUNK_DATA_DIR` paths are correct relative to the project root.

## Running the Application

### Start the Backend

From the project root directory (where `main.py` is located):

```bash
# Activate your virtual environment first if not already active
# On Windows: venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate

uvicorn app.main:app --reload --port 8000
```
This will start the FastAPI backend server, typically accessible at `http://localhost:8000`.

### Start the Frontend

From the `frontend/` directory:

```bash
npm run dev
# or
yarn dev
```
This will start the Next.js development server, typically accessible at `http://localhost:3000`.

## Testing

*   **Backend Tests:** Run Python tests using `pytest` (if configured).
*   **Frontend Tests:** Run frontend tests using `jest` or other configured testing frameworks.

## Contributing

Contributions are welcome! Please follow standard Git practices: fork the repository, create a new branch for your features or bug fixes, and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
