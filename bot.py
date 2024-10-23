import streamlit as st
from llm import llm
import time
from agent import agent_generate_response

st.title("Neo4j KnowledgeBase Portal")

client = llm

def stream_data(sentence):
    for word in sentence.split(" "):
        yield word + " "
        time.sleep(0.02)
        
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"content": "Hello! I am your virtual librarian, looking after your Google Drive documents. How can I assist you today?", "role": "assistant"})


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        agent_response = agent_generate_response(prompt)
        stream = stream_data(agent_response)
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})