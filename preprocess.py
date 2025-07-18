import os
import pickle
from pathlib import Path
import logging
import configparser

# Try importing necessary libraries and provide user-friendly messages if they are missing
try:
    from utils.file_ops import extract_text_from_document
except ImportError:
    print("Error: Could not import 'extract_text_from_document'. Make sure utils/file_ops.py is accessible.")
    exit(1)

try:
    from utils.chunking import recursive_chunk_text
except ImportError:
    print("Error: Could not import 'recursive_chunk_text'. Make sure utils/chunking.py is accessible.")
    exit(1)

try:
    from utils.semantic_search import build_faiss_index
except ImportError:
    print("Error: Could not import 'build_faiss_index'. Make sure utils/semantic_search.py is accessible.")
    exit(1)

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Configure logging
LOG_LEVEL = config.get('LOGGING', 'LOG_LEVEL', fallback='INFO').upper()
LOG_FILE = config.get('LOGGING', 'LOG_FILE', fallback='preprocess.log')

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

DOCUMENTS_DIR = config.get('PATHS', 'DOCUMENTS_DIR', fallback='documents/')
INDEX_DIR = config.get('PATHS', 'INDEX_DIR', fallback='faiss_index')
SENTENCE_TRANSFORMER_MODEL = config.get('MODEL', 'SENTENCE_TRANSFORMER_MODEL', fallback='all-MiniLM-L6-v2')
MAX_CHUNK_SIZE = config.getint('CHUNKING', 'MAX_CHUNK_SIZE', fallback=1024)
OVERLAP = config.getint('CHUNKING', 'OVERLAP', fallback=100)

def preprocess_and_save_index():
    """
    Processes all supported documents (.pdf, .docx, .txt), creates a unified 
    FAISS index, and saves the index and chunk data to disk.
    """
    all_chunks_text = []
    chunk_metadata = []

    logger.info("Starting document preprocessing...")

    # Create the index directory if it doesn't exist
    os.makedirs(INDEX_DIR, exist_ok=True)

    # Define supported file types
    supported_extensions = ["*.pdf", "*.docx", "*.txt"]

    # Loop through each document in the folder
    logger.info(f"Searching for documents in: {Path(DOCUMENTS_DIR).resolve()}")
    
    doc_files = []
    for ext in supported_extensions:
        doc_files.extend(Path(DOCUMENTS_DIR).glob(ext))

    if not doc_files:
        logger.warning("No documents found in the 'documents' directory. Please add your files.")
        return

    for doc_file in doc_files:
        logger.info(f"Processing {doc_file.name}...")
        text = extract_text_from_document(str(doc_file))
        
        if not text:
            logger.warning(f"Skipping {doc_file.name} due to empty or failed text extraction.")
            continue

        try:
            # Pass chunking parameters from config
            chunks = recursive_chunk_text(text, max_chunk_size=MAX_CHUNK_SIZE, overlap=OVERLAP)
            
            if not chunks:
                logger.warning(f"No chunks generated for {doc_file.name}. Skipping.")
                continue

            for chunk in chunks:
                all_chunks_text.append(chunk)
                chunk_metadata.append({"source": doc_file.name})
        except Exception as e:
            logger.error(f"Error chunking text from {doc_file.name}: {e}")


    if not all_chunks_text:
        logger.error("No text could be extracted or chunked from any documents. Aborting.")
        return

    logger.info("\nBuilding FAISS index for all documents...")
    # Build a unified semantic search index
    try:
        # Pass model name from config
        model, index, embeddings = build_faiss_index(all_chunks_text, model_name=SENTENCE_TRANSFORMER_MODEL)
    except Exception as e:
        logger.error(f"Error building FAISS index: {e}")
        return

    # Save the FAISS index and the chunks
    index_path = os.path.join(INDEX_DIR, "faiss_index.bin")
    chunks_path = os.path.join(INDEX_DIR, "chunks.pkl")

    try:
        with open(index_path, "wb") as f:
            pickle.dump(index, f)

        with open(chunks_path, "wb") as f:
            pickle.dump({"texts": all_chunks_text, "metadata": chunk_metadata}, f)

        logger.info(f"FAISS index saved to {index_path}")
        logger.info(f"Chunks data saved to {chunks_path}")
        logger.info("Preprocessing complete.")
    except Exception as e:
        logger.error(f"Error saving FAISS index or chunks data: {e}")

if __name__ == "__main__":
    preprocess_and_save_index()

