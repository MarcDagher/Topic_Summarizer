# General
import datetime
from pathlib import Path
from dotenv import load_dotenv

# FastAPI
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# LangChain
from FastAPI_Helpers.agent import Agent
from langchain_groq import ChatGroq
from FastAPI_Helpers.prompts import searcher_prompt
from langchain_core.messages import HumanMessage
from langchain_community.tools import TavilySearchResults

#######################
# Prepare Environment #
#######################
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

#################
# Prepare Agent #
#################
model = ChatGroq(model="mixtral-8x7b-32768", temperature=0.2)
tavily_search_client = TavilySearchResults(max_results=5)
agent = Agent(model=model, tools=[tavily_search_client], system_prompt=searcher_prompt.format(todays_date=str(datetime.datetime.now().date())))

# Function to send a message to groq and recive its outputs
def send_user_message(user_message):
    config = {"configurable": {"thread_id": "1"}}
    response = []
    for event in agent.graph.stream({"conversation": [HumanMessage(content=str(user_message))]}, config, stream_mode="values"):
        response.append(event["conversation"][-1])
    
    state = agent.graph.get_state(config=config).values
    return {"response": response,}

###############
# Prepare API #
###############
app = FastAPI()

class Message(BaseModel):
  message: str

@app.post("/conversation/")
def call_agent(request: Message):
    try:
        user_message = HumanMessage(content=request.message)
        ai_response = send_user_message(user_message)
        return ai_response
    except Exception as e:
        
        print("-----------------")
        print(e)
        print("-----------------")
        if e.response.status_code == 400: return "Failed to call the function due to your bad prompt"
        elif e.response.status_code == 422: return "Unprocessable Entry"
        elif e.response.status_code == 429: return "Rate limit reached for model"
        elif e.response.status_code == 500: return "Internal Server Error"
        elif e.response.status_code == 503: return "Internal Server Error"

# Only run this if the script is executed directly (not inside a notebook or interactive shell)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)