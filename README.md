# Books to Scrape Scraper

Project ini merupakan scraper data buku menggunakan **Playwright dengan Python**. Program mengambil data buku, melakukan **data cleaning**, kemudian menyimpan hasilnya dalam format CSV.

## 1. Situs Target

**Link:** https://books.toscrape.com/

Data yang diambil:

* **Title**
* **Price**
* **Rating**

Jumlah data yang diambil dibatasi sebanyak **20 buku**.

## 2. Library yang Digunakan

Saya menggunakan **Playwright**.

Playwright dipilih karena project ini menggunakan Python sebagai bahasa pemrograman. Playwright menyediakan dukungan untuk Python sehingga dapat digunakan untuk mengotomatisasi browser dan mengambil data dari halaman website.

## 3. Data Cleaning

Data hasil scraping dibersihkan sebelum disimpan sebagai data akhir. Proses cleaning yang diterapkan meliputi:

* Menghapus **spasi berlebihan** pada judul buku.
* Menghapus **simbol mata uang (£)** dan mengubah harga menjadi **float**.
* Mengubah **rating dari teks menjadi integer**, contohnya `Three` menjadi `3`.
* Menangani **data yang kosong** dengan nilai pengganti `Unknown`.

Data hasil scraping disimpan sebagai `books_raw.csv`, sedangkan data setelah proses cleaning disimpan sebagai `books_clean.csv`.

## 4. Screenshot

### Sebelum Cleaning

Screenshot isi file `books_raw.csv`:

![Before Cleaning](screenshots/before-cleaning.png)

### Setelah Cleaning

Screenshot isi file `books_clean.csv`:

![After Cleaning](screenshots/after-cleaning.png)