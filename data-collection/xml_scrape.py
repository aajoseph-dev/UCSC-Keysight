from bs4 import BeautifulSoup


file = open("/Users/shaun/Desktop/115b/UCSC-Keysight/documents/EDU36311A_K_01_04_03_01_00_01_04_01_01-v3/EDU36311A.sdl", "r")
contents = file.read()
soup = BeautifulSoup(contents, 'xml')

link = soup.find_all("HelpLink")

with open('myfile23.txt', 'w+') as f:
    for data in link:
        f.write(data.get("url"))
        f.write("\n")

f.close()
