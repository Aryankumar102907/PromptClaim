import docx
import logging
from pathlib import Path
from io import StringIO

# For PDFMiner.six
from pdfminer.high_level import extract_text as pdfminer_extract_text
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

# Configure logging for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logger.addHandler(handler)

def extract_text_from_pdf(path):
    """Extracts text from a PDF file using pdfminer.six."""
    try:
        # Using pdfminer.high_level.extract_text for simplicity and robustness
        text = pdfminer_extract_text(path)
        if not text.strip():
            logger.warning(f"No text extracted from PDF: {path}. It might be an image-based PDF or empty.")
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF {path} using pdfminer.six: {e}")
        return ""

def extract_text_from_docx(path):
    """Extracts text from a DOCX file."""
    try:
        doc = docx.Document(path)
        text = "\n".join([para.text for para in doc.paragraphs])
        if not text:
            logger.warning(f"No text extracted from DOCX: {path}. It might be empty.")
        return text
    except Exception as e:
        logger.error(f"Error extracting text from DOCX {path}: {e}")
        return ""

def extract_text_from_txt(path):
    """Extracts text from a TXT file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
            if not text:
                logger.warning(f"TXT file is empty: {path}.")
            return text
    except Exception as e:
        logger.error(f"Error reading TXT file {path}: {e}")
        return ""

def extract_text_from_document(file_path):
    """
    Detects the file type and extracts text accordingly.
    Supports PDF, DOCX, and TXT.
    """
    path = Path(file_path)
    if not path.exists():
        logger.error(f"File not found: {file_path}")
        return ""

    if path.suffix.lower() == '.pdf':
        return extract_text_from_pdf(file_path)
    elif path.suffix.lower() == '.docx':
        return extract_text_from_docx(file_path)
    elif path.suffix.lower() == '.txt':
        return extract_text_from_txt(file_path)
    else:
        logger.warning(f"Unsupported file type for extraction: {path.suffix} for file {file_path}")
        return ""