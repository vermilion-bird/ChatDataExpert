import os
import pandas as pd
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_pandas_dataframe_agent
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from agents.agent_toolkits.matplotlib.base import create_matplotlib_agent
from conf.config import OPENAI_MODEL, AZURE_OPENAI_API_DEPLOYNENT_ID,AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_BASE,AZURE_OPENAI_API_EMBDDING_DEPLOYMENT_ID,AZURE_OPENAI_API_EMBDDING_MODEL,AZURE_OPENAI_API_VERSION,ELASTICSEASRCH_URL,ES_INDEX,ES_USER,ES_PASSWORD,ES_CA_CERTS,AZURE_OPENAI_API_MODEL
import uuid
from datetime import datetime
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain import ElasticVectorSearch
from langchain.llms.openai import AzureOpenAI



def read_data(file_path):
    if file_path.endswith('.csv') or file_path.endswith('.txt'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.json') or file_path.endswith('.jsonl'):
        df = pd.read_json(file_path)
    return df


def create_embddings(llm_type='azure'):
    if llm_type == 'azure':
        embeddings = OpenAIEmbeddings(
        deployment=AZURE_OPENAI_API_EMBDDING_DEPLOYMENT_ID,
        model=AZURE_OPENAI_API_EMBDDING_MODEL,
        openai_api_base=AZURE_OPENAI_API_BASE,
        openai_api_type="azure",
        openai_api_version=AZURE_OPENAI_API_VERSION,
        chunk_size=1
        )
    else:
        embeddings = OpenAIEmbeddings(
        model=OPENAI_MODEL,
        )
    return embeddings

def create_llm(llm_type='azure'):
    print(AZURE_OPENAI_API_MODEL)
    if llm_type == 'azure':
        llm = AzureOpenAI(
        deployment_name=AZURE_OPENAI_API_DEPLOYNENT_ID,
        model=AZURE_OPENAI_API_MODEL,
        openai_api_base=AZURE_OPENAI_API_BASE,
        )
    return llm

def env_var(api_type='azure'):
    """环境变量设置"""
    if api_type == 'azure':
        os.environ["OPENAI_API_TYPE"] = "azure"
        os.environ["OPENAI_API_VERSION"] = AZURE_OPENAI_API_VERSION
        os.environ["OPENAI_API_BASE"] = AZURE_OPENAI_API_BASE
        os.environ["OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY
    else:
        os.environ["OPENAI_API_KEY"] = api_key


def file_agent(file_path, model_name=OPENAI_MODEL):
    df = read_data(file_path)
    agent = create_pandas_dataframe_agent(
        ChatOpenAI(model_name=model_name, temperature=0), df, verbose=True)
    return agent


def sql_agent(db_uri, model_name=OPENAI_MODEL):
    db = SQLDatabase.from_uri(db_uri)
    toolkit = SQLDatabaseToolkit(db=db)
    agent_executor = create_sql_agent(
        llm=ChatOpenAI(model_name=model_name, temperature=0),
        toolkit=toolkit,
        verbose=True)
    return agent_executor


def matplotlib_agent(file_path, model_name=OPENAI_MODEL):
    df = read_data(file_path)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    timedate = datetime.now().strftime("%Y%m%d")
    unique_id = str(uuid.uuid4())[:8]
    plot_dir = f'./temp/{timedate}'
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    plot_path = f'{plot_dir}/{timestamp}_{unique_id}.png'
    llm = ChatOpenAI(model_name=model_name, temperature=0)
    agent = create_matplotlib_agent(
        llm, df, temperature=0, verbose=True, plot_path=plot_path)
    return agent, plot_path

def es_embedding_text(documents,meta_data=None):
    """文本嵌入"""
    env_var(api_type='azure')
    embeddings = create_embddings()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    if meta_data:
        docs = [doc.metadata.update(meta_data) or doc for doc in embddings]
    es_ssl_verify = {'verify_certs':True, 'basic_auth':(ES_USER, ES_PASSWORD), 'ca_certs': ES_CA_CERTS}
    db = ElasticVectorSearch.from_documents(docs, embeddings, index_name=ES_INDEX, elasticsearch_url=ELASTICSEASRCH_URL, es_ssl_verify=es_ssl_verify)
    return db

def es_vector_search(query, top_k=3):
    """向量搜索"""
    env_var(api_type='azure')
    embeddings = create_embddings()
    es_ssl_verify = {'verify_certs':True, 'basic_auth':(ES_USER, ES_PASSWORD), 'ca_certs': ES_CA_CERTS}
    elastic_vector_search = ElasticVectorSearch(
            elasticsearch_url=ELASTICSEASRCH_URL,
            index_name=ES_INDEX,
            embedding=embeddings,
            es_ssl_verify=es_ssl_verify
        )
    results = elastic_vector_search.similarity_search(query, k=top_k)
    return results