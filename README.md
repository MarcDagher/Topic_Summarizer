<h1 align="center">Topic Summarizer</h1>

<h3>🎯Aim</h3>
The aim of this repo is to build a system that is knowledgable of current day events, allowing users to interact with it and ask about any topic at any time.

<h3>🛠️Tools Used</h3>
To build this system I used LangGraph, Groq, Taivly, FastAPI, and Streamlit.

🕸️[LangGraph](https://www.langchain.com/langgraph) allows the organization of the agents workflow in a graphical manner, where each task is represented as a node and the possible paths to take are represented as edges. In my case, I had only two nodes (other than _end_ and _start_), LLM and ToolBox.

The LLM I used was 🤖<strong>"llama3-70b-8192"</strong> through [Groq's API](https://console.groq.com/docs/models). Groq provides many other models through an easy-to-use API [integrated into LangChain](https://python.langchain.com/v0.2/docs/integrations/chat/groq/). Groq's fast inference speed makes it much more useful when working with agents that take on multiple tasks throughout their workflow.

In order to use the agent and visualize its work, I used ⚡[FastAPI](https://fastapi.tiangolo.com/) to build two simples APIs and 🚀[Streamlit](https://streamlit.io/) to build a simple chat interface. The reason for using FastAPI and Streamlit is for there simplicity and ease of use.

<h3>📜Code Implementation</h3>

[FastAPI_Helpers/agent.py file](https://github.com/MarcDagher/Topic_Summarizer/blob/main/FastAPI_Helpers/agent.py) contains the main work done in this repo, where the code for the LanGrah agent is constructed as nodes and edges. Since LLMs are powerful tools for mult-task usecases, an LLM serves as a chatbot and as a tool-user in this application, the tool being Tavily. Although LLMs come with their own challenges, the use of prompt engineering techniques like identity prompting, few-shot prompting, and chain-of-thought prompting. The LLM was first given and identity, then followed with a step-by-step guide for tool usage, and instructed on how to organize and output its results.
