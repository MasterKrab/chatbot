import os
from dotenv import load_dotenv
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.passthrough import RunnablePassthrough
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.pydantic_v1 import BaseModel, Field

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

# Load environment variables
load_dotenv()
path_pdf_reglamento_ue = os.path.join(os.getcwd(), "data", "EU-AI-Act-2024-Spanish.pdf")
path_pdf_politica_nacional_ia_chile = os.path.join(os.getcwd(), "data", "Política Nacional de IA Actualizada-2-05.pdf")
path_pdf_modelos_lenguaje = os.path.join(os.getcwd(), "data", "Doc Plan de Acción Politica IA 2024-25-06.pdf")
openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_API_KEY'] = openai_api_key


# Define the ChatManager class
class ChatManager():
    def __init__(self, llm = ChatOpenAI(model="gpt-3.5-turbo")):
        self.llm = llm
        self.structured_llm = llm.with_structured_output(Classifier)
        self.retrievers = {
            "reglamento ue": Retriever(path_pdf_reglamento_ue),
            "política nacional de ia de chile": Retriever(path_pdf_politica_nacional_ia_chile),
            "modelos de lenguaje": Retriever(path_pdf_modelos_lenguaje)
        }

    def generate(self, prompt: str) -> str:

        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "Debes responder la pregunta del usuario utiliando el siguiente contexto. CONTEXTO: {context}"),
                ("human", "{question}"),
            ]
        )

        final_chain = (
            RunnablePassthrough.assign(classification=(itemgetter("question") | self.structured_llm))
            | RunnablePassthrough.assign(
                context=lambda x: self.retrievers[x['classification'].type].retrieve(x['question']),
                output_text=lambda x: f"context: {x['context']} question: {x['question']}"
            )
            | RunnablePassthrough.assign(chain=(prompt_template | self.llm | StrOutputParser()))
        )

        return final_chain.invoke({"question": prompt})


# Define the Retriever class
class Retriever():
    def __init__(self, path_pdf: str):
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

class Classifier(BaseModel):
    """Clasifica el tipo de interacción"""
    type: Literal["reglamento ue", "política nacional de ia de chile", "modelos de lenguaje"] = Field(description="Dada la interacción recibida, clasifica si se tratara de un pregunta sobre reglamento de la UE, política nacional de IA de Chile o modelos de lenguaje",)


if __name__ == "__main__":

    # retriever_reglamento_ue = Retriever(path_pdf_reglamento_ue)
    # retriever_politica_nacional_ia_chile = Retriever(path_pdf_politica_nacional_ia_chile)
    # retriever_modelos_lenguaje = Retriever(path_pdf_modelos_lenguaje)

    chat_manager = ChatManager()

    chat1 = chat_manager.generate("¿Qué es el reglamento de la UE?")
    chat2 = chat_manager.generate("¿Cuál es la política nacional de IA de Chile?")
    chat3 = chat_manager.generate("¿Qué son los modelos de lenguaje?")

    print(chat1)
    print(chat2)
    print(chat3)
