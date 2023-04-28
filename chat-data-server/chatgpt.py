import pandas as pd
from langchain.llms import OpenAI
from langchain.agents import create_pandas_dataframe_agent
import os
os.environ["OPENAI_API_KEY"] = "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"


def file_agent(file_path):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    print(df)
    agent = create_pandas_dataframe_agent(
        OpenAI(temperature=0), df, verbose=True)
    return agent

# export http_proxy="http://127.0.0.1:8889"
# export https_proxy="http://127.0.0.1:8889"
