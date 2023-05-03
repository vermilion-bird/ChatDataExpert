import pandas as pd
from langchain.llms import OpenAI
from langchain.agents import create_pandas_dataframe_agent

from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor

def read_data(file_path):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    return df

def file_agent(file_path):
    df = read_data(file_path)
    agent = create_pandas_dataframe_agent(
        OpenAI(temperature=0), df, verbose=True, max_iterations=5)
    return agent

def sql_agent(db_uri):
    db = SQLDatabase.from_uri(db_uri)
    toolkit = SQLDatabaseToolkit(db=db)
    agent_executor = create_sql_agent(
        llm=OpenAI(temperature=0),
        toolkit=toolkit,
        verbose=True    )
    return agent_executor

