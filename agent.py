import pandas as pd
import requests
from langchain.prompts import PromptTemplate
from langchain_experimental.utilities import PythonREPL
from langchain_google_genai import GoogleGenerativeAI
import streamlit as st
import matplotlib.pyplot as plt
import os
import textwrap
import re

class PandasAgent():
    
    import pandas as pd
    import requests
    from langchain.prompts import PromptTemplate
    from langchain_experimental.utilities import PythonREPL
    
    def __init__(self, api_key: str, model: str, df: pd.DataFrame):
        self._model = model
        self._api_key = api_key
        self._df = df
        self.llm = GoogleGenerativeAI(model='gemini-2.0-flash', api_key = self._api_key)

        os.makedirs('data', exist_ok=True)

        self._df_path = f"data/{st.session_state['session_id']}.csv"
        self._df.to_csv(self._df_path, index=False)
        self.response = None 

        self._prompt = PromptTemplate.from_template(
            template = """
            You are a data scientist assistant and must strictly answer only those queries that are related to the given data. In case of any unnecessary queries reply "I don't know"
            From the given dataframe: `{df}`
            Reason the following query: {query}
            Include code as well. (code given should be compatabile with markdown format).
            Your response to the query should be strictly in the form of as follows:
            1. Code Snippet (Assume that the dataset is already imported and is contained by the variable `df`, Make necessary imports except `pandas`)
            2. Short description about the code snippet
            3. Sample Output
            """
        )
        
        self.runner = PythonREPL()
    
    def set_df(self, df: pd.DataFrame):
        self._df = df
        self._df.to_csv(self._df_path, index=False)
    
    def set_model(self, model: str):
        self._model = model
    
    def update_df(self):
        self._df = pd.read_csv(self._df_path)
        st.session_state['content'] = self._df.to_string(index=False)
        
    def chat(self, query: str):
        try:
            prompt_str = self._prompt.invoke({'df': self._df.head().to_string(index=False), 'query': query}).to_string().strip()
            response = self.llm.invoke(prompt_str)
            self.response = str(response)
            return self.response
            
        except requests.exceptions.RequestException as e:
            print(f"Error occurred during API request: {e}")
            return f"Error occurred: {e}"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return f"An unexpected error occurred: {e}"
    
    def preprocess_code(self, raw_code: str) -> str:
        if not raw_code or not raw_code.strip():
            return ""
        
        lines = raw_code.split('\n')
        
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        
        if not lines:
            return ""
        
        min_indent = float('inf')
        for line in lines:
            if line.strip():  
                indent = len(line) - len(line.lstrip())
                min_indent = min(min_indent, indent)
        
        if min_indent == float('inf'):
            min_indent = 0
        
        dedented_lines = []
        for line in lines:
            if line.strip():
                dedented_lines.append(line[min_indent:])
            else:
                dedented_lines.append("")
        
        cleaned_code = '\n'.join(dedented_lines)
        
        cleaned_code = cleaned_code.strip()
        
        cleaned_code = re.sub(r'^```python\s*', '', cleaned_code, flags=re.MULTILINE)
        cleaned_code = re.sub(r'^```\s*$', '', cleaned_code, flags=re.MULTILINE)
        cleaned_code = re.sub(r'^\s*python\s*$', '', cleaned_code, flags=re.MULTILINE)
        
        cleaned_code = re.sub(r'\n\s*\n\s*$', '\n', cleaned_code)
        
        return cleaned_code

    def get_code(self):
        if self.response: 
            code_blocks = self.response.split("```")
            raw_code = ''.join([code.strip("python") for code in code_blocks if code.startswith('python')])
            return self.preprocess_code(raw_code)
            
    def run_code(self):
        imports_code = f"""import pandas as pd
df = pd.read_csv('{self._df_path}')\n"""
        code_to_run = imports_code + self.get_code().strip() + f"\ndf.to_csv('{self._df_path}', index=False)"
        output = self.runner.run(code_to_run)

        if len(output) == 0:
            output = "Executed Successfully"

        if "plt.show()" in code_to_run:
            plt.savefig(f"data/{st.session_state['session_id']}.png")
            output = None        

        self.update_df()
        return output

    def cleanup(self):
        csv_path = self._df_path
        png_path = f"data/{st.session_state['session_id']}.png"

        if os.path.exists(csv_path):
            os.remove(csv_path)
        
        if os.path.exists(png_path):
            os.remove(png_path)
