import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq

load_dotenv()

CHROMA_PATH = os.path.join(os.getcwd(), "chroma_db")
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def ingest_document(file_path: str):
    """PDF file ko read kar ke chunks ChromaDB me store karta hy."""
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    chunks = text_splitter.split_documents(docs)

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=CHROMA_PATH
    )
    return len(chunks)


def query_rag(question: str):
    """User ke question par context retrieve kar ke LLM se answer leta hy."""
    if not os.path.exists(CHROMA_PATH):
        return "Abhi koi training notes upload nahi huay."

    vector_db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_model
    )
    
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    relevant_docs = retriever.invoke(question)

    if not relevant_docs:
        return "Is topic ke related koi information notes mein nahi mili."

    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    llm = ChatGroq(
        model_name="openai/gpt-oss-20b",
        temperature=0.2,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    prompt = f"""You are an AI Academic Support Assistant for students.
Answer the question strictly using the provided context from the training notes. 
If the answer cannot be found in the context, politely say that the topic is not covered in the current notes.

Context:
{context}

Question: {question}

Answer:"""

    response = llm.invoke(prompt)
    return response.content