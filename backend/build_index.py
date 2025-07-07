import os
import json
import fitz 
import requests
from bs4 import BeautifulSoup
import docx
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from dotenv import load_dotenv
load_dotenv()

PDF_DIR = "./data/pdfs"
WEB_BASE_URL = "https://www.angelone.in/support"
PDF_JSON_OUTPUT = "./data/pdfs/insurance_docs.json"
WEB_JSON_OUTPUT = "./data/web_pages/support_data.json"
VECTOR_STORE_PATH = "./embeddings/faiss_index"

HF_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
SAM_API_KEY = os.getenv("SAMBANOVA_API_KEY")

def extract_pdfs():
    output = []
    for file in os.listdir(PDF_DIR):
        if file.endswith(".pdf"):
            doc = fitz.open(os.path.join(PDF_DIR, file))
            text = "\n".join([page.get_text() for page in doc])
            output.append({
                "source": file,
                "content": text
            })
        
        if file.endswith(".docx"):
            doc = docx.Document(os.path.join(PDF_DIR, file))
            text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            output.append({
                "source": file,
                "content": text
            })

    os.makedirs(os.path.dirname(PDF_JSON_OUTPUT), exist_ok=True)

    with open(PDF_JSON_OUTPUT, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Extracted and saved {len(output)} PDFs to {PDF_JSON_OUTPUT}")


def scrape_webpages():
    visited = set()
    pages = []

    def scrape(url):
        if url in visited or not url.startswith(WEB_BASE_URL):
            return
        try:
            resp = requests.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            pages.append({"url": url, "text": text})
            visited.add(url)
            for a in soup.find_all("a", href=True):
                href = a['href']
                if href.startswith("/support"):
                    scrape(WEB_BASE_URL + href[len("/support"):])
                elif href.startswith(WEB_BASE_URL):
                    scrape(href)
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    scrape(WEB_BASE_URL)

    os.makedirs(os.path.dirname(WEB_JSON_OUTPUT), exist_ok=True)
    with open(WEB_JSON_OUTPUT, "w") as f:
        json.dump(pages, f, indent=2)

    print(f"Scraped and saved {len(pages)} web pages to {WEB_JSON_OUTPUT}")


def delete_existing_files_or_index(directory_path):
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                except OSError as e:
                    print(f"Error deleting {file_path}: {e}")


def load_documents():
    all_docs = []

    for path in [WEB_JSON_OUTPUT, PDF_JSON_OUTPUT]:
        with open(path, "r") as f:
            data = json.load(f)
            for entry in data:
                all_docs.append({
                    "text": entry["text"] if "text" in entry else entry["content"],
                    "metadata": {"source": entry.get("url") or entry.get("source")}
                })

    return all_docs


def split_docs(docs):
    texts = [doc["text"] for doc in docs]
    metadatas = [doc["metadata"] for doc in docs]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    chunks = splitter.create_documents(texts, metadatas=metadatas)
    return chunks


def create_faiss_vectorstore(chunks):
    embeddings = HuggingFaceEndpointEmbeddings(huggingfacehub_api_token=HF_API_TOKEN, model="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(chunks, embedding=embeddings)

    os.makedirs(os.path.dirname(VECTOR_STORE_PATH), exist_ok=True)
    delete_existing_files_or_index(VECTOR_STORE_PATH)
    vectordb.save_local(VECTOR_STORE_PATH)


def build_index():
    try:
        extract_pdfs()
        scrape_webpages()
        docs = load_documents()
        chunks = split_docs(docs)
        create_faiss_vectorstore(chunks)
        return "FAISS Index created successfully."

    except Exception as e:
        print(f"Error while building index: {str(e)}")
        return "Error while building index."
