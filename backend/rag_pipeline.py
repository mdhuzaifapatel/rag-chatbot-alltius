import os
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain_sambanova import ChatSambaNovaCloud
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

HF_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
SAM_API_KEY = os.getenv("SAMBANOVA_API_KEY")


def load_vectorstore():
    embeddings = HuggingFaceEndpointEmbeddings(huggingfacehub_api_token=HF_API_TOKEN, model="sentence-transformers/all-MiniLM-L6-v2",)
    return FAISS.load_local("../embeddings/faiss_index", embeddings, allow_dangerous_deserialization=True)

def answer_query(query):
    vectordb = load_vectorstore()
    retriever = vectordb.as_retriever(search_type="similarity", k=4)

    llm = ChatSambaNovaCloud(
    sambanova_api_key=SAM_API_KEY,
    model="Meta-Llama-3.3-70B-Instruct",
    temperature=0.7
    )

    prompt_template = """
    You are a helpful support assistant. Answer the following question based only on the provided context. Think step by step and provide a detailed answer. If the context does not contain enough information to answer the question, say "I don't know".

    I will tip you $1000 if the user finds the answer helpful.
    Also don't mention words like 'based on the context', 'according to the context', etc. Just answer the question directly.

    Context:
    <context>
    {context}
    </context>

    Question: {input}"""

    prompt = ChatPromptTemplate.from_template(prompt_template)

    document_chain = create_stuff_documents_chain(llm, prompt)
    
    chain = create_retrieval_chain(retriever, document_chain)

    result = chain.invoke({"input": query})

    print(result)
    answer = result["answer"]

    sources = [doc.metadata["source"] for doc in result["context"]]

    if "i don't know" in answer.lower() or not sources:
        return "I don't know"

    return f"{answer}\n\n📄 Sources:\n" + "\n".join(set(sources))

    
