from bs4 import BeautifulSoup
import os
import fungsi
import requests

def main_scraper(url,directory):
    fungsi.create_directory(directory) #Membuot Directory
    source_code = requests.get(url)
    source_text = source_code.text
    soup = BeautifulSoup(source_text,"html.parser")
    articles = soup.find_all("h3", {'class':'article__title'})
    articles2 = soup.find_all(True, {'class':['article_box','article_title']}) #Penvlison Multiple closs

    for article in articles:
        print("URL :"+ article.a.get("href"))
        print("Judul: "+ article.text)
        print()
    for article2 in articles2:
        print("URL2:"+article2.a.get("href"))
        print("Judul2 :"+ article2.text)
        print()
    
main_scraper('https://tekno.kompas.com/gadget', 'hasil')