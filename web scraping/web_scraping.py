import os
import requests
from bs4 import BeautifulSoup

# URL of the Wikipedia about Nepal
URL = "https://en.wikipedia.org/wiki/Nepal"

response = requests.get(URL)
soup = BeautifulSoup(response.content,"html.parser")
content = soup.find("div", id = "mw-content-text")


#extracting the text content
text_content = ''
if content:
    paragraphs = content.find_all("p")
    for paragraphs in paragraphs:
        text_content += paragraphs.text + "\n"
        
# printing the scraped-data.
# print(text_content.encode("utf-8"))

# saving the scraped data in .txt format
TEXT_FILE = "wikipedia_text.txt"

with open(os.path.join("./data/", TEXT_FILE), "w", encoding="utf-8") as file:
    file.write(text_content)
