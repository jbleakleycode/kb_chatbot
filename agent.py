from llm import llm
from graph import graph
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.tools import Tool
from langchain_community.chat_message_histories import Neo4jChatMessageHistory
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from utils import get_session_id
from vector import get_article_content

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a neo4j expert providing information about the knowledge base."),
        ("human", "{input}"),
    ]
)

general_chat = chat_prompt | llm | StrOutputParser()

tools = [
    Tool.from_function(
        name="General Chat",
        description="For used chat/questions that do not ask for 'article' or 'document' information.",
        func=general_chat.invoke,
    ), 
    Tool.from_function(
        name="Neo4j knowledge base search",  
        description="To be used for questions relating to Neo4j, or that ask for documents or article information (as this referes to knowledge base content). Do not answer any questions using your pre-trained knowledge, only use the information provided in the context.",
        func=get_article_content, 
    )
]
# For when you are asked to provide information from the neo4j knowledge base. 

def get_memory(session_id):
    return Neo4jChatMessageHistory(session_id=session_id, graph=graph)

agent_prompt = PromptTemplate.from_template("""
You are a Neo4j team member helping other team members by fetching information from the knowledge base in a palatable, easy to follow format.

Be as helpful as possible and return as much information as possible while being concise.

Explicitly return the title of the documents/articles found and include all document names as sources in the final response.


TOOLS:
------

You have access to the following tools:

{tools}

Please use the following format:

When you have a response to say to the Human, you MUST use the format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: you should always include the action to take - it should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Action: Continue iteration if final answer has not been provided, otherwise provide the final answer and stop iteration.
Final Answer: The final answer to the question originally asked.




ALWAYS explicitly return the title (from the metadata) of the documents/articles found and include all document names as sources in the final response.

If a document/article is requested, explicitly return the content (from the metadata) pertaining to the document/article.
If a summary of a document/article is requested, return a summary of the content (from the metadata) pertaining to the document/article.
If the software of a document/article is requested, return the softwares from the metadata pertaining to the document/article.
If the operation of a document/article is requested, return the operations from the metadata pertaining to the document/article.

Begin!


Previous conversation history:
{chat_history}

Question: {input}

Thought:{agent_scratchpad}
Action: Continue iteration if final answer has not been provided, otherwise provide the final answer and stop iteration.
""")

agent = create_react_agent(llm, tools, agent_prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
    )

chat_agent = RunnableWithMessageHistory(
    agent_executor,
    get_memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)

def agent_generate_response(user_input):
    """
    Create a handler that calls the Conversational agent
    and returns a response to be rendered in the UI
    """
    print("memory", get_memory(get_session_id()))

    response = chat_agent.invoke(
        {"input": user_input},
        {"configurable": {"session_id": get_session_id()}},)

    return response['output']
