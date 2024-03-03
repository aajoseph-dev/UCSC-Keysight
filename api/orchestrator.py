import os
import sys
from openai import AzureOpenAI
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader
#from langchain_openai import AzureOpenAI

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient


if __name__ == "__main__":

    load_dotenv()

    # Define Azure search index properties
    index_name = "pdf_data"
    endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
    key = os.getenv("AZURE_AI_SEARCH_API_KEY")

    # Init the search index client
    credential = AzureKeyCredential(key)
    client = SearchClient(endpoint=endpoint,
                        index_name=index_name,
                        credential=credential)
    
    # Define Azure ML properties
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_VERSION"] = "2024-02-15-preview"
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_KEY1")
    os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_AI_SEARCH_ENDPOINT")

    # Init the Azure OpenAI model
    # llm = AzureOpenAI(deployment_name = "OpenTap-Plugin-LLM", 
    #                 model = "gpt-35-turbo",
    #                 temperature=1)
    
    llm = AzureOpenAI(
        azure_endpoint = "https://opentappluginai.openai.azure.com/", 
        api_key=os.getenv("OPENAI_KEY1"),  
        api_version="2024-02-15-preview"
    )
    
    # Read the PDF file using the langchain loader
    pdf_link = "../test-docs/one_page.pdf"
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

    # question = sys.argv[1]
    question = "Give me a full list of front panel controls for E364xA power supply"
    #category = sys.argv[2]
    # print(message_text)

    user_input = "question: "
    user_input += question

    context = """"""
    results = client.search(search_text=user_input, top = 2)


    for doc in results:
        context += "\n" + doc['data']

    print("context: ", context)

    print("done printing context")
        
    message_text = [{"role":"system","content":"{}. here is some context to help generate the plugin{}".format(question, context)}]
    #message_text = [{"role":"system","content":"generate a C++ outline for a opentap plugin for the {} {}. here is some context to help generate the plugin{}".format(device, category, context)}]

    completion = llm.chat.completions.create(
        model="OpenTap-Plugin-LLM", 
        messages = message_text,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )


    print(completion.choices[0].message.content)
