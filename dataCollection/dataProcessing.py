from bs4 import BeautifulSoup
import pdfkit
import os
import requests
import zipfile
import io
from collections import defaultdict
import sys

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

                        soup = BeautifulSoup(contents, 'xml')

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
                            pdfkit.from_file(topicLinks, f'{outputFolder}/{fileName}.pdf', verbose=True)
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
                

if __name__ == "__main__":
    print("Select an option")
    print("c: Convert Help File to PDF")
    print("f: Fetch URL Data")
    print("e: Exit the program")
    
    choice = input("Enter you choice (c or f): ")

    while True:
        if choice == "c" or "C":
            parentFolder = input("Enter the directory that contains the CE_files: ")
            outputFolder = input("Enter the directory to save the PDFs: ")
            break

        elif choice == "f" or "F":
            parentFolder = input("Enter the path to the xml file: ")
            outputFolder = input("Enter the directory to save the output: ")
            break

        elif choice == "e" or "E":
            print("The program has been terminated")
            sys.exit()