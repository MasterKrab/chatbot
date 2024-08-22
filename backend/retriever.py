import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter


class Retriever():
    instances = 0

    def __init__(self, path_pdf: str):
        Retriever.instances += 1
        print(f"Loading PDF and generating retriever...  [{Retriever.instances}/3]")
        self.load_pdf(path_pdf)
        self.generate_docs_and_split()
        self.generate_embeddings()
        self.generate_vectorstore()
        self.generate_retriever()

    def load_pdf(self, path_pdf: str):
        self.loader = PyPDFLoader(path_pdf)
        self.documents = self.loader.load()

    def generate_docs_and_split(self):
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        self.texts = text_splitter.split_documents(self.documents)

    def generate_embeddings(self):
        self.embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_vectorstore(self):
        self.vectorstore = FAISS.from_documents(self.texts, self.embeddings)

    def generate_retriever(self):
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

    def retrieve(self, query: str) -> str:
        results = self.retriever.invoke(query)
        return results
