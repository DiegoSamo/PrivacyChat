from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph
from schemas import MessagesState
from backports import configparser
from langgraph.checkpoint.memory import MemorySaver
from nodes import chat_node,random_node,ramdom_pathFinder,recognition_node,recognition_pathFinder,RECON,RAMDOM,CHAT

builder=StateGraph(MessagesState)
builder.add_node(RECON,recognition_node)
builder.add_node(RAMDOM,random_node)
builder.add_node(CHAT,chat_node)
builder.add_conditional_edges(RECON,recognition_pathFinder)
builder.add_conditional_edges(RAMDOM,ramdom_pathFinder)
builder.add_edge(CHAT,RAMDOM)
builder.set_entry_point(RECON)


test_memory=True
testTo="test1"
num_iterations = 30
exit_folder="salidaTestSLMMemory.txt"

configfile_name = "./config_files/test.ini"
configFile = configparser.ConfigParser()
with open(configfile_name, encoding='utf-8') as configfilename:
    configFile.read_file(configfilename)

if test_memory is True:
    memory = MemorySaver()
    graph=builder.compile(checkpointer=memory)
    config = {"configurable": {"thread_id": "Memory81"}}
else:
    graph=builder.compile()


initMessage=HumanMessage(content="")
with open(exit_folder, "a", encoding="utf-8") as file:
    file.write("Prueba de Rendimiento del SLM Qwen2.5 test Memoria."+"\n")
    #file.write(f"Mensaje con el que se realiza la pueba: {initMessage.content}" + "\n\n")

if __name__ == "__main__":

    for i in range(num_iterations):
        if test_memory is True:
            initMessage=HumanMessage(content=configFile.get(testTo,f"prompt{i+1}"))
            output=graph.invoke({"messages":[initMessage],"state":RECON},config=config)
        else:
            #initMessage.content="Hola me llamo Diego"
            #initMessage.content="Hola me llamo Diego y quiero organizar un viaje a mi novia que se llama Patricia, gano 1000€ al mes y me gustaria saber si me puedes enviar la informacion a mi correo diegoxanchez@gmail.com y a mi numero de telefono 608400177"
            initMessage=HumanMessage(content=configFile.get(testTo,f"prompt{i+1}"))
            output=graph.invoke({"messages":[initMessage],"state":RECON})

        mensaje=f"Iteracion {i+1}:\n Mensaje de entrada:{initMessage.content} || \n Salida Aleatorizacion:{output["messages"][-3].content} || \n Salida del ChatBot:{output["messages"][-2].content} || \n Salida Desaleatorizacion:{output["messages"][-1].content}"
        print(mensaje)
        with open(exit_folder, "a", encoding="utf-8") as file:
            file.write(mensaje + "\n")
