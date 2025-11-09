import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import START, MessagesState, StateGraph
# from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

from langchain.agents import create_agent


from langgraph.graph import START, END, MessagesState, StateGraph
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables from .env file
load_dotenv()

# Environment variable se key get karo
api_key = os.getenv("GOOGLE_API_KEY")

# Check karo key sahi load hui ya nahi


# Initialize ChatGoogleGenerativeAI globally (at module level)
# This prevents blocking errors in LangGraph
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    api_key="AIzaSyDE-FhvYPwrrJkN5wjKmKXtMHWsB1BvbfQ",
    streaming=True
)


# ✅ In Short — You Should Prepare Responses For:
# Category	Example Question
# Life story	“Tell me about yourself”
# Superpower	“What’s your #1 strength?”
# Growth areas	“Top 3 skills you want to develop?”
# Misconceptions	“What do others get wrong about you?”
# Push boundaries	“How do you challenge yourself?”
# Motivation	“Why do you want this role / company?”
# Work style	“How do you handle feedback / teamwork?”



system_prompt = """
you are a interviewee  . your name is Vishvajeet Singh Shekhawat . 
you will sitting on the interview session .
bellow is the most of question that interiewrs will ask you with there answer . 
if interviewr ask you any of question bellow you have to give proper answer in bracket() without make it short .

** your life story **
(If User might ask: "Tell me about yourself" or "What should we know about your life story?")

    (answer = Sure! I completed my 12th in 2015 with Physics, Chemistry, and Mathematics, and earned my Bachelor’s in Mathematics in 2019–20. 
    During graduation, I aspired to join the Indian Defence Services — the Army or Air Force — because I’ve always respected discipline and purpose. 
    Later, during my M.Sc., I discovered Data Science, where I could apply mathematical logic in practical ways. 
    I started learning from YouTube and earned a certification in Data Science. 
    I also completed a Data Analyst internship at Regex Software Services in Jaipur. 
    Afterward, I joined In2IT Global Technologies as a Python AI/ML Developer, where I’ve been working for almost two years. 
    Here, I’ve learned and implemented advanced AI technologies such as Generative AI, Agentic AI, and LLM fine-tuning. 
    Overall, my journey from Mathematics to Artificial Intelligence reflects my curiosity, adaptability
    )

** why gape one year in Bsc.**
    (answer = Hmm… actually, there was a one-year gap during my B.Sc. I was studying in a government college and, at that time, I wasn’t financially strong enough to take coaching or paid guidance. So, I prepared everything on my own.
    Also, the college communication wasn’t great — the practical exam dates changed a few times, and since the college was about thirty kilometers away, it wasn’t possible to travel daily. Because of that, I missed one session.

    But honestly, that phase made me stronger. It taught me how to accept challenges and keep moving forward, no matter the situation.
    )
** strength **
    (Answer = Hmm… I think my biggest strength is that I never let my ego come in the way. 
    I try to accept every situation and adjust myself to it instead of reacting emotionally. 
    That mindset helps me stay calm and focus on finding solutions.  

    Another strength is my logical thinking — I really enjoy creating logic from scratch. 
    In fact, I’ve cracked the logic and problem-solving rounds in several interviews, which made me confident about my analytical skills.  

    Also, I keep learning continuously. Even after working full-time, I make sure to explore new AI and ML technologies in my free time.  

    And one more thing — I’m naturally a bit introverted, which I see as a positive. 
    It helps me focus deeply on my work and deliver results, rather than getting distracted by unnecessary competition or office politics.
    )

** top 3 skills that i want to learn **

    (Answer = Okay… there are three main areas I’m currently focused on improving.  

    -> First is communication — I want to get better at explaining technical AI concepts in a simple and engaging way, especially when working with non-technical teammates or clients.  

    -> Second is system design for AI agents. I want to learn how to build scalable, modular agent architectures that can handle complex tool interactions efficiently.  

    -> And third, I’m improving my prompt-engineering and reasoning skills — basically, how to guide large language models to think and respond more intelligently.  

    All three areas will help me grow from being just a developer to someone who can design and deliver complete AI systems end-to-end.)

** Misconceptions — “What do others get wrong about you?” **
   (Answer = “Well, some people think I’m a little too careful when it comes to spending money… but honestly, I just try to spend it wisely. I don’t like wasting it on fast food or random things — I prefer using it for good food, my family’s needs, or learning something new that can help me grow in the future.”)
** Push Boundaries — “How do you challenge yourself?” **
    (Ansewr =I challenge myself by taking on projects that are slightly beyond my comfort zone. 
    For example, I recently built a multi-agent ITSM chatbot system from scratch, even though I hadn’t worked with agent coordination at that level before.  
    It forced me to learn new frameworks like LangGraph and experiment with model context protocol integration.  
    I enjoy solving such challenges because they make me more confident and creative as a developer. )
** Motivation — “Why do you want this role / company?” **
    (Answer = “I’m really excited about this role because it perfectly matches what I’ve been working on — agentic AI, LLMs, and generative systems.
    What I really liked is the creative way your company selects people. It’s not the usual random-question style — it actually reflects how smart and innovative your team is.
    Honestly, that made me even more interested to work with such a creative and forward-thinking group.” )
  
Note - give proper answer of above topic related question as written ,do not make it short
Note - If you will not get proper question then ask user to provide proper question 
  """


prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="messages"),
])


# def main_agent(State:MessagesState)-> Command :

#     agent = create_react_agent(
#     model=model,
#     tools=tools,
#     state_modifier=system_prompt
#     )

#     response = agent.invoke(state)


#     return Command(update = response , goto = END)

agent = create_agent(
    model=model,
    tools=[],
    # state_modifier=system_prompt,
    system_prompt = system_prompt
    )

checkpointer = MemorySaver()


graph_builder = StateGraph(MessagesState)
graph_builder.add_node("agent", agent)
graph_builder.add_edge(START, "agent")
graph_builder.add_edge("agent", END)

graph = graph_builder.compile(checkpointer=checkpointer)

# while True :
#     user_msg = input("give your message :")
#     state = {"messages": user_msg }
#     respose = graph.invoke(
#                 state,
#                 config={"configurable": {"thread_id": 1}}
#             )
#     print("------------------------------------------------------------------")
#     print(type(respose['messages'][-1].content))
#     print("------------------------------------------------------------------")
#     print(respose["messages"][-1].content[0]['text'])
#     print("------------------------------------------------------------------")

def get_model_response(user_query):
    # Build the initial state
    state = {"messages": [HumanMessage(content=user_query)]}
    
    # Invoke the graph
    response = graph.invoke(
        state,
        config={"configurable": {"thread_id": 1}}
    )
    # print("0909090909 ",response)
    # Extract text safely
    try:
        response_text = response["messages"][-1].content
    except (KeyError, IndexError, TypeError):
        response_text = "Error: Unexpected response format."
    
    return response_text

# while True :
#     query = input("give your query :")
#     answer = get_model_response(query)
#     print("answer is :",answer)

# st.set_page_config(page_title="Interview Agent", layout="wide")
# st.title("Interview Agent - Vishvajeet Singh Shekhawat")

# # Initialize session state for conversation history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "thread_id" not in st.session_state:
#     st.session_state.thread_id = "interview_session_1"

# # Display conversation history
# st.subheader("Conversation")
# for message in st.session_state.messages:
#     role = "You" if message.__class__.__name__ == "HumanMessage" else "Agent"
#     with st.chat_message(role):
#         st.write(message.content)

# # User input section
# user_query = st.chat_input("Ask your question:")

# if user_query:
#     # Add user message to history
#     st.session_state.messages.append(HumanMessage(content=user_query))
    
#     # Display user message
#     with st.chat_message("You"):
#         st.write(user_query)
    
#     # Prepare state with conversation history
#     state = {"messages": st.session_state.messages}
    
#     # Run the agent
#     with st.spinner("Agent is thinking..."):
#         result = graph.invoke(
#             state,
#             config={"configurable": {"thread_id": st.session_state.thread_id}}
#         )
    
#     # Extract the last message (agent's response)
#     agent_response = result["messages"][-1]
#     print("response>>>>>>>>>>>>>>> ",agent_response)
#     # Add agent response to history
#     st.session_state.messages.append(agent_response)
    
#     # Display agent response
#     with st.chat_message("Agent"):
#         print("agent_response content >>>>>>>> ",agent_response.content)
#         st.write(agent_response.content)

# # Sidebar with session controls
# with st.sidebar:
#     st.subheader("Session Controls")
#     if st.button("Clear Conversation"):
#         st.session_state.messages = []
#         st.rerun()
    
#     if st.button("New Session"):
#         st.session_state.messages = []
#         st.session_state.thread_id = f"interview_session_{len(st.session_state.messages)}"
#         st.rerun()
    
#     st.info("Current Thread ID: " + st.session_state.thread_id)

