from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage,AIMessage
from schemas import MessagesState,compareText
from chains import randomice_responder,chatgpt_responder,unrandomice_responder,randomice_prompt_template
from langgraph.graph import END,StateGraph
from presidioReconizer import Presidio


RECON="RecognitionAgent"
CHAT="ChatBotAgent"
RAMDOM="RandomizationAgent"


def recognition_node(state:MessagesState):
    onlymessage=state['messages'][-1]
    if state['state'] == RECON:
        res=Presidio.examine(onlymessage.content)
        return{
        "keywords":res 
        }
    else:
        return {
        "messages":onlymessage
        }


def random_node(state:MessagesState):
    onlyMessage=state['messages'][-1].content
    onlyKeywords=state.get("keywords","")
    if state['state']==RECON:
        reports=state.get("report",{})
        ollamaMessages=state.get("ollamaMessages",[])
        report=str(reports)
        if onlyKeywords != "":
            res=randomice_responder.invoke(input={"ollamaMessages":ollamaMessages,"infoToRandomice":onlyMessage,"PIITokens":onlyKeywords})
            ollamaMessages.append(randomice_prompt_template.invoke(input={"ollamaMessages":ollamaMessages,"infoToRandomice":onlyMessage,"PIITokens":onlyKeywords}).to_messages()[-1])
            ollamaMessages.append(res)

        else:
            res=HumanMessage(content=onlyMessage)
        reports=compareText(reports,onlyMessage,onlyKeywords,res.content)
        #ollamaMessages.append(AIMessage(content=res.tool_calls[0]["args"]["message"]))
        #addToDiccionary(reports,res.tool_calls[0]["args"]["data"],res.tool_calls[0]["args"]["aleatorizedData"])
        #"chatMessages":HumanMessage(content=res.tool_calls[0]["args"]["message"])
        return{"messages":res,
               "chatMessages":HumanMessage(content=res.content),
               "report":reports,
               "ollamaMessages":ollamaMessages}
    else:
        reports=state.get("report",{})
        report=', '.join(f'{value} -> {key}' for key,value in reports.items())
        res=unrandomice_responder.invoke(input={"infoToUnrandomice":onlyMessage,"report":report})
        return{"messages":res}


def chat_node(state:MessagesState):
    stateInNode=CHAT

    res=chatgpt_responder.invoke(input={"randomicedInfo":state['chatMessages']})
    return{"messages":res,
           "chatMessages":res,
           "state":stateInNode}

def recognition_pathFinder(state:MessagesState):
    if state['state']==CHAT:
        return END
    else:
        return RAMDOM

def ramdom_pathFinder(state:MessagesState):
    if state['state'] == RECON :
        return CHAT
    else:
        return RECON


