# Mengimpor modul-modul yang telah dibuat
import penambahan
import pengurangan
import perkalian
import pembagian

# Meminta input dari pengguna
try:
    angka_pertama = float(input("Masukkan angka pertama: "))
    angka_kedua = float(input("Masukkan angka kedua: "))

    # Melakukan perhitungan menggunakan fungsi dari modul
    hasil_tambah = penambahan.tambah(angka_pertama, angka_kedua)
    hasil_kurang = pengurangan.kurang(angka_pertama, angka_kedua)
    hasil_kali = perkalian.kali(angka_pertama, angka_kedua)
    hasil_bagi = pembagian.bagi(angka_pertama, angka_kedua)

    # Menampilkan hasil
    print(f"Penambahan dari {angka_pertama} dan {angka_kedua} adalah {hasil_tambah}")
    print(f"Pengurangan dari {angka_pertama} dan {angka_kedua} adalah {hasil_kurang}")
    print(f"Perkalian dari {angka_pertama} dan {angka_kedua} adalah {hasil_kali}")
    print(f"Pembagian dari {angka_pertama} dan {angka_kedua} adalah {hasil_bagi}")

except ValueError:
    print("Input yang Anda masukkan tidak valid. Harap masukkan angka.")