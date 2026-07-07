from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

retriever = None
vector_db = None
embedding_model = None

BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "chroma_db"

def load_pdf(pdf_path: str | Path):
    loader = PyPDFLoader(str(pdf_path))
    return loader.load()

def split_documents(documents: list):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    return splitter.split_documents(documents)

def create_embedding_model():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def create_vector_database(chunks, embedding_model):

    return Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=str(CHROMA_DIR)
    )

def initialize_rag(pdf_path, k=3):

    global retriever
    global vector_db
    global embedding_model

    if retriever is not None:
        return
    
    try:
        documents = load_pdf(pdf_path)
    except Exception as e:
       raise RuntimeError(
        f"Failed to initialize RAG: {e}"
    )

    chunks = split_documents(documents)

    embedding_model = create_embedding_model()

    vector_db = create_vector_database(
        chunks,
        embedding_model
    )

    retriever = vector_db.as_retriever(
    search_kwargs={"k": k}
    )

    print("RAG initialized successfully.")

def retrieve_context(query):

    if retriever is None:
        raise RuntimeError(
            "RAG has not been initialized."
        )

    docs = retriever.invoke(query)

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )

if __name__ == "__main__":

    PDF_PATH = (
        BASE_DIR
        / "data"
        / "Module 2_Technical Analysis.pdf"
    )

    initialize_rag(PDF_PATH)

    print(retrieve_context("RSI above 70"))