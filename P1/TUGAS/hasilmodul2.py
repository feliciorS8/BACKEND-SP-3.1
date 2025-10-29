# Program ini akan terus meminta angka dan menambahkannya ke total
# sampai pengguna memasukkan 'exit' atau 'keluar'

def tambah_terus_menerus():
    total = 0  # Inisialisasi total dengan nilai 0
    print("Program penambahan berkelanjutan. Ketik 'exit' atau 'keluar' untuk berhenti.")

    while True:
        # Meminta input dari pengguna
        input_pengguna = input(f"Masukkan angka (total saat ini: {total}): ")
        
        # Menghentikan loop jika pengguna memasukkan 'exit'
        if input_pengguna.lower() in ('exit', 'keluar'):
            print(f"\nProgram selesai. Total akhir adalah: {total}")
            break # Menghentikan perulangan

        try:
            # Mengubah input menjadi angka
            angka_baru = float(input_pengguna)
            # Menambahkan angka baru ke total yang sudah ada
            total += angka_baru  # Ini adalah sintaks singkat dari total = total + angka_baru
            
        except ValueError:
            # Menangani jika input bukan angka
            print("Input tidak valid. Harap masukkan angka.")

# Memanggil fungsi untuk menjalankan program
tambah_terus_menerus()