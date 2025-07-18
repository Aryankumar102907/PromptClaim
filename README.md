# 🚀 LLM-Powered Intelligent Query Retrieval System

## ✨ Unveiling the Future of Document Interaction

Welcome to the **LLM-Powered Intelligent Query Retrieval System**, a groundbreaking application designed to revolutionize how you interact with complex policy documents. This system doesn't just search; it *understands*, *reasons*, and *decides*, providing intelligent answers to your nuanced queries. Built with cutting-edge Large Language Models (LLMs) and advanced semantic search capabilities, this project stands as a testament to the power of AI in transforming information retrieval.

## 🌟 Why This System is Special: A Deep Dive into its Brilliance

This isn't just another search engine. Our system is engineered for unparalleled intelligence and efficiency, boasting several key specialities:

*   **🧠 LLM-Powered Dynamic Decision Making**: At its core, the system leverages the formidable reasoning capabilities of Google's Gemini LLM. It doesn't merely extract keywords; it comprehends the context of your query, cross-references it with relevant document clauses, and makes informed decisions (e.g., "Approved," "Rejected") along with detailed justifications. This goes far beyond traditional information retrieval, offering actionable insights.
*   **🔍 Semantic Search Prowess**: Forget rigid keyword matching. Our system employs state-of-the-art Sentence Transformers and FAISS indexing to perform highly accurate semantic searches. This means your queries are understood based on their meaning, not just literal words, leading to remarkably precise and contextually relevant results, even for complex or ambiguously phrased questions.
*   **🧩 Modular and Scalable Architecture**: Designed with FastAPI for the backend and Next.js for the frontend, the system features a clean, modular architecture. This ensures high performance, easy maintainability, and seamless scalability, allowing for future enhancements and integration with other services.
*   **📄 Intelligent Document Processing**: The system intelligently processes various document types (PDF, DOCX, TXT), extracting text and segmenting it into semantically coherent chunks. This preprocessing step is crucial for effective semantic indexing and ensures that the LLM receives optimal context for its reasoning.
*   **⚡ Real-time Indexing and Updates**: Documents can be uploaded and deleted dynamically via the API. The system automatically re-indexes the relevant data in real-time, ensuring that your knowledge base is always up-to-date without manual intervention.
*   **🔒 Secure and Robust**: With integrated Google OAuth2 for authentication and JWT for secure API access, the system prioritizes data security and user privacy.
*   **🧪 Testable and Verifiable Logic**: The core decision-making logic is encapsulated and testable, as demonstrated by the `check_accuracy.py` script. This commitment to verifiable outcomes ensures reliability and allows for continuous improvement of the system's intelligence.

This system is more than a tool; it's an intelligent assistant that empowers users to navigate and understand vast amounts of information with unprecedented ease and accuracy.

## 🛠️ Technologies Used

### Backend
*   **Python**: The core language for all backend logic.
*   **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
*   **Sentence Transformers**: For generating semantic embeddings from text.
*   **FAISS**: A library for efficient similarity search and clustering of dense vectors.
*   **Google Generative AI (Gemini API)**: For the Large Language Model capabilities.
*   **python-dotenv**: For managing environment variables.
*   **python-jose**: For JWT (JSON Web Tokens) handling.
*   **httpx**: A fully featured HTTP client for Python.
*   **python-docx**: For reading `.docx` files.
*   **pdfminer.six**: For extracting text from PDF files.

### Frontend
*   **Next.js**: A React framework for building performant web applications.
*   **React**: A JavaScript library for building user interfaces.
*   **Tailwind CSS**: A utility-first CSS framework for rapid UI development.
*   **Shadcn/ui**: Reusable components built using Radix UI and Tailwind CSS.

## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

*   Python 3.9+
*   Node.js (LTS version recommended)
*   npm or yarn

### 1. Clone the Repository

First, clone the repository to your local machine using Git and navigate into the project directory:

```bash
git clone https://github.com/your-username/LLM-Powered-Intelligent-Query-Retrieval-System.git
cd LLM-Powered-Intelligent-Query-Retrieval-System
```

### 2. Backend Setup

#### 2.1. Create and Activate Virtual Environment

It is recommended to create a Python virtual environment to manage dependencies and avoid conflicts with other projects.

```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

#### 2.2. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

#### 2.3. Configure Environment Variables

Create a `.env` file in the root directory of the project (`LLM-Powered-Intelligent-Query-Retrieval-System/.env`) and add the following. These environment variables are crucial for the application to function correctly, especially for API key management and Google OAuth2 authentication:

```
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
GOOGLE_CLIENT_ID="YOUR_GOOGLE_CLIENT_ID"
GOOGLE_CLIENT_SECRET="YOUR_GOOGLE_CLIENT_SECRET"
GOOGLE_REDIRECT_URI="http://localhost:8000/auth/google/callback"
SECRET_KEY="YOUR_SUPER_SECRET_KEY_FOR_JWT"
```
*   **`GEMINI_API_KEY`**: Obtain this from the Google AI Studio.
*   **`GOOGLE_CLIENT_ID`**, **`GOOGLE_CLIENT_SECRET`**, **`GOOGLE_REDIRECT_URI`**: Set up a new OAuth 2.0 Client ID in the Google Cloud Console. Ensure `http://localhost:8000/auth/google/callback` is added as an authorized redirect URI.
*   **`SECRET_KEY`**: A strong, random string used for signing JWT tokens. You can generate one using Python:
    ```python
    import os
    import secrets
    print(secrets.token_urlsafe(32))
    ```

#### 2.4. Prepare Documents and Build FAISS Index

Place your policy documents (PDF, DOCX, TXT) into the `documents/` directory. Then, run the preprocessing script to build the FAISS index. This script extracts text from the documents, chunks them into smaller, semantically coherent pieces, and creates a FAISS index for efficient semantic search.

```bash
python preprocess.py
```
This step is crucial as it extracts text, chunks documents, and creates the semantic search index.

#### 2.5. Run the Backend Server

This command starts the FastAPI backend server, making the API accessible for the frontend and other clients.
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
The backend API will be accessible at `http://localhost:8000`.

### 3. Frontend Setup

#### 3.1. Navigate to the Frontend Directory

Change your current directory to the `frontend` folder:

```bash
cd frontend
```

#### 3.2. Install Dependencies

Install the necessary Node.js packages for the frontend:

```bash
npm install
# or
yarn install
```

#### 3.3. Run the Frontend Development Server

This command starts the Next.js development server, allowing you to access the frontend application.
```bash
npm run dev
# or
yarn dev
```
The frontend application will be accessible at `http://localhost:3000`.

### 4. Running Both Backend and Frontend Concurrently

To run both the backend and frontend simultaneously, open two separate terminal windows:

**Terminal 1 (for Backend):**
```bash
cd LLM-Powered-Intelligent-Query-Retrieval-System
.\venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 (for Frontend):**
```bash
cd LLM-Powered-Intelligent-Query-Retrieval-System/frontend
npm run dev  # or yarn dev
```

This setup allows the frontend to communicate with the backend API, providing a complete local development environment.

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, pull requests, or suggest improvements.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.