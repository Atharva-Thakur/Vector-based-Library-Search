import os
import glob
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import unicodedata

def clean_text(text):
    """Normalize and clean text to remove encoding issues."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)  # Normalize Unicode
    text = text.encode("utf-8", "ignore").decode("utf-8")  # Remove non-UTF-8 characters
    return text

def extract_text_from_pdf(pdf_path):
    """Extract and clean text from PDFs."""
    if not os.path.isfile(pdf_path):
        print(f"⚠️ Error: '{pdf_path}' is not a valid file.")
        return ""

    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text("text") for page in doc if page.get_text("text")])
        text = clean_text(text)  # Clean encoding issues
        if text.strip():
            return text.strip()
    except Exception as e:
        print(f"⚠️ PyMuPDF failed for {pdf_path}: {e}")

    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages if page.extract_text()])
        text = clean_text(text)  # Clean encoding issues
        return text.strip()
    except Exception as e:
        print(f"⚠️ pdfplumber also failed for {pdf_path}: {e}")

    return ""  # Return empty string if both methods fail


def save_faiss_db(db, file_path):
    """Save the FAISS index to disk using LangChain's method."""
    try:
        db.save_local(file_path)  # LangChain's save method
        print(f"✅ FAISS index saved at: {file_path}")
    except Exception as e:
        print(f"❌ Error saving FAISS index: {str(e)}")


def process_pdfs_in_directory(directory, output_dir):
    """Process all PDFs in the directory, create FAISS DBs, and save them."""

    if not os.path.exists(directory) or not os.path.isdir(directory):
        print(f"⚠️ Error: Directory '{directory}' does not exist or is inaccessible.")
        return

    pdf_files = glob.glob(os.path.join(directory, "*.pdf"))

    if not pdf_files:
        print(f"⚠️ No PDF files found in {directory}.")
        return

    for pdf_file in pdf_files:
        pdf_name = os.path.splitext(os.path.basename(pdf_file))[0]  # Extract filename without extension
        print(f"📄 Processing: {pdf_file}...")

        # Extract text
        document_text = extract_text_from_pdf(pdf_file)
        if not document_text:
            print(f"⚠️ No valid text extracted from {pdf_file}. Skipping...")
            continue

        metadata = {
            "source": pdf_file,
            "grade": 9,  # Store role as a list for flexibility
            "topic": pdf_name,
        }

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformer/bge-m3")

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, add_start_index=True)
        texts = text_splitter.split_text(document_text)

        # Convert texts into LangChain `Document` format with metadata
        documents = [Document(page_content=text, metadata=metadata) for text in texts]

        # Generate embeddings with metadata
        db = FAISS.from_documents(documents, embeddings)

        # Save the FAISS index for each PDF
        index_file_path = os.path.join(output_dir, pdf_name)
        os.makedirs(index_file_path, exist_ok=True)  # Ensure directory exists
        save_faiss_db(db, index_file_path)



if __name__ == "__main__":
    pdf_directory = "./dataset"  # Path to PDF folder
    vectorstore_root = "./vectorstores"  # Path to save FAISS indexes
    os.makedirs(vectorstore_root, exist_ok=True)  # Ensure root output directory exists

    process_pdfs_in_directory(pdf_directory, vectorstore_root)