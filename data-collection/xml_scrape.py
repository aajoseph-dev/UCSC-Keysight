import webbrowser
from bs4 import BeautifulSoup
import urllib.parse
import os
import pdfkit


topic_links = []
path = "/Users/madeline/Desktop/UCSC-Keysight/documents/EDU/EDU36311A.sdl"
path_to_topics = "/Users/madeline/Desktop/UCSC-Keysight/documents/EDU/docs/"

with open(path, "r") as file:
    contents = file.read()
soup = BeautifulSoup(contents, 'xml')

link = soup.find_all("HelpLink")
# print("soup:", soup)
# print(str(link))
for data in link:

    data_str = str(data.get('url'))
    data_str = data_str.replace('\\', '/')
    complete_path = path_to_topics + data_str
    sep = '#'
    complete_path = complete_path.split(sep, 1)[0]
    topic_links.append(complete_path)


pdfkit.from_file(topic_links, 'out.pdf')

# for link in topic_links:
#     file_path = path + link
#     file_path = file_path.replace('\\', '/')
#    
#     file_path = file_path.split(sep, 1)[0]
#     print("file_path:", file_path)
#     with open(file_path, "r") as file:
#         contents = file.read()
#         soup = BeautifulSoup(contents, "html.parser")
#     links = soup.find_all('h3')
#     with open('myfile1.txt', 'a') as f:
#         for data in links:
#             f.write(data.get_text())
#             # print(data.get_text())
#             f.write("\n")
    # count += 1
    # if count == 3:
    #     break

    # /Users/madeline/Desktop/UCSC-Keysight/documents/EDU/docs/Topics/2 - Programming Commands/60 - IEEE-488 Subsystem.htm
    # /Users/madeline/Desktop/UCSC-Keysight/documents/EDU/docs/Topics/2 - Programming Commands/60 - IEEE-488 Subsystem.htm#ESE
