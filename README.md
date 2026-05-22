# OmniConvert v1.2 - Personal Batch Converter

OmniConvert adalah aplikasi desktop berbasis Python yang dirancang untuk melakukan konversi file secara massal (*batch conversion*) dengan antarmuka pengguna (GUI) yang modern, gelap, dan responsif. Aplikasi ini membagi file ke dalam beberapa kategori utama (Gambar, Dokumen, Presentasi, dan Script) untuk memudahkan manajemen alur kerja.

  ## Fitur Utama
- **Konversi Massal Mandiri**: Mengonversi banyak file sekaligus dalam satu kali klik.
- **Deteksi Kategori Otomatis**: Memindai folder sumber dan mengelompokkan file secara otomatis berdasarkan ekstensinya.
- **Log Terminal Real-time**: Menampilkan status proses konversi baris demi baris secara langsung.
- **Lokal**: Semua proses konversi dilakukan 100% di komputer lokal Anda tanpa mengunggah file ke internet.

  ## Dukungan Format Konversi

| Kategori | Format Asal | Target Konversi |
| :--- | :--- | :--- |
| **Gambar** | `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp` | `PNG`, `JPG`, `WEBP`, `PDF` |
| **Dokumen** | `.docx`, `.pdf`, `.txt` | `PDF`, `DOCX`, `TXT` |
| **Presentasi** | `.ppt`, `.pptx` | `PDF` |
| **Script** | `.py` | `PDF`, `TXT` |

  ## Panduan Instalasi (Menjalankan dari Source Code)

### 1. Prasyarat
Pastikan Anda sudah menginstal Python (versi 3.8 atau yang lebih baru) di komputer Anda.

### 2. Instalasi Library Pendukung
Buka Terminal atau Command Prompt di folder proyek Anda, lalu jalankan perintah berikut untuk menginstal semua *dependencies*:

```bash
pip install customtkinter Pillow pdf2docx pypdf fpdf pywin32
