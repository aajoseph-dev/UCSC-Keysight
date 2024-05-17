import os
import sys
import requests
import zipfile
import io
from collections import defaultdict

from bs4 import BeautifulSoup
import pdfkit
from PyPDF2 import PdfReader

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings

class DataFetch:

    def __init__(self):
        pass

    def convertToPDF(self, parentFolder, outputFolder):

        if not os.path.exists(parentFolder) or not os.path.isdir(parentFolder):
            print(f"Error: Parent folder '{parentFolder}' does not exist or is not a directory.")
            return
        
        if not os.path.exists(outputFolder) or not os.path.isdir(outputFolder):
            print(f"Error: Output folder '{outputFolder}' is not a valid directory.")
            return
    
        for folderName in os.listdir(parentFolder):
            topicLinks = []
            folderPath = os.path.join(parentFolder, folderName)
            if os.path.isdir(folderPath):

                for fileName in os.listdir(folderPath):

                    filePath = os.path.join(folderPath, fileName)

                    if fileName.endswith(".sdl"):

                        with open(filePath, "r") as file: 
                            contents = file.read()

                        soup = BeautifulSoup(contents, 'lxml-xml')
                        link = soup.find_all("HelpLink")

                        for data in link:
                            dataStr = str(data.get('url'))
                            dataStr = dataStr.replace('\\', '/') 
                            completePath =  f"{folderPath}/docs/{dataStr}"
                            sep = '#'
                            completePath = completePath.split(sep, 1)[0] 

                            if ".htm" in completePath or ".html" in completePath:
                                topicLinks.append(completePath)

                        try:
                            pdfkit.from_file(topicLinks, f'{outputFolder}/{fileName.strip(".sdl")}.pdf', verbose=True)
                        except Exception as e:
                            print(f"The file could not be parsed: {e}")

    def fetchUrlData(self, filePath, outputFolder):
        if not os.path.exists(filePath) or not os.path.isfile(filePath):
            print(f"Error: File path '{filePath}' does not exist or is not a valid file.")
            return

        if not os.path.exists(outputFolder) or not os.path.isdir(outputFolder):
            print(f"Error: Output folder '{outputFolder}' is not a valid directory.")
            return
        
        dict = defaultdict(list)

        # open and read in sdl file
        with open(filePath, "r") as file: 
            contents = file.read()
        soup = BeautifulSoup(contents, 'xml')

        idfs = soup.find_all("idf")

        #[guid, revision num, firmware ver, supported models, short name]
        for data in idfs:
            if data.get("name") in dict:
                if data.get("revisionNumber") > dict[data.get("name")][1]:
                    dict[data.get("name")] = [data.get("guid"), 
                                            data.get("revisionNumber"),
                                            data.get("firmwareVersions"),
                                            data.get("supportedModels"),
                                            data.get("shortName")]
            else:
                dict[data.get("name")] = [data.get("guid"), 
                                            data.get("revisionNumber"),
                                            data.get("firmwareVersions"),
                                            data.get("supportedModels"),
                                            data.get("shortName")]

        for key in dict:
            url = f"http://commandexpert.support.keysight.com/mojo/download.php?Guid={dict[key][0]}&&RevisionNumber={dict[key][1]}&&Version={dict[key][2]}"
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                z = io.BytesIO(response.content)
                if zipfile.is_zipfile(z):
                    with zipfile.ZipFile(z, 'r') as z:
                        z.extractall(f"{outputFolder}/docs/{key}")
                    print("File downloaded successfully.")
                else:
                    print(f"Not a zipfile: key {key}, {dict[key]}")
            else:
                print(f"Failed to download file: key {key}, {dict[key]}. Status code: {response.status_code}")

    def uploadFile(self, pathToFile):
            
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

        print("about to chunk/split the doc")

        # Calculate average chunk size
        average_chunk_size = self.calculate_average_chunk_size(pathToFile)

        loader = PyPDFLoader(pathToFile, extract_images=False)
        data = loader.load_and_split()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=average_chunk_size,
            chunk_overlap=0.15 * average_chunk_size,  # 15% overlap
            length_function=len
        )

        chunks = text_splitter.split_documents(data)

        vector_store.add_documents(documents=chunks)

        print("DONE!")

    def calculate_average_chunk_size(self, pathToFile):
        total_characters = 0
        total_pages = 0

        # Calculate total character count and total page count
        with open(pathToFile, 'rb') as file:
            pdf_reader = PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                total_characters += len(pdf_reader.pages[page_num].extract_text())
            total_pages += len(pdf_reader.pages)

        # Calculate average character count per page
        average_character_count_per_page = total_characters / total_pages

        # Consider overlap (e.g., 15% overlap)
        overlap_percentage = 0.15
        average_chunk_size = average_character_count_per_page / (1 - overlap_percentage)

        return average_chunk_size

if __name__ == "__main__":
    print("Select an option")
    print("c: Convert Help File to PDF")
    print("f: Fetch URL Data")
    print("u: Upload files to azure")
    print("e: Exit the program")
    
    choice = input("Enter you choice: ")
    dataFetch = DataFetch()

    if choice == "c":
        parentFolder = input("Enter the directory that contains the CE_files: ")
        outputFolder = input("Enter the directory to save the PDFs: ")
        dataFetch.convertToPDF(parentFolder, outputFolder)

    elif choice == "f":
        parentFolder = input("Enter the path to the xml file: ")
        outputFolder = input("Enter the directory to save the output: ")
        dataFetch.fetchUrlData(parentFolder, outputFolder)

    elif choice == "u":
        pathToFile = input("Enter path to file: ")
        dataFetch.uploadFile(pathToFile)

    elif choice == "e":
        print("The program has been terminated")
    else:
        print("invalid input")
    
    sys.exit()

        