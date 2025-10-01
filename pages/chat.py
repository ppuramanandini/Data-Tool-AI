import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
import os

st.set_page_config('AI Data Tool - Chat', page_icon="📊")

def run_code(container):
    output = st.session_state.agent.run_code()
    
    with container:
        if isinstance(output, str): 
            st.markdown(output)
        elif output == None:
            image = Image.open(f"data/{st.session_state['session_id']}.png")
            st.image(image)

def clean_session():
    if 'agent' in st.session_state:
        st.session_state.agent.cleanup()
    
    keys_to_delete = ['agent', 'session_id', 'df', 'file_name', 'content', 'messages', 'executed']
    for key in keys_to_delete:
        if key in st.session_state:
            del st.session_state[key]
    st.switch_page("app.py")

if 'agent' not in st.session_state:
    st.error("No agent found. Please upload a file on the main page first.")
    st.stop()

st.title("Chat and Edit")

st.session_state['executed'] = False

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.agent.chat(prompt)
        st.markdown(response)

    container = st.container(border=True)
    st.button(label="Execute", on_click=run_code, args=(container, ))
    
    st.session_state.messages.append({"role": "assistant", "content": response})

st.sidebar.button("Clean Session & Start Over", on_click=clean_session, type="primary")
