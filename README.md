<h1 align="center">Topic Summarizer</h1>

<h3>🎯Aim</h3>
The aim of this repo is to build a system that stays up-to-date with current day events, allowing users to interact with it and ask about any topic at any time.

<h3>🛠️Tools Used</h3>
To build this system I used the following tools:

- 🕸️[LangGraph](https://www.langchain.com/langgraph) allows for the organization of the agent's workflow in a graphical manner, where each task is represented as a node and the possible paths to take are represented as edges. In my case, I had only two nodes LLM and ToolBox (other than _end_ and _start_).

- 🤖<strong>"llama3-70b-8192"</strong> accessed through [Groq's API](https://console.groq.com/docs/models). Groq provides a variety of models through an easy-to-use API, which is [integrated into LangChain](https://python.langchain.com/v0.2/docs/integrations/chat/groq/). Groq's fast inference speed makes it advantageous when working with agents that handle multiple tasks throughout their workflow.

- ⚡[FastAPI](https://fastapi.tiangolo.com/) was used to create two simple APIs for the system. FastAPI is chosen for its simplicity and efficiency.

- 🚀[Streamlit](https://streamlit.io/) was used to build a straightforward chat interface. Streamlit's ease of use makes it an ideal choice for this purpose.

<h3>📜Code Implementation</h3>

[FastAPI_Helpers/agent.py file](https://github.com/MarcDagher/Topic_Summarizer/blob/main/FastAPI_Helpers/agent.py) contains the core implementation of this repo, where the code for the LanGrahp agent is constructed using nodes and edges. In this application, the LLM serves both as a chatbot and as a tool user, with Taivly as the associated tool. Although LLMs are powerful tools, they come with their own challenges that are addressed using prompt engineering techniques like identity prompting, few-shot prompting, and chain-of-thought prompting. The LLM is first given an identity, followed by a step-by-step guide for tool usage, and instructions on organizing and presenting its results.
