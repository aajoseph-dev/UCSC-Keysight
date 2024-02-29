from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain_openai import AzureOpenAI

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from dotenv import load_dotenv

import os


def generate_response(user_question):

    # Fetch the appropriate chunk from the database
    context = """"""
    results = client.search(search_text=user_question, top = 2)
        
    for doc in results:
        context += "\n" + doc['data']
    print(context)

    # Append the chunk and the question into prompt
    qna_prompt_template = f"""You will be provided with the question and a related context, you need to answer the question using the context.

    Context:
    {context}

    Question:
    {user_question}

    Make sure to answer the question only using the context provided, if the context doesn't contain the answer then return "I don't have enough information to answer the question".

    Answer:"""

    # Call LLM model to generate response
    response = llm(qna_prompt_template)
    return response

if __name__ == "__main__":

    load_dotenv() # take environment variables from .env.

    # Define Azure search index properties
    index_name = "azure-rag-demo-index" # NEEDS TO BE UPDATED
    endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT") # = "YOUR_AZURE_SEARCH_ENDPOINT" 
    key1 = os.getenv("AZURE_AI_SEARCH_API_KEY") # = "YOUR_AZURE_SEARCH_KEY" 

    credential = AzureKeyCredential(key1)
    client = SearchClient(endpoint=endpoint,
                        index_name=index_name,
                        credential=credential)

    # Define Azure ML properties
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_VERSION"] = os.getenv("OPENAI_API_VERSION_ENV")
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_KEY1") # "YOUR_OPENAI_KEY"
    os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("OPENAI_ENDPOINT") # "YOUR_OPENAI_ENDPOINT"

    # Init the Azure OpenAI model
    llm = AzureOpenAI(deployment_name = "OpenTap-Plugin-LLM", 
                    model = "gpt-35-turbo",
                    temperature=1)

    # Read the PDF file using the langchain loader
    pdf_link = "../test-docs/dual_power_supplies.pdf"
    loader = PyPDFLoader(pdf_link, extract_images=False)
    data = loader.load_and_split()

    # Split data into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 5000,
        chunk_overlap  = 20,
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

        result = client.upload_documents(documents=[data])

    # Take the user input and call the utility function to generate the response
    user_question = “YOUR_QUESTION”
    response = generate_response(user_question)
    print("Answer:",response)