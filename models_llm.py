import os
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from dotenv import load_dotenv


load_dotenv()

modelo = AzureChatOpenAI(
    azure_deployment = os.getenv('deploy'),
    openai_api_version = os.getenv('version'),
    api_key = os.getenv('apikey'),
    azure_endpoint = os.getenv('endpoint'),
    request_timeout = 60,
    max_retries = 2,
    max_tokens=None
)

llm_embed = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv('deploy_e'),
    openai_api_version=os.getenv('version_e'),
    azure_ad_token=os.getenv('apijey_e'),
    azure_endpoint = os.getenv('endpoint_e'),
    chunk_size=1,
    request_timeout=120,
    max_retries=3
)