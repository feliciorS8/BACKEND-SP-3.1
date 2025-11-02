from bs4 import BeautifulSoup   #buat baca dan ambil data dari HTML (alat pengambil isi web
import requests             #buat minta data dari web pake pyhton  
import os                   #bikinfolder atau file otomatis
import time                 #buat jeda waktu biar ga numpuk requestnya

# ===============================
#  FUNGSI UNTUK NULIS KE FILE doc atau world
# ===============================
def write_to_file(path, text):
    # Bikin folder kalau belum ada
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Tambahkan teks ke file .doc
    with open(path, "a", encoding="utf-8") as f:      #(a) itu appaend jadi klo dijalankan terus bakal namabah TAPII kalo pake W nanti bis kehapus
        f.write(text + "\n")

# ==================================
#  FUNGSI AMBIL ISI BERITA PER ARTIKEL
# ==================================
def get_details(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Cari semua paragraf isi berita
        paragraphs = soup.find_all("p")    #mengambil semua paragraf dalam artikel tsb
        isi = "\n".join([p.get_text(strip=True) for p in paragraphs])    #mengambil strip tnapa tag html

        return isi if isi else "(Isi berita tidak ditemukan)"
    except Exception as e:
        return f"(Gagal mengambil isi berita: {e})"

# ==================================
#  FUNGSI UTAMA UNTUK SCRAPING
# ==================================
def main_scraper(url):
    print("🔎 Mengambil data dari berita:", url)
    folder = "menyimpan isi berita P7"
    file_path = os.path.join(folder, "artikel.doc")   # nama lokasi world hasil scraping

    # Buat file baru kosong
    os.makedirs(folder, exist_ok=True)
    open(file_path, "w", encoding="utf-8").close()

    # Ambil halaman utama
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Cari semua artikel di halaman Kompas Gadget
    articles = soup.find_all("h3", {'class': "article__title"})

    for i, article in enumerate(articles[:5], start=1):
        link = article.a.get("href")
        title = article.text.strip()
        print(f"\n{i}. {title}")
        print(f"   URL: {link}")

        # Ambil isi berita lengkap
        isi = get_details(link)

        # Tulis ke file Word
        write_to_file(file_path, f"Judul: {title}")
        write_to_file(file_path, f"URL: {link}")
        write_to_file(file_path, "Paragraf:\n")
        write_to_file(file_path, isi)
        write_to_file(file_path, "-" * 100 + "\n")

        print("✅ Disimpan ke Word\n")

        # kasih jeda biar gak kebanyakan request
        time.sleep(1.5)

    print(f"\n🎉 Semua berita berhasil disimpan ke: {file_path}")

# ==================================
#  JALANKAN PROGRAM
# ==================================
main_scraper("https://tekno.kompas.com/gadget")