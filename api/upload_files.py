import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

def upload_doc(document_path):

    # Load in all keys and endpoints
    load_dotenv()
    index_name = "pdf_data"
    endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
    key = os.getenv("AZURE_AI_SEARCH_API_KEY")

    # Init the search index client
    credential = AzureKeyCredential(key)
    client = SearchClient(endpoint=endpoint,
                        index_name=index_name,
                        credential=credential)
    
    # Chunk/split the doc
    loader = PyPDFLoader(document_path, extract_images=False)
    data = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 5000,
        chunk_overlap  = 300,
        length_function = len
    )

    chunks = text_splitter.split_documents(data)

    # Store the data into Azure search index
    for index, chunk in enumerate(chunks):
        data = {
            "id" : str(index + 1),
            "data" : chunk.page_content,
            "source": chunk.metadata["source"]
        }
        print("data:", data)

    result = client.upload_documents(documents=[data])

if __name__ == "__main__":
    document_path = input("Path to File:")
    upload_doc(document_path)