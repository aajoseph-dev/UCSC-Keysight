from bs4 import BeautifulSoup
import pdfkit
import os

parent_folder = "/Users/madeline/Desktop/UCSC-Keysight/docs/CE_files"

topic_links = [] 

counter = 0

with open("error_log.txt", "a") as error_file:
    for folder_name in os.listdir(parent_folder):
        topic_links = []
        counter += 1
        folder_path = os.path.join(parent_folder, folder_name)
        if (counter >= 30) and (os.path.isdir(folder_path)):
            # if counter == 35:
            print(f"folderpath: {folder_path}")
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if file_name.endswith(".sdl"):
                    print("FILE_PATH:", file_path)

                    with open(file_path, "r") as file: 
                        contents = file.read()
                    soup = BeautifulSoup(contents, 'xml')

                    # collect only the urls under HelpLink in .sdl file for each programming command
                    link = soup.find_all("HelpLink")

                    # iterate through each programming command url in .sdl, and add the first part of htm, which is path_to_topics
                    for data in link:
                        data_str = str(data.get('url'))
                        # if (".htm" not in data_str) or (".html" not in data_str):
                        #     continue
                        data_str = data_str.replace('\\', '/') 
                        complete_path =  f"{folder_path}/docs/{data_str}"
                        # print("complete path:", complete_path)
                        sep = '#'
                        complete_path = complete_path.split(sep, 1)[0] # remove characters starting from # and onwards
                        # if complete_path.endswith(".png") or complete_path.endswith(".gif") or complete_path.endswith(".js") or complete_path.endswith(".css"):
                        #     continue
                        if ".htm" in complete_path or ".html" in complete_path:
                            # print("complete_path:", c)
                            topic_links.append(complete_path)

                    # using the complete paths to the .htm for each programming command, put the content onto 1 .pdf file
                    try:
                        pdfkit.from_file(topic_links, f'{file_name}.pdf', verbose=True)
                    except Exception as e:
                        print("error?")
                        error_file.write(f"{file_name} Exception: {e}\n")