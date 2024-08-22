import os
import params
from dotenv import load_dotenv
from typing import Literal
from operator import itemgetter

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.passthrough import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from retriever import Retriever

# Load environment variables
load_dotenv()
path_pdf_reglamento_ue = os.path.join(os.getcwd(), "data", params.EU_AI_ACT_PDF)
path_pdf_politica_nacional_ia_chile = os.path.join(os.getcwd(), "data", params.POLITICA_NACIONAL_IA_PDF)
path_pdf_modelos_lenguaje = os.path.join(os.getcwd(), "data", params.PLAN_DE_ACCION_IA_PDF)
openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_API_KEY'] = openai_api_key


class Classifier(BaseModel):
    """Clasifica el tipo de interacción"""
    type: Literal["reglamento ue", "política nacional de ia de chile", "modelos de lenguaje"] = Field(description="Dada la interacción recibida, clasifica si se tratara de un pregunta sobre reglamento de la UE, política nacional de IA de Chile o modelos de lenguaje",)


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
        classification_result = self.structured_llm.invoke(prompt)
        classification_type = classification_result.type

        if classification_type not in self.retrievers:
            raise ValueError(f"Invalid classification type: {classification_type}")

        source = self.retrievers[classification_type].retrieve(prompt)

        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "Debes responder la pregunta del usuario utiliando el siguiente contexto. CONTEXTO: {source}"),
                ("human", "{question}"),
            ]
        )

        final_chain = (prompt_template | self.llm | StrOutputParser())

        return final_chain.invoke({"question": prompt, "source": source})


if __name__ == "__main__":

    chat_manager = ChatManager()

    while True:
        question = input("Pregunta: ")
        chat = chat_manager.generate(question)
        print(chat)
