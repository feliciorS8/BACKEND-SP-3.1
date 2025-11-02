import os
import requests
from bs4 import BeautifulSoup
import time

def write_to_file(path, text):
    # pastikan foldernya ada
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def get_details(url):
    source_code = requests.get(url)
    soup = BeautifulSoup(source_code.text, "html.parser")
    paragraphs = soup.find_all("p")

    write_to_file("Cerpen Islami/artikel.doc", "Paragraf:\n")
    for p in paragraphs:
        write_to_file("Cerpen Islami/artikel.doc", p.text)
        print(p.text)
        print("-"*50)
    write_to_file("Cerpen Islami/artikel.doc", "-"*80 + "\n\n")

# contoh panggil fungsi
get_details("https://tekno.kompas.com/read/2024/05/01/140000/test-berita-gadget")
