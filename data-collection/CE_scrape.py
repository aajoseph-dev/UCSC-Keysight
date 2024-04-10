import requests
import zipfile
import io
import os
from bs4 import BeautifulSoup
from collections import defaultdict

dict = defaultdict(list)

cwd = os.path.dirname(os.getcwd())

# path = "/Users/madeline/Desktop/UCSC-Keysight/docs/entire.xml"
path = f"{cwd}/docs/entire.xml"

# open and read in sdl file
with open(path, "r") as file: 
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
    download_directory = f"{cwd}/docs/{key}"
    os.makedirs(download_directory, exist_ok=True)
    url = f"http://commandexpert.support.keysight.com/mojo/download.php?Guid={dict[key][0]}&&RevisionNumber={dict[key][1]}&&Version={dict[key][2]}"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        z = io.BytesIO(response.content)
        if zipfile.is_zipfile(z):
            with zipfile.ZipFile(z, 'r') as z:
                z.extractall(download_directory)
            print("File downloaded successfully.")
        else:
            print(f"Not a zipfile: key {key}, {dict[key]}")
    else:
        print(f"Failed to download file: key {key}, {dict[key]}. Status code: {response.status_code}")
        
# file:///Users/madeline/Desktop/UCSC-Keysight/docs/CE_files/B296x%20Low%20N
#  ise%20Power%20Source/docs/B2960/B2960_subsystem_TRIGgerACQuireTRANsientALLTOUTputSTATe.html