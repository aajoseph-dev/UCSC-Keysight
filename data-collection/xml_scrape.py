from bs4 import BeautifulSoup
import pdfkit

topic_links = [] # list to contain every programming command htm content
path = "/Users/madeline/Desktop/UCSC-Keysight/documents/EDU/EDU36311A.sdl" # contains each url for the htm of each command
path_to_topics = "/Users/madeline/Desktop/UCSC-Keysight/documents/EDU/docs/" # first part of htm

# open and read in sdl file
with open(path, "r") as file: 
    contents = file.read()
soup = BeautifulSoup(contents, 'xml')

# collect only the urls under HelpLink in .sdl file for each programming command
link = soup.find_all("HelpLink")

# iterate through each programming command url in .sdl, and add the first part of htm, which is path_to_topics
for data in link:
    data_str = str(data.get('url'))
    data_str = data_str.replace('\\', '/') 
    complete_path = path_to_topics + data_str
    sep = '#'
    complete_path = complete_path.split(sep, 1)[0] # remove characters starting from # and onwards
    topic_links.append(complete_path)

# using the complete paths to the .htm for each programming command, put the content onto 1 .pdf file
pdfkit.from_file(topic_links, 'out.pdf')
