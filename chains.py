from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from backports import configparser




configfile_name = "./config_files/prompts.ini"

configFile = configparser.ConfigParser()
configFile.read(configfile_name)


llm = ChatOpenAI(model="gpt-4o")
slm = ChatOllama(model="qwen2.5:latest"
                 ,num_thread=8
                 ,num_ctx=8192
                 ,lazy=False
                 ,temperature=0.6
                 ,top_p=0.9
                 ,disable_streaming=True
                 ,verbose=False
                 ,return_log_probs=False
                 ,output_attentions=False)



randomPrompt=[]
for option in configFile.options("Random"):
    if "placeholder" in option:
        randomPrompt.append(MessagesPlaceholder(variable_name=configFile.get("Random",option)))
    if "system" in option:
        randomPrompt.append(("system",configFile.get("Random",option)))
    if "human" in option:
        randomPrompt.append(("human",configFile.get("Random",option)))
randomice_prompt_template = ChatPromptTemplate.from_messages(randomPrompt)

unrandomPrompt=[]
for option in configFile.options("Unrandom"):
    if "placeholder" in option:
        unrandomPrompt.append(MessagesPlaceholder(variable_name=configFile.get("Unrandom",option)))
    if "system" in option:
        unrandomPrompt.append(("system",configFile.get("Unrandom",option)))
    if "human" in option:
        unrandomPrompt.append(("human",configFile.get("Unrandom",option)))
unrandomice_prompt_template = ChatPromptTemplate.from_messages(unrandomPrompt)


chatPrompt=[]
for option in configFile.options("Chat"):
    if "system" in option:
        chatPrompt.append(Systcontent=configFile.get("Chat",option))
    if "placeholder" in option:
        chatPrompt.append(MessagesPlaceholder(variable_name=configFile.get("Chat",option)))

chatgpt_prompt_template =ChatPromptTemplate.from_messages(chatPrompt)


randomice_responder = randomice_prompt_template | slm

unrandomice_responder = unrandomice_prompt_template | slm

chatgpt_responder=chatgpt_prompt_template | llm


