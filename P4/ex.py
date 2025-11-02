from bs4 import BeautifulSoup
import os
import fungsi 
import requests

def main_scraper(url, directory):
    fungsi.create_directory(directory) 
    
    # mengambil Source Code dengan Error Handling
    try:
        source_code = requests.get(url, timeout=10)
        source_code.raise_for_status() # Cek status HTTP (misal: 404, 500)
        source_text = source_code.text
    except requests.exceptions.RequestException as e:
        print(f"❌ Error saat mengambil URL: {e}")
        return # keluar dr fungsi jika fail
    # 3. Parsing HTML
    soup = BeautifulSoup(source_text, "html.parser")
    
    # 4. Scraping Data dengan Nama Kelas yang Diperkirakan Benar
    
    # PENCARIAN 1: Cari tag h3 dengan class 'article__title'
    # Class asli : 'article_title article_title -- nedium' (salah ketik)
    # Class yang benar/umum digunakan di Kompas: 'article__title'
    articles = soup.find_all("h3", {'class':'article__title'}) 
    
    # PENCARIAN 2: Cari tag apa saja (True) yang memiliki salah satu class
    articles2 = soup.find_all(True, {'class':['article__box','article__title']})

    # 5. Cetak Hasil Pencarian 1
    print("\n--- Hasil Judul Berita (Pencarian 1: article__title) ---")
    if not articles:
        print("Judul tidak ditemukan. Cek kembali nama kelas HTML di Kompas.")
        
    for article in articles:
        # Tambahkan error handling untuk memastikan tag 'a' ada
        if article.a: 
            print("URL : " + article.a.get("href"))
            # Gunakan .strip() untuk membersihkan whitespace berlebihan pada judul
            print("Judul: " + article.text.strip()) 
            print("-" * 20)

    # 6. Cetak Hasil Pencarian 2
    print("\n--- Hasil Judul Berita (Pencarian 2: Multiple Class) ---")
    for article2 in articles2:
        if article2.a:
            print("URL2: " + article2.a.get("href"))
            print("Judul2: " + article2.text.strip())
            print("-" * 20)
            
# 7. Panggil Fungsi Utama
if __name__ == "__main__":
    main_scraper('https://tekno.kompas.com/gadget', 'hasil')