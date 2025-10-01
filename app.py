import streamlit as st
from agent import PandasAgent
from utils import upload_file
from dotenv import load_dotenv
import os
from uuid import uuid1

st.set_page_config('AI-Powered Data Tool', page_icon="📊")

st.title('AI-Powered Data Tool')
st.divider()

load_dotenv()

df = upload_file()

if df is not None:
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = str(uuid1())

    if 'agent' not in st.session_state:
        st.session_state['agent'] = PandasAgent(
            api_key=st.secrets['API-KEY'], 
            model="gpt-oss:20b",
            df=st.session_state['df']
        )
    st.dataframe(st.session_state['df'])
if st.button(label="Chat now"):
    st.switch_page("pages/chat.py")

with st.sidebar:
    if 'content' not in st.session_state:
        st.session_state['content'] = ''
    else:
        content = st.session_state.get('content')
        res=content.split('\n')
        comma_separated_rows = [','.join(ele.split()) for ele in res]

        content = '\n'.join(comma_separated_rows)

        st.download_button(label="Download Preprocessed Data", data=content, file_name="data.csv")

