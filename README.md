# NutriFood Dashboard

NutriFood Dashboard adalah aplikasi Streamlit untuk menganalisis bahan pangan Indonesia berdasarkan kategori, kandungan gizi, harga, dan `skor_kesehatan`. Dashboard ini membantu pengguna membandingkan bahan pangan secara lebih objektif sebelum menyusun rekomendasi menu.

## Ringkasan Proyek

Permasalahan utama yang diangkat adalah sulitnya memilih bahan pangan yang seimbang antara kebutuhan gizi dan keterjangkauan harga. Solusi yang dikembangkan adalah dashboard analisis berbasis data yang menampilkan pola kategori bahan pangan, protein tertinggi, harga terendah, kalori tertinggi, skor kesehatan, serta hasil A/B testing sederhana.

Analisis utama pada proyek ini menjawab enam pertanyaan bisnis:

1. Bagaimana distribusi kategori bahan pangan dalam dataset?
2. Bahan pangan apa saja yang memiliki protein tertinggi per 100 gram?
3. Bahan pangan apa saja yang memiliki harga paling rendah?
4. Bahan pangan apa saja yang memiliki kalori tertinggi?
5. Bahan pangan apa saja yang memiliki `skor_kesehatan` tertinggi?
6. Apakah rata-rata `skor_kesehatan` makanan murah berbeda dengan makanan mahal?

## Fitur Aplikasi

- Ringkasan jumlah data, jumlah kategori, rata-rata harga, dan rata-rata `skor_kesehatan`.
- Visualisasi distribusi kategori bahan pangan.
- Tabel dan grafik top 10 bahan pangan berdasarkan protein, harga, kalori, dan `skor_kesehatan`.
- A/B testing sederhana untuk membandingkan `skor_kesehatan` kelompok bahan pangan murah dan mahal.
- Ringkasan EDA per kategori.
- Data dictionary dan data model-ready.
- Sidebar navigasi untuk berpindah antarbagian dashboard.

## Struktur Project

```text
.
├── app.py
├── main.py
├── main.ipynb
├── requirements.txt
├── data/
│   ├── data_set_bahan_pangan_1000.xlsx
│   └── data_final_identik.csv
└── output/
```

Keterangan file utama:

- `app.py`: aplikasi Streamlit.
- `main.py`: script analisis data.
- `main.ipynb`: notebook analisis dengan struktur pembahasan yang lebih naratif.
- `requirements.txt`: daftar library Python untuk menjalankan aplikasi.
- `data/data_set_bahan_pangan_1000.xlsx`: dataset utama yang digunakan dashboard.

## Kebutuhan Sistem

Gunakan Python 3.10 sampai 3.12 agar proses instalasi dependency lebih stabil.

Library yang digunakan:

```text
streamlit
pandas
matplotlib
scipy
openpyxl
```

## Menjalankan di Lokal

Clone repository, lalu masuk ke folder project:

```bash
git clone <url-repository>
cd <nama-folder-project>
```

Buat virtual environment:

```bash
python -m venv .venv
```

Aktifkan virtual environment.

Untuk Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Untuk macOS atau Linux:

```bash
source .venv/bin/activate
```

Install dependency:

```bash
pip install -r requirements.txt
```

Jalankan aplikasi Streamlit:

```bash
python -m streamlit run app.py
```

Jika ingin menentukan port secara manual:

```bash
python -m streamlit run app.py --server.port 8501
```

Setelah berjalan, buka alamat berikut di browser:

```text
http://localhost:8501
```

## Menjalankan Analisis

Untuk menjalankan analisis melalui script Python:

```bash
python main.py
```

Script ini akan menghasilkan beberapa file output, seperti:

- `data_final.csv`
- `data_dictionary.csv`
- `data_model_ready.csv`
- `ab_testing_result.csv`

Untuk membaca analisis secara lebih terstruktur, buka file `main.ipynb` melalui Jupyter Notebook atau Visual Studio Code.

## Deploy ke Streamlit Community Cloud

Sebelum deploy, pastikan file berikut sudah masuk ke repository:

- `app.py`
- `requirements.txt`
- folder `data/`
- `main.py` dan `main.ipynb` jika ingin menyertakan analisis lengkap

Langkah deploy:

1. Push project ke GitHub.
2. Buka Streamlit Community Cloud.
3. Pilih repository project.
4. Pada bagian main file, isi dengan:

```text
app.py
```

5. Jalankan deploy.

Streamlit akan membaca `requirements.txt`, menginstall dependency, lalu menjalankan `app.py`.

Jika deploy memilih versi Python yang terlalu baru dan dependency gagal terinstall, gunakan Python 3.12 melalui pengaturan environment atau tambahkan file `runtime.txt` berisi:

```text
python-3.12
```

## Catatan Data

Dashboard dapat berjalan meskipun `data_final.csv` belum tersedia. Jika file tersebut tidak ditemukan, aplikasi akan membentuk data final langsung dari `data/data_set_bahan_pangan_1000.xlsx`.

Kolom `skor_kesehatan` dibuat dengan rumus:

```text
(protein * 2) + karbo - lemak
```

Skor ini digunakan sebagai fitur sederhana untuk membantu pemeringkatan bahan pangan berdasarkan kombinasi protein, karbohidrat, dan lemak.

