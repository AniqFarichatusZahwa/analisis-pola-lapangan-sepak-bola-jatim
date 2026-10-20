# Analisis Pola Pemanfaatan Lapangan Sepak Bola di Jawa Timur

Project akhir Data Warehousing untuk mengintegrasikan data pertandingan sepak bola dan karakteristik fasilitas di Jawa Timur. Data diolah menggunakan DuckDB, diintegrasikan ke DuckLake, lalu disajikan melalui dashboard interaktif Streamlit.

## Tujuan Project

Project ini bertujuan menganalisis persebaran venue dan jumlah pertandingan yang tercatat berdasarkan kompetisi serta karakteristik fasilitas. Analisis mencakup:

- Persebaran stadion dan lapangan sepak bola yang digunakan dalam kompetisi.
- Venue dengan jumlah pertandingan tercatat terbanyak dan paling sedikit.
- Perbandingan aktivitas pertandingan Piala Soeratin, Liga 1, dan Piala AFF U-19.
- Distribusi pertandingan Piala Soeratin berdasarkan kelompok usia U-13, U-15, dan U-17.
- Eksplorasi hubungan luas lapangan dan kapasitas penonton dengan jumlah pertandingan yang tercatat.

> **Batasan data:** jumlah pertandingan menggambarkan pertandingan yang tercakup dalam dataset project, bukan seluruh aktivitas sepak bola di Jawa Timur. Data luas, kapasitas, koordinat, dan informasi venue dapat tidak lengkap.

## Dataset

Project menggunakan empat kelompok data yang disebut **4 Bebek**.

| Kelompok data | Sumber | File CSV | Database DuckDB | Cakupan |
|---|---|---|---|---|
| Bebek Fasilitas | [Open Data Surabaya](https://opendata.surabaya.go.id/kumpulan_dataset/z001-10646-3), PSSI Jawa Timur, dan sumber fasilitas resmi lainnya | `data_lapangan.csv` | `bebek_fasilitas.duckdb` | 67 stadion/lapangan yang tercatat |
| Bebek Soeratin | [PSSI Jawa Timur](https://pssijatim.com/) | `data_event_soeratin.csv` | `bebek_soeratin.duckdb` | 824 pertandingan U-13, U-15, dan U-17 |
| Bebek Liga 1 | [Liga Indonesia Baru](https://www.ligaindonesiabaru.com/) | `data_event_liga1.csv` | `bebek_liga1.duckdb` | 34 pertandingan Persebaya pada musim 2023/2024 dan 2024/2025 |
| Bebek AFF U-19 | [Bola.net](https://www.bola.net/tim_nasional/hasil-lengkap-klasemen-dan-top-skor-piala-aff-u-19-2024-indonesia-767c10.html) | `data_event_aff.csv` | `bebek_aff.duckdb` | 17 pertandingan Piala AFF U-19 2024 |

Rincian data Soeratin:

| Kelompok usia | Jumlah pertandingan |
|---|---:|
| U-13 | 135 |
| U-15 | 144 |
| U-17 | 545 |
| **Total** | **824** |

Cakupan Liga 1 terbatas pada pertandingan Persebaya yang dikumpulkan untuk project, bukan seluruh pertandingan Liga 1. Terdapat pertandingan Soeratin yang belum memiliki informasi venue. Nilai fasilitas yang tidak diketahui diperlakukan sebagai data kosong, bukan nol.

## Teknologi

- **Python** — pembersihan dan transformasi data.
- **DuckDB** — database lokal untuk setiap kelompok data.
- **DuckLake** — pengelolaan katalog dan penyimpanan data analitik terintegrasi.
- **Streamlit** — aplikasi dashboard.
- **Pandas** — pengolahan data.
- **Plotly** — grafik interaktif.
- **PyDeck** — visualisasi peta.

## Arsitektur Project

```text
Sumber data publik
    |
    v
CSV (data mentah)
    |
    v
4 database DuckDB
    |
    v
Pembersihan dan transformasi (ETL)
    - standardisasi tanggal dan kolom
    - pemeriksaan duplikasi
    - standardisasi nama venue
    - pembuatan venue_id
    - pencocokan event dengan fasilitas
    |
    v
DuckLake
    - shared_catalog.ducklake
    - lakehouse_storage/
    |
    v
Tabel analitik
    - analytics.fact_event
    - fasilitas.dim_venue
    - analytics.mart_aktivitas_venue
    - analytics.mart_kompetisi_venue
    - analytics.mart_karakteristik_venue
    |
    v
Dashboard Streamlit
```

### Struktur DuckLake

| Schema | Tabel | Kegunaan |
|---|---|---|
| `soeratin` | `event_soeratin` | Data pertandingan Soeratin yang sudah diproses |
| `liga1` | `event_liga1` | Data pertandingan Liga 1 yang sudah diproses |
| `aff` | `event_aff` | Data pertandingan AFF U-19 yang sudah diproses |
| `fasilitas` | `dim_venue` | Identitas dan karakteristik venue |
| `analytics` | `fact_event` | Data pertandingan terintegrasi |
| `analytics` | `mart_aktivitas_venue` | Agregasi jumlah pertandingan per venue |
| `analytics` | `mart_kompetisi_venue` | Perbandingan aktivitas per venue dan kompetisi |
| `analytics` | `mart_karakteristik_venue` | Data untuk analisis karakteristik fasilitas dan aktivitas |

## Struktur Folder

```text
analisis-pola-lapangan-sepak-bola-jatim/
├── app.py
├── requirements.txt
├── shared_catalog.ducklake
├── lakehouse_storage/
├── data/
│   ├── raw/
│   │   ├── data_lapangan.csv
│   │   ├── data_event_soeratin.csv
│   │   ├── data_event_liga1.csv
│   │   └── data_event_aff.csv
│   └── duckdb/
│       ├── bebek_fasilitas.duckdb
│       ├── bebek_soeratin.duckdb
│       ├── bebek_liga1.duckdb
│       └── bebek_aff.duckdb
└── src/
    ├── load_duckdb.py
    ├── integrasi_data.py
    └── buat_mart.py
```

> Struktur di atas menggambarkan susunan utama project. File diagnostik atau file pendukung lain dapat berada di folder `src/` atau folder project.

## Menjalankan Project Secara Lokal

### 1. Clone repository

```bash
git clone https://github.com/AniqFarichatusZahwa/analisis-pola-lapangan-sepak-bola-jatim.git
cd analisis-pola-lapangan-sepak-bola-jatim
```

### 2. Buat virtual environment (opsional, disarankan)

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Jika PowerShell menolak aktivasi karena kebijakan eksekusi, gunakan terminal lain atau sesuaikan kebijakan sesuai pengaturan perangkat.

### 3. Instal dependensi

```bash
pip install -r requirements.txt
```

### 4. Pastikan file data tersedia

Pastikan CSV di `data/raw/`, database DuckDB di `data/duckdb/`, serta katalog `shared_catalog.ducklake` dan data pada `lakehouse_storage/` tersedia sesuai kebutuhan project.

### 5. Jalankan dashboard

```bash
streamlit run app.py
```

Dashboard akan terbuka pada alamat lokal yang ditampilkan di terminal oleh Streamlit.

## Alur Pemrosesan Data

Script utama yang digunakan dalam alur data:

1. `src/load_duckdb.py` — memuat dataset ke database DuckDB lokal.
2. `src/integrasi_data.py` — membersihkan, menstandardisasi, dan mengintegrasikan data ke DuckLake.
3. `src/buat_mart.py` — membentuk tabel data mart untuk analisis.
4. `app.py` — membaca tabel DuckLake dan menampilkan dashboard.

Urutan ini menjelaskan alur kerja yang dirancang untuk project. Sebelum menjalankan ulang script integrasi atau pembuatan mart, pastikan memahami apakah script akan membuat ulang atau mengubah tabel yang sudah ada.

## Dashboard

Dashboard Streamlit menyediakan halaman analisis untuk:

- **Activity Overview** — ringkasan jumlah pertandingan, venue, kompetisi, dan venue dengan aktivitas tertinggi.
- **Venue Distribution Map** — peta interaktif persebaran venue berdasarkan koordinat yang tersedia.
- **Competition Analysis** — perbandingan pertandingan berdasarkan kompetisi dan kelompok usia.
- **Facility Analysis** — eksplorasi luas lapangan, kapasitas penonton, dan jumlah pertandingan pada venue yang memiliki data relevan.

Ketersediaan visualisasi mengikuti kelengkapan data yang tersedia. Hubungan antara karakteristik fasilitas dan jumlah pertandingan bersifat eksploratif dan tidak menunjukkan sebab-akibat secara langsung.

## Deployment ke Streamlit Community Cloud

Dashboard dapat dipublikasikan melalui [Streamlit Community Cloud](https://share.streamlit.io/) dengan repository GitHub.

1. Pastikan `app.py`, `requirements.txt`, katalog DuckLake, dan file data yang dibutuhkan tersedia pada repository atau pada penyimpanan yang dapat diakses oleh aplikasi.
2. Buka Streamlit Community Cloud dan hubungkan akun GitHub.
3. Pilih repository project, branch `main`, dan file utama `app.py`.
4. Deploy aplikasi dan periksa log apabila terjadi error.
5. Setelah perubahan kode didorong ke GitHub, tunggu Streamlit menyelesaikan deployment ulang.

### Catatan penting untuk DuckLake di cloud

Streamlit Community Cloud menjalankan aplikasi pada server jarak jauh, sehingga **tidak dapat membaca folder lokal Windows**, misalnya `C:/Users/HP/...` dari laptop pengembang.

- Gunakan path yang mengacu pada direktori project, bukan path absolut milik laptop.
- Pastikan file Parquet yang dirujuk oleh metadata DuckLake benar-benar tersedia pada server.
- Jika katalog masih menyimpan lokasi data lama, koneksi DuckLake mungkin perlu mengatur ulang lokasi data menggunakan konfigurasi `DATA_PATH` dan `OVERRIDE_DATA_PATH` yang sesuai dengan versi DuckLake dan struktur penyimpanan.
- Mengubah path pada Python saja tidak akan memulihkan file Parquet yang belum tersedia di server.
- Jangan menghapus `shared_catalog.ducklake` atau `lakehouse_storage/` tanpa memastikan cadangan dan memahami dampaknya terhadap tabel.

## Keterbatasan Data

- Data pertandingan hanya mencakup kompetisi dan periode yang dikumpulkan untuk project.
- Data Liga 1 berfokus pada pertandingan Persebaya Surabaya pada dua musim yang disebutkan.
- Sebagian pertandingan belum memiliki informasi venue atau belum berhasil dicocokkan.
- Luas lapangan, kapasitas penonton, alamat, dan koordinat tidak tersedia untuk seluruh venue.
- Jumlah pertandingan tercatat tidak selalu mewakili seluruh aktivitas aktual suatu venue.