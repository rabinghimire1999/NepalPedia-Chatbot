import os
import requests
from bs4 import BeautifulSoup

# URL from the britannica website
URL = "https://www.britannica.com/place/Nepal"

response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")
content =  soup.find("div", id = "-place-Nepal")

# extracting the content
text_content = ''
if content:
    paragraphs = content.find_all("p")
    for paragraphs in paragraphs:
        text_content += paragraphs.text + '\n'
        
# printing the scarped data 
# print(text_content.encode("utf-8"))

# saving the scraped data in .txt format
TEXT_FILE = "britinnacia.txt"

with open(os.path.join("./data/", TEXT_FILE), "w", encoding="utf-8") as file:
    file.write(text_content)
