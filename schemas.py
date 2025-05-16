from operator import add
from typing import Annotated,Tuple,Dict
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from pydantic import BaseModel,Field
from backports import configparser

configfile_name = "./config_files/prompts.ini"
configFile = configparser.ConfigParser()
configFile.read(configfile_name)

class MessagesState(TypedDict):
   state:str
   messages:Annotated[list[AnyMessage], add_messages]
   keywords:str
   chatMessages:Annotated[list[AnyMessage], add_messages]
   ollamaMessages:list[AnyMessage]
   report:dict[str, str]

def compareText(previousReport: dict[str, str], originalText: str, keywords: str, aleatorizedText: str) -> dict[str, str]:
    originalWords = originalText.split()
    aleatorizedWords = aleatorizedText.split()
    keywordsList = keywords.split(',')  # permite múltiples keywords separadas por coma
    differences = {}

    for keyword in keywordsList:
        keyword = keyword.strip()
        kw_parts = keyword.split()

        for i in range(len(originalWords) - len(kw_parts) + 1):
            if originalWords[i:i + len(kw_parts)] == kw_parts:
                # Encontramos la frase en el original, cogemos su equivalente del aleatorizado
                aleatorized_fragment = ' '.join(aleatorizedWords[i:i + len(kw_parts)])
                if keyword not in previousReport:
                    differences[keyword] = aleatorized_fragment
                break  # No seguimos buscando este keyword

    previousReport.update(differences)
    return previousReport


