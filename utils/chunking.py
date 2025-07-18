import re

def recursive_chunk_text(text, max_chunk_size=1024, overlap=100):
    """
    Recursively splits text into chunks of a specified size, with overlap.
    Tries to split based on newlines and sentences.
    """
    chunks = []
    if len(text) <= max_chunk_size:
        return [text]

    # Try splitting by double newline, then single newline
    for separator in ["\n\n", "\n", ". ", "? ", "! ", " "]:
        splits = text.split(separator)
        if len(splits) > 1:
            break

    current_chunk = ""
    for i, split in enumerate(splits):
        if len(current_chunk) + len(split) + len(separator) > max_chunk_size:
            chunks.append(current_chunk.strip())
            # Add overlap
            current_chunk = current_chunk[-overlap:] + split + separator
        else:
            current_chunk += split + separator

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def simple_chunk_text(text, max_words=300):
    words = text.split()
    chunks = [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]
    return chunks
