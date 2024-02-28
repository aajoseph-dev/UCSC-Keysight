from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain_openai import AzureOpenAI

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

import os

# Define Azure search index properties
index_name = "azure-rag-demo-index"
endpoint = "YOUR_AZURE_SEARCH_ENDPOINT" 
key = "YOUR_AZURE_SEARCH_KEY" 

# Init the search index client
credential = AzureKeyCredential(key)
client = SearchClient(endpoint=endpoint,
                      index_name=index_name,
                      credential=credential)