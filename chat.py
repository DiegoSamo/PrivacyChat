import tkinter as tk
from PIL import Image as PilImage, ImageTk, ImageDraw
from tkinter import *
from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from backports import configparser
from langchain_core.messages import HumanMessage,AIMessage
from langgraph.graph import END,START
from typing import List, Sequence, Union
from langchain_core.messages import BaseMessage,ToolMessage,HumanMessage
from langgraph.graph import END,MessageGraph,StateGraph,MessagesState
from schemas import MessagesState
from langgraph.checkpoint.memory import MemorySaver

slm=ChatOllama(model="qwen2.5:latest",num_ctx=1024,top_k=10,top_p=0.8,num_thread=7)
# Define a new graph/
workflow = StateGraph(state_schema=MessagesState)


# Define the function that calls the model
def call_model(state: MessagesState):
    response = slm.invoke(state["messages"])
    # Update message history with response:
    return {"messages": response}


# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "slmTest55"}}

# Función para enviar un mensaje al modelo de Ollama
def enviar_a_ollama(mensaje_usuario):
    # Petición a Ollama
    input_messages = [HumanMessage(mensaje_usuario)]
    output = app.invoke({"messages": input_messages}, config)
    return output["messages"][-1].content

# Simulación de la función que interactúa con la IA (Ollama)

# Función para manejar el envío del mensaje
def enviar_mensaje(event=None):
    mensaje_usuario = entrada.get("1.0", tk.END).strip()  # Obtener texto del cuadro de entrada
    if mensaje_usuario:
        habilitar_chat()
        chat.insert(tk.END, "Myself: ","myself")
        chat.insert(tk.END, f"{mensaje_usuario}\n\n")  # Mostrar el mensaje del usuario
        chat.config(state=tk.DISABLED)  # Bloquear área de chat

        # Enviar el mensaje al modelo de Ollama
        respuesta_modelo = enviar_a_ollama(mensaje_usuario)
        habilitar_chat()
        chat.insert(tk.END, "PrivacyChatOllama: ","chatbot")  # Mostrar la respuesta del modelo
        chat.insert(tk.END, f"{respuesta_modelo}\n\n")
        chat.config(state=tk.DISABLED)

        # Limpiar la entrada
        entrada.delete("1.0", tk.END)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("PrivacyChatOllama")
ventana.configure(bg="#383838")

# Marco para contener el área de chat y la barra de desplazamiento

# Área de chat (modo solo lectura) con barra de deslizamiento
chat = tk.Text(ventana, height=30, width=200, state=tk.DISABLED, wrap=tk.WORD,bg="#5A5A5A",fg="White")
chat.pack(pady=10)

# Configurar estilos de colores
chat.tag_configure("myself", foreground="green")  # Mensajes del usuario en verde
chat.tag_configure("chatbot", foreground="red")    # Respuestas del modelo en rojo

# Marco para la entrada de texto y el botón
frame_entrada = tk.Frame(ventana,bg="#5A5A5A")
frame_entrada.pack(pady=5)

# Caja de entrada de texto
entrada = tk.Text(frame_entrada, height=5, width=40, wrap=tk.WORD, bg="#5A5A5A", fg="White")
entrada.grid(row=0, column=0, padx=(0, 5))
entrada.bind("<Return>", enviar_mensaje) # Enviar con Enter

# Cargar y ajustar la imagen del botón
boton_imagen = PhotoImage(file="SendR.png")

# Botón dentro del área de entrada
boton_enviar = tk.Button(frame_entrada, image=boton_imagen, command=enviar_mensaje, borderwidth=0,bg="#5A5A5A", activebackground="White")
boton_enviar.grid(row=0, column=1)


# Habilitar el área de chat para agregar texto
def habilitar_chat():
    chat.config(state=tk.NORMAL)
    chat.see(tk.END)  # Desplazarse automáticamente al final

# Configurar para que "Shift + Enter" agregue nueva línea
def nueva_linea(event):
    entrada.insert(tk.INSERT, "\n")
    return "break"  # Evitar enviar el mensaje directamente

entrada.bind("<Shift-Return>", nueva_linea)

# Ejecutar la aplicación
ventana.mainloop()