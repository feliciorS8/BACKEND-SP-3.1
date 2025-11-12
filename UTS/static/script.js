// script.js — kontrol dasar interaksi CRUD Data Pasien Rumah Sakit

document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");

  if (form) {
    form.addEventListener("submit", (e) => {
      const nama = document.querySelector("#nama_pasien");
      const antrian = document.querySelector("#nomor_antrian");
      const kodePoli = document.querySelector("#kode_poli");

      // Validasi biar ga kosong
      if (!nama.value.trim() || !antrian.value.trim() || !kodePoli.value.trim()) {
        e.preventDefault();
        alert("❗ Semua field wajib diisi ya!");
        return;
      }

      // Validasi antrian harus angka
      if (isNaN(antrian.value)) {
        e.preventDefault();
        alert("⚠️ Nomor antrian harus berupa angka!");
        return;
      }
    });
  }

  // Konfirmasi saat klik tombol hapus
  const deleteLinks = document.querySelectorAll(".delete-link");
  deleteLinks.forEach(link => {
    link.addEventListener("click", (e) => {
      if (!confirm("Apakah kamu yakin ingin menghapus data ini? 😥")) {
        e.preventDefault();
      }
    });
  });
});
