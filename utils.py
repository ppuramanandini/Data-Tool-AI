import streamlit as st
import pandas as pd
from streamlit.delta_generator import DeltaGenerator
from streamlit.runtime.uploaded_file_manager import UploadedFile

def upload_file() -> pd.DataFrame | None:
    df = None
    file = st.file_uploader("Upload your file: ")
    if file:
        try:
            df = read_file(file)
            if 'file_name' not in st.session_state:
                st.session_state['file_name'] = file.name
                st.session_state['df'] = df
            elif st.session_state.file_name != file.name:
                st.session_state.file_name = file.name
                 
        except ValueError as e:
            st.error(f"{e}")
    else:
        st.subheader("Please upload a file")
    return df

def read_file(file:UploadedFile | None) -> pd.DataFrame : 
    if file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
    elif file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith('json'):
        df = pd.read_json(file)
    else:
        raise ValueError("Invalid File Type: Please enter a valid file(csv, excel, json)")  
    if df.empty:
        raise ValueError("Empty file")
    return df