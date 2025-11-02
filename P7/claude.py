import requests
from bs4 import BeautifulSoup
import os
import time

# Fungsi untuk membuat direktori/folder
def create_directory(directory):
    """Bikin folder baru kalau belum ada"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"✓ Folder '{directory}' berhasil dibuat!")
    else:
        print(f"✓ Folder '{directory}' sudah ada")

# Fungsi untuk cek apakah file sudah ada
def does_file_exist(filepath):
    """Cek apakah file sudah ada atau belum"""
    return os.path.exists(filepath)

# Fungsi untuk membuat file baru
def create_new_file(filepath):
    """Bikin file baru yang kosong"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("=== DAFTAR ARTIKEL ===\n\n")
    print(f"✓ File '{filepath}' berhasil dibuat!")

# Fungsi untuk menulis ke file
def write_to_file(filepath, content):
    """Tulis/tambahkan konten ke file"""
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(content)

# Fungsi untuk mengambil detail artikel
def get_details(url, directory):
    """Ambil detail lengkap dari setiap artikel"""
    try:
        print(f"  → Mengambil detail dari: {url}")
        
        # Kasih jeda biar ga keburu-buru request (etika scraping)
        time.sleep(1)
        
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Ambil judul artikel (sesuaikan dengan struktur HTML website)
        title = soup.find('h1')
        title_text = title.text.strip() if title else 'Tidak ada judul'
        
        # Ambil tanggal (sesuaikan selector-nya)
        date = soup.find('time') or soup.find('span', {'class': 'date'})
        date_text = date.text.strip() if date else 'Tidak ada tanggal'
        
        # Ambil konten artikel (sesuaikan selector-nya)
        content_div = soup.find('div', {'class': 'entry-content'}) or soup.find('article')
        content_text = content_div.text.strip()[:500] if content_div else 'Tidak ada konten'
        
        # Format detail artikel
        detail_format = f"""
{'='*60}
JUDUL: {title_text}
URL: {url}
TANGGAL: {date_text}
KONTEN (preview):
{content_text}...
{'='*60}

"""
        
        # Simpan detail ke file terpisah
        detail_file = directory + "/detail_artikel.txt"
        if not does_file_exist(detail_file):
            create_new_file(detail_file)
        
        write_to_file(detail_file, detail_format)
        print(f"  ✓ Detail artikel disimpan!")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error mengambil detail: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Error parsing detail: {e}")
        return False

# Fungsi utama scraper
def main_scraper(url, directory):
    """Fungsi utama untuk scraping website"""
    print(f"\n🚀 Memulai scraping dari: {url}")
    print(f"📁 Menyimpan ke folder: {directory}\n")
    
    # Buat folder
    create_directory(directory)
    
    try:
        # Ambil halaman utama
        print("📥 Mengambil halaman utama...")
        source_code = requests.get(url, timeout=10)
        source_text = source_code.text
        soup = BeautifulSoup(source_text, "html.parser")
        
        # Cari semua artikel dengan class 'post'
        articles = soup.find_all(True, {'class': 'post'})
        
        if not articles:
            print("⚠️ Tidak ada artikel ditemukan! Cek struktur HTML website.")
            return
        
        print(f"✓ Ditemukan {len(articles)} artikel!\n")
        
        # Loop setiap artikel
        for idx, article in enumerate(articles, 1):
            print(f"[{idx}/{len(articles)}] Memproses artikel...")
            
            # Ambil link artikel
            link_tag = article.find('a')
            if not link_tag or not link_tag.get('href'):
                print("  ⚠️ Artikel tidak punya link, skip...\n")
                continue
            
            article_url = link_tag.get('href')
            article_format = f"{idx}. URL: {article_url}\n"
            
            # Buat/tulis ke file daftar artikel
            artikel_file = directory + "/artikel.txt"
            if not does_file_exist(artikel_file):
                create_new_file(artikel_file)
            
            write_to_file(artikel_file, article_format)
            
            # Ambil detail artikel
            get_details(article_url, directory)
            
            print(f"  ✓ Artikel #{idx} selesai diproses!\n")
        
        print(f"\n🎉 Scraping selesai! Total {len(articles)} artikel berhasil disimpan.")
        print(f"📂 Cek folder '{directory}' untuk hasilnya.\n")
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error koneksi: {e}")
        print("Cek koneksi internet atau URL-nya mungkin salah.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

# Jalankan scraper
if __name__ == "__main__":
    print("="*60)
    print("WEB SCRAPER - CARPAN ISLAMI".center(60))
    print("="*60)
    
    # Konfigurasi
    target_url = "https://tekno.kompas.com/read/2025/10/28/17070027/google-cari-15-pengguna-pixel-garis-keras"
    save_folder = "Carpan Islami"
    
    # Mulai scraping
    main_scraper(target_url, save_folder)
    
    print("="*60)
    print("PROGRAM SELESAI".center(60))
    print("="*60)