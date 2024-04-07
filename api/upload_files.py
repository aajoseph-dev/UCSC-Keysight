import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings


def upload_doc(document_path, tags):
    load_dotenv()
    azure_endpoint: str = os.getenv("OPENAI_ENDPOINT")
    azure_openai_api_key: str = os.getenv("OPENAI_KEY1")
    azure_openai_api_version: str = "2023-05-15"
    azure_deployment: str = "OpenTap-Plugin-Embedding-Model"

    vector_store_address: str = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
    vector_store_password: str =  os.getenv("AZURE_AI_SEARCH_API_KEY")

    embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
        azure_deployment=azure_deployment,
        openai_api_version=azure_openai_api_version,
        azure_endpoint=azure_endpoint,
        api_key=azure_openai_api_key,
    )

    index_name: str = "plugin-pdf-vector"
    vector_store: AzureSearch = AzureSearch(
        azure_search_endpoint=vector_store_address,
        azure_search_key=vector_store_password,
        index_name=index_name,
        embedding_function=embeddings.embed_query,
    )

    # Chunk/split the doc
    loader = PyPDFLoader(document_path, extract_images=False)
    data = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 5000,
        chunk_overlap  = 300,
        length_function = len
    )



    chunks = text_splitter.split_documents(data)
    vector_store.add_documents(documents=chunks)


if __name__ == "__main__":
    document_path = input("Path to File:")
    tags = input("Tags (Comma Seperated):").split(",")
    upload_doc(document_path, tags)