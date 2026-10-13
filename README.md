# Analisis Pola Pemanfaatan Lapangan Sepak Bola di Jawa Timur

Project ini merupakan project akhir Data Warehousing yang mengintegrasikan data pertandingan sepak bola dan karakteristik fasilitas olahraga di Jawa Timur untuk menganalisis pola pemanfaatan lapangan berdasarkan aktivitas event dan karakteristik fasilitas. Project ini menggunakan **DuckDB, DuckLake, dan Streamlit** untuk mendukung proses penyimpanan, pengolahan, integrasi, analisis, dan visualisasi data.

## Kelompok Data: 4 Bebek

Project ini menggunakan empat kelompok data utama yang disebut sebagai **4 Bebek**:

1. **Bebek Fasilitas** — data karakteristik stadion dan lapangan sepak bola, meliputi nama venue, lokasi administratif, alamat, luas lapangan, dan kapasitas penonton. Sumber data mencakup [Open Data Surabaya](https://opendata.surabaya.go.id/kumpulan_dataset/z001-10646-3) serta sumber resmi lain yang relevan untuk melengkapi informasi fasilitas di Jawa Timur.
2. **Bebek Soeratin** — data pertandingan Piala Soeratin kelompok usia U-13, U-15, dan U-17 yang bersumber dari [PSSI Jawa Timur](https://pssijatim.com/).
3. **Bebek Liga 1** — data pertandingan Liga 1 Indonesia musim 2023/2024 dan 2024/2025 yang bersumber dari [Liga Indonesia Baru](https://www.ligaindonesiabaru.com/).
4. **Bebek AFF U-19** — data pertandingan Piala AFF U-19 tahun 2024 yang bersumber dari [Bola.net](https://www.bola.net/).

## Arsitektur Data Warehouse

Keempat kelompok data akan disimpan terlebih dahulu dalam database DuckDB masing-masing. Selanjutnya, data melalui proses *Extract, Transform, Load* (ETL), termasuk pembersihan data, standardisasi nama venue, dan validasi informasi pertandingan maupun fasilitas.

Data yang telah dibersihkan kemudian diintegrasikan ke dalam DuckLake untuk membentuk penyimpanan data analitik terpusat. Integrasi dilakukan dengan menyelaraskan identitas venue agar data pertandingan dari berbagai kompetisi dapat dihubungkan dengan karakteristik fasilitas yang sesuai.

## Analisis dan Visualisasi

Data yang telah terintegrasi digunakan untuk:

- Menganalisis jumlah pertandingan yang tercatat pada setiap venue.
- Membandingkan aktivitas pertandingan antara Soeratin, Liga 1, dan AFF U-19.
- Mengidentifikasi persebaran stadion dan lapangan sepak bola di Jawa Timur.
- Mengeksplorasi keterkaitan antara karakteristik fasilitas, seperti luas lapangan dan kapasitas penonton, dengan jumlah pertandingan yang tercatat.

Hasil analisis akan disajikan melalui dashboard interaktif berbasis **Streamlit**, termasuk peta persebaran venue sepak bola di Jawa Timur.

## Teknologi yang Digunakan

- **Python** — pemrosesan dan analisis data.
- **DuckDB** — penyimpanan dan pengolahan data pada masing-masing kelompok.
- **DuckLake** — integrasi dan pengelolaan data analitik.
- **Pandas** — pembersihan, transformasi, dan integrasi data.
- **Streamlit** — pengembangan dashboard interaktif.
- **Plotly** — visualisasi data dan peta persebaran venue.

## Tujuan Project

Project ini bertujuan membangun sebuah **data warehouse aktivitas pertandingan dan karakteristik fasilitas lapangan sepak bola di Jawa Timur** yang memungkinkan pengguna untuk melihat persebaran venue serta intensitas pertandingan berdasarkan kompetisi dan karakteristik fasilitas.

Analisis diarahkan untuk menjawab pertanyaan seperti:

- Bagaimana persebaran stadion dan lapangan sepak bola yang digunakan dalam kompetisi di Jawa Timur?
- Venue mana yang memiliki jumlah pertandingan tercatat paling banyak dan paling sedikit?
- Bagaimana perbandingan aktivitas pertandingan antara Piala Soeratin, Liga 1, dan Piala AFF U-19?
- Bagaimana distribusi pertandingan Piala Soeratin berdasarkan kelompok usia U-13, U-15, dan U-17?
- Kabupaten/kota mana yang memiliki konsentrasi venue dengan aktivitas pertandingan paling tinggi?
- Bagaimana distribusi jumlah pertandingan pada setiap venue berdasarkan kompetisi yang diikuti?
- Bagaimana perbedaan karakteristik fasilitas, seperti luas lapangan dan kapasitas penonton, ant venue di Jawa Timur?
- Apakah venue dengan kapasitas penonton lebih besar cenderung memiliki jumlah pertandingan tercatat lebih banyak?
- Apakah terdapat pola hubungan antara luas lapangan dan intensitas aktivitas pertandingan pada venue yang memiliki data luas?
- Venue mana yang memiliki aktivitas pertandingan tinggi meskipun kapasitas atau luas fasilitasnya relatif terbatas?
- Bagaimana pola persebaran venue berdasarkan jumlah pertandingan dan karakteristik fasilitas melalui peta interaktif?
- Bagaimana integrasi data dari berbagai sumber dapat membantu menghasilkan informasi yang lebih terstruktur mengenai aktivitas pertandingan dan fasilitas sepak bola di Jawa Timur?

**Catatan:** Jumlah pertandingan merepresentasikan aktivitas yang tercatat dalam sumber dan kompetisi yang digunakan. Angka tersebut tidak serta-merta menggambarkan seluruh pemanfaatan lapangan sepak bola di Jawa Timur.

## Dataset

Project ini menggunakan empat kelompok data utama yang disebut sebagai **“4 Bebek”**, yaitu data pertandingan Piala Soeratin, Liga 1 Indonesia, Piala AFF U-19, dan karakteristik fasilitas lapangan sepak bola di Jawa Timur.

### 1. Bebek Fasilitas — Data Karakteristik Stadion dan Lapangan Sepak Bola

**Sumber:**

- [Open Data Surabaya — Sarana dan Prasarana Olahraga](https://opendata.surabaya.go.id/kumpulan_dataset/z001-10646-3)
- [PSSI Jawa Timur](https://pssijatim.com/)
- Sumber resmi pemerintah daerah dan pengelola fasilitas olahraga yang relevan.

**Dataset:** `data_lapangan.csv`  
**Database DuckDB:** `bebek_fasilitas.duckdb`

Dataset ini berisi informasi karakteristik 67 stadion dan lapangan sepak bola yang tercatat dalam data penelitian. Informasi tersebut digunakan untuk mengidentifikasi lokasi venue, membandingkan fasilitas olahraga, dan menghubungkan karakteristik fasilitas dengan aktivitas pertandingan.

**Variabel dataset:**

| Variabel | Keterangan |
|:---|:---|
| `nama_venue` | Nama stadion atau lapangan |
| `jumlah_event` | Jumlah pertandingan yang tercatat |
| `kecamatan` | Kecamatan lokasi fasilitas |
| `kelurahan` | Kelurahan lokasi fasilitas |
| `nama_fasilitas_olahraga` | Nama fasilitas olahraga |
| `alamatlokasi` | Alamat fasilitas |
| `luas_m2` | Luas dalam meter persegi |
| `kapasitas_penonton` | Kapasitas penonton |

Dataset fasilitas digunakan sebagai tabel referensi untuk menghubungkan data pertandingan dengan lokasi dan karakteristik venue. Informasi luas dan kapasitas diperiksa berdasarkan ketersediaan sumber; nilai yang belum diketahui akan ditangani sebagai data kosong dan tidak diasumsikan sebagai nol.

### 2. Bebek Soeratin — Data Pertandingan Piala Soeratin

**Sumber:** PSSI Jawa Timur

- [Piala Soeratin U-13](https://pssijatim.com/page-piala-soeratin-u-13)
- [Piala Soeratin U-15](https://pssijatim.com/page-piala-soeratin-u-15)
- [Piala Soeratin U-17](https://pssijatim.com/page-piala-soeratin-u-17)

**Dataset:** `data_event_soeratin.csv`  
**Database DuckDB:** `bebek_soeratin.duckdb`

Dataset ini berisi data pertandingan Piala Soeratin kelompok usia U-13, U-15, dan U-17 di Jawa Timur. Informasi yang dikumpulkan meliputi identitas pertandingan, nama kompetisi, tanggal pertandingan, nama venue, level atau babak kompetisi, tim yang bertanding, hasil skor, dan sumber informasi.

**Data yang tersedia saat ini:**

| Kelompok Usia | Jumlah Pertandingan |
|:---|---:|
| U-13 | 135 |
| U-15 | 144 |
| U-17 | 545 |
| **Total** | **824** |

**Variabel dataset:**

| Variabel | Keterangan |
|:---|:---|
| `id_event` | Identitas unik pertandingan |
| `nama_event` | Nama kompetisi |
| `tanggal_mulai` | Tanggal pertandingan |
| `tanggal_selesai` | Tanggal selesai event |
| `nama_venue` | Nama stadion atau lapangan |
| `level_event` | Tingkat atau babak kompetisi |
| `peserta_tim` | Tim yang bertanding |
| `hasil_skor` | Hasil pertandingan |
| `sumber` | URL sumber informasi |

Dataset ini digunakan untuk menganalisis distribusi pertandingan berdasarkan kelompok usia, jumlah event per venue, dan persebaran lokasi pertandingan. Terdapat 20 pertandingan yang belum memiliki informasi venue dan perlu ditangani pada tahap pembersihan data.

### 3. Bebek Liga 1 — Data Pertandingan Liga 1 Indonesia

**Sumber:** Liga Indonesia Baru

- [Liga 1 musim 2023/2024 — Persebaya Surabaya](https://www.ligaindonesiabaru.com/clubs/single/BRI_LIGA_1_2023-2024/PERSEBAYA_SURABAYA)
- [Liga 1 musim 2024/2025 — Persebaya Surabaya](https://www.ligaindonesiabaru.com/clubs/single/BRI_LIGA_1_2024-25/PERSEBAYA_SURABAYA)

**Dataset:** `data_event_liga 1.csv`  
**Database DuckDB:** `bebek_liga1.duckdb`

Dataset ini berisi catatan pertandingan Persebaya Surabaya pada kompetisi Liga 1 Indonesia musim 2023/2024 dan 2024/2025. Data mencakup tanggal pertandingan, nama venue, tim yang bertanding, hasil skor, dan sumber informasi.

**Data yang tersedia saat ini:**

| Musim Kompetisi | Jumlah Pertandingan |
|:---|---:|
| 2023/2024 | 17 |
| 2024/2025 | 17 |
| **Total** | **34** |

**Variabel dataset:**

| Variabel | Keterangan |
|:---|:---|
| `id_event` | Identitas unik pertandingan |
| `nama_event` | Nama kompetisi dan musim |
| `tanggal_mulai` | Tanggal pertandingan |
| `tanggal_selesai` | Tanggal selesai event |
| `nama_venue` | Nama stadion |
| `level_event` | Tingkat kompetisi |
| `peserta_tim` | Tim yang bertanding |
| `hasil_skor` | Hasil pertandingan |
| `sumber` | URL sumber informasi |

Data ini digunakan sebagai pembanding aktivitas pertandingan pada kompetisi liga profesional. Cakupan datanya terbatas pada pertandingan Persebaya Surabaya yang tercatat dalam dataset, bukan keseluruhan pertandingan Liga 1 Indonesia.

### 4. Bebek AFF U-19 — Data Pertandingan Piala AFF U-19 2024

**Sumber:** Bola.net

- [Hasil Lengkap, Klasemen, dan Top Skor Piala AFF U-19 2024](https://www.bola.net/tim_nasional/hasil-lengkap-klasemen-dan-top-skor-piala-aff-u-19-2024-indonesia-767c10.html)

**Dataset:** `data_event_aff.csv`  
**Database DuckDB:** `bebek_aff.duckdb`

Dataset ini berisi catatan pertandingan Piala AFF U-19 tahun 2024. Informasi yang tersedia meliputi identitas pertandingan, nama kompetisi, tanggal pertandingan, venue, status kompetisi, tim yang bertanding, hasil skor, dan sumber informasi.

**Data yang tersedia saat ini:**

| Keterangan | Jumlah |
|:---|---:|
| Tahun kompetisi | 2024 |
| Jumlah pertandingan | 17 |

**Variabel dataset:**

| Variabel | Keterangan |
|:---|:---|
| `id_event` | Identitas unik pertandingan |
| `nama_event` | Nama kompetisi |
| `tanggal_mulai` | Tanggal pertandingan |
| `tanggal_selesai` | Tanggal selesai event |
| `nama_venue` | Nama stadion atau lapangan |
| `level_event` | Tingkat kompetisi |
| `peserta_tim` | Tim yang bertanding |
| `hasil_skor` | Hasil pertandingan |
| `sumber` | URL sumber informasi |

Data AFF U-19 digunakan untuk mengidentifikasi aktivitas pertandingan internasional yang berlangsung di venue di Jawa Timur serta membandingkannya dengan aktivitas kompetisi lainnya.

## 🔗 Integrasi Empat Kelompok Data

Keempat kelompok data memiliki karakteristik dan tingkat granularitas yang berbeda:

| Sumber | Cakupan | Unit Data | Detail |
|:---|:---|:---|:---|
| Bebek Fasilitas | Stadion dan lapangan sepak bola dalam dataset penelitian di Jawa Timur | Venue/fasilitas | Nama fasilitas, lokasi administratif, alamat, luas lapangan, dan kapasitas penonton |
| Bebek Soeratin | Kompetisi Piala Soeratin di Jawa Timur | Pertandingan | Kelompok usia U-13, U-15, U-17, tanggal, tim, skor, dan venue |
| Bebek Liga 1 | Pertandingan Persebaya Surabaya pada musim 2023/2024 dan 2024/2025 | Pertandingan | Tanggal pertandingan, tim, skor, dan venue |
| Bebek AFF U-19 | Kompetisi Piala AFF U-19 tahun 2024 | Pertandingan | Tanggal pertandingan, tim, skor, dan venue |

Keempat kelompok data tersebut tidak dapat langsung digabungkan berdasarkan urutan baris karena memiliki unit pengamatan yang berbeda. Data pertandingan mencatat aktivitas pada suatu waktu, sedangkan data fasilitas mendeskripsikan karakteristik setiap venue.

Integrasi dilakukan melalui beberapa tahapan:

1. **Standardisasi data pertandingan.** Ketiga dataset pertandingan diselaraskan ke dalam struktur kolom yang konsisten, seperti identitas pertandingan, kompetisi, tanggal, kelompok usia jika tersedia, nama venue, tim yang bertanding, hasil skor, dan sumber data.

2. **Penggabungan data pertandingan.** Setelah memiliki struktur yang konsisten, data Soeratin, Liga 1, dan AFF U-19 digabungkan secara vertikal (*union*) menjadi satu tabel aktivitas pertandingan. Kolom kompetisi digunakan untuk membedakan asal setiap pertandingan.

3. **Standardisasi identitas venue.** Nama stadion dan lapangan diseragamkan untuk menangani perbedaan penulisan, singkatan, atau nama alternatif. Setiap venue kemudian diberikan identitas unik berupa `venue_id`.

4. **Integrasi dengan data fasilitas.** Tabel aktivitas pertandingan dihubungkan dengan tabel fasilitas melalui `venue_id`. Dengan demikian, setiap pertandingan yang berhasil dicocokkan dengan venue dapat dikaitkan dengan informasi lokasi, luas lapangan, dan kapasitas penonton.

5. **Validasi data terintegrasi.** Proses validasi meliputi pemeriksaan duplikasi pertandingan, kelengkapan tanggal dan venue, kecocokan nama fasilitas, serta penanganan nilai yang belum tersedia. Pertandingan yang belum dapat dicocokkan dengan fasilitas disimpan untuk proses verifikasi lebih lanjut.

Sebagai contoh, pertandingan Piala Soeratin, Liga 1, dan AFF U-19 yang berlangsung di venue yang sama akan tetap menjadi catatan pertandingan yang berbeda dalam tabel aktivitas. Ketiganya dapat dihubungkan ke satu identitas venue yang sama pada tabel fasilitas.

Hasil integrasi membentuk dataset analitik yang memungkinkan penghitungan jumlah pertandingan berdasarkan venue dan kompetisi, analisis persebaran fasilitas, serta eksplorasi hubungan antara karakteristik fasilitas dan aktivitas pertandingan.

Perlu diperhatikan bahwa data luas dan kapasitas tidak selalu tersedia untuk seluruh venue. Selain itu, data pertandingan hanya merepresentasikan kompetisi yang tercakup dalam sumber penelitian dan tidak menggambarkan seluruh aktivitas penggunaan lapangan sepak bola di Jawa Timur.

## Arsitektur Data Warehousing

Project mengikuti arsitektur data warehousing yang terdiri dari empat kelompok data (*4 Bebek*), proses ETL, integrasi menggunakan DuckLake, serta analisis dan visualisasi menggunakan Streamlit.

```text
                         DATA SOURCES
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
    PSSI Jawa Timur     Liga Indonesia Baru     Bola.net
       Soeratin              Liga 1              AFF U-19
          |                   |                   |
          v                   v                   v
 data_event_soeratin.csv  data_event_liga1.csv  data_event_aff.csv
          |                   |                   |
          v                   v                   v
 +------------------+ +------------------+ +------------------+
 | BEBEK SOERATIN   | | BEBEK LIGA 1     | | BEBEK AFF U-19   |
 | bebek_soeratin   | | bebek_liga1       | | bebek_aff        |
 | .duckdb          | | .duckdb           | | .duckdb          |
 +------------------+ +------------------+ +------------------+
          |                   |                   |
          +-------------------+-------------------+
                              |
                              |
       Open Data Surabaya & Sumber Fasilitas Resmi
                              |
                              v
                     data_lapangan.csv
                              |
                              v
                   +---------------------+
                   | BEBEK FASILITAS     |
                   | bebek_fasilitas     |
                   | .duckdb             |
                   +---------------------+
                              |
                              |
              +---------------+---------------+
              |                               |
              v                               v
       Seluruh Database DuckDB               |
              |                               |
              +---------------+---------------+
                              |
                              v
                     ETL / ELT PROCESS
             - Data cleaning dan validasi
             - Standardisasi nama venue
             - Pemeriksaan duplikasi event
             - Standardisasi tanggal
             - Pembuatan venue_id
             - Integrasi event dan fasilitas
                              |
                              v
                     DUCKLAKE LAKEHOUSE
                              |
                 +------------+------------+
                 |                         |
                 v                         v
          shared_catalog.ducklake    lakehouse_storage/
                 |
                 v
             DATA MART
                 |
       +---------+----------+
       |                    |
       v                    v
  fact_event             dim_venue
       |                    |
       +---------+----------+
                 |
                 v
       ANALYTICS & AGGREGATION
                 |
       +---------+----------+
       |                    |
       v                    v
 Aktivitas per Venue   Perbandingan Kompetisi
                 |
                 v
        STREAMLIT DASHBOARD
                 |
       +---------+----------+
       |                    |
       v                    v
 Peta Persebaran       Statistik dan Grafik
       Venue             Aktivitas Event
```

### Penjelasan Arsitektur

**1. Data Sources**

Data diperoleh dari empat kelompok sumber, yaitu PSSI Jawa Timur untuk Piala Soeratin, Liga Indonesia Baru untuk Liga 1, Bola.net untuk AFF U-19, serta Open Data Surabaya dan sumber resmi lainnya untuk karakteristik fasilitas sepak bola.

**2. DuckDB — 4 Bebek**

Setiap kelompok data dikelola menggunakan database DuckDB yang terpisah. Pemisahan ini bertujuan menjaga struktur dan asal data masing-masing kelompok sebelum proses integrasi.

**3. ETL / ELT Process**

Data melalui proses pembersihan, penyesuaian format, pemeriksaan duplikasi, dan standardisasi nama venue. Setiap venue yang berhasil diidentifikasi diberikan `venue_id` agar data pertandingan dari berbagai kompetisi dapat dihubungkan ke fasilitas yang sesuai.

**4. DuckLake Lakehouse**

Data yang telah dibersihkan diintegrasikan ke dalam DuckLake sebagai penyimpanan analitik terpusat. Katalog DuckLake mengelola metadata tabel, sedangkan penyimpanan lakehouse digunakan untuk mengelola data yang terintegrasi.

**5. Data Mart**

Data yang terintegrasi disusun menjadi tabel analitik, yaitu:

- `fact_event` — mencatat pertandingan, tanggal, kompetisi, tim, hasil, dan identitas venue.
- `dim_venue` — menyimpan identitas dan karakteristik venue, seperti lokasi administratif, alamat, luas, kapasitas, dan koordinat.
- `mart_aktivitas_venue` — menyajikan agregasi jumlah pertandingan berdasarkan venue.
- `mart_kompetisi_venue` — menyajikan perbandingan aktivitas pertandingan berdasarkan kompetisi dan venue.

**6. Streamlit Dashboard**

Data mart digunakan untuk membangun dashboard interaktif yang menampilkan peta persebaran stadion dan lapangan sepak bola di Jawa Timur, jumlah pertandingan per venue, perbandingan aktivitas antar kompetisi, serta eksplorasi hubungan antara karakteristik fasilitas dan aktivitas pertandingan.

## 🗄️ Local DuckDB

Setiap kelompok sumber data memiliki database DuckDB tersendiri. Pemisahan ini bertujuan menjaga data dari setiap sumber tetap terorganisasi sebelum melalui proses pembersihan, transformasi, dan integrasi ke DuckLake.

### Rencana Database

```text
bebek_soeratin.duckdb
bebek_liga1.duckdb
bebek_aff.duckdb
bebek_fasilitas.duckdb
```

### Struktur Data Lokal

| Database | Sumber Data | File CSV |
|:---|:---|:---|
| `bebek_soeratin.duckdb` | PSSI Jawa Timur | `data_event_soeratin.csv` |
| `bebek_liga1.duckdb` | Liga Indonesia Baru | `data_event_liga1.csv` |
| `bebek_aff.duckdb` | Bola.net | `data_event_aff.csv` |
| `bebek_fasilitas.duckdb` | Open Data Surabaya dan sumber fasilitas lainnya | `data_lapangan.csv` |

### Fungsi Local DuckDB

Local DuckDB berfungsi sebagai **raw/staging layer**, yaitu lapisan penyimpanan awal sebelum data diintegrasikan ke DuckLake.

Pada tahap ini, setiap dataset diimpor ke database masing-masing. Data asli dipertahankan sebagai referensi, sedangkan proses pembersihan dan transformasi dilakukan untuk menghasilkan tabel yang siap diintegrasikan.

Contoh alur pengolahan:

```text
data_event_soeratin.csv
          |
          v
bebek_soeratin.duckdb
          |
          v
cleaning / transformation
          |
          v
DuckLake
```

Alur serupa diterapkan pada data Liga 1, AFF U-19, dan fasilitas lapangan. Proses ini membantu menjaga keterlacakan sumber data sekaligus mempermudah validasi sebelum integrasi.

## 🦆 DuckLake

Data yang telah melalui proses pembersihan dan transformasi kemudian diintegrasikan ke dalam satu lingkungan DuckLake sebagai penyimpanan data analitik terpusat.

DuckLake digunakan untuk mengelola data terintegrasi yang menghubungkan aktivitas pertandingan dari berbagai kompetisi dengan karakteristik stadion dan lapangan sepak bola.

### Rencana Struktur DuckLake

```text
DuckLake
|
|-- soeratin
|   `-- event_soeratin
|
|-- liga1
|   `-- event_liga1
|
|-- aff
|   `-- event_aff
|
|-- fasilitas
|   `-- dim_venue
|
`-- analytics
    |-- fact_event
    |-- mart_aktivitas_venue
    |-- mart_kompetisi_venue
    `-- mart_karakteristik_venue
```

### Penjelasan Struktur

- **`soeratin.event_soeratin`** — menyimpan data pertandingan Piala Soeratin yang telah dibersihkan.
- **`liga1.event_liga1`** — menyimpan data pertandingan Liga 1 yang telah dibersihkan.
- **`aff.event_aff`** — menyimpan data pertandingan Piala AFF U-19 yang telah dibersihkan.
- **`fasilitas.dim_venue`** — menyimpan identitas dan karakteristik setiap venue, termasuk lokasi, luas, kapasitas, serta koordinat jika tersedia.
- **`analytics.fact_event`** — menggabungkan catatan pertandingan dari ketiga kompetisi ke dalam satu struktur analitik yang seragam.
- **`analytics.mart_aktivitas_venue`** — menyajikan jumlah pertandingan yang tercatat pada setiap venue.
- **`analytics.mart_kompetisi_venue`** — menyajikan perbandingan aktivitas pertandingan berdasarkan venue dan kompetisi.
- **`analytics.mart_karakteristik_venue`** — mendukung analisis eksploratif antara karakteristik fasilitas dan jumlah pertandingan.

Tabel-tabel analitik akan dihubungkan menggunakan identitas venue (`venue_id`). Dengan demikian, beberapa catatan pertandingan yang berlangsung di venue yang sama tetap tercatat sebagai pertandingan berbeda, tetapi dapat dikaitkan dengan satu data karakteristik fasilitas.

### Katalog dan Penyimpanan DuckLake

Rencana penggunaan DuckLake:

```text
shared_catalog.ducklake
lakehouse_storage/
```

`shared_catalog.ducklake` digunakan sebagai nama katalog DuckLake yang direncanakan untuk mengelola metadata tabel, sedangkan `lakehouse_storage/` merupakan lokasi penyimpanan data lakehouse.

Nama dan lokasi tersebut merupakan rancangan awal yang akan disesuaikan saat implementasi teknis.

### Tujuan Integrasi DuckLake

Integrasi melalui DuckLake bertujuan untuk:

1. Menyatukan data pertandingan dari tiga kompetisi dalam struktur analitik yang konsisten.
2. Menghubungkan aktivitas pertandingan dengan identitas dan karakteristik venue.
3. Mempermudah penghitungan jumlah pertandingan per venue tanpa menghitung data secara ganda.
4. Menyediakan tabel analitik untuk perbandingan aktivitas antarkompetisi.
5. Menyediakan data yang siap digunakan oleh dashboard interaktif berbasis Streamlit, termasuk peta persebaran stadion dan lapangan sepak bola di Jawa Timur.

## 🔄 ETL / ELT Process

Proses ETL (*Extract, Transform, Load*) / ELT (*Extract, Load, Transform*) dilakukan untuk mempersiapkan data pertandingan dan karakteristik fasilitas sebelum diintegrasikan ke dalam DuckLake. Proses ini mencakup pengambilan data, pembersihan, standardisasi, integrasi, dan pemuatan data ke dalam struktur analitik.

### 1. Extract

Data dikumpulkan dari empat kelompok sumber yang digunakan dalam project:

```text
PSSI Jawa Timur
    └── data_event_soeratin.csv

Liga Indonesia Baru
    └── data_event_liga1.csv

Bola.net
    └── data_event_aff.csv

Open Data Surabaya & Sumber Fasilitas Resmi
    └── data_lapangan.csv
```

Keempat dataset disimpan sebagai data mentah (*raw data*) dan diimpor ke database DuckDB masing-masing:

- `bebek_soeratin.duckdb`
- `bebek_liga1.duckdb`
- `bebek_aff.duckdb`
- `bebek_fasilitas.duckdb`

Data mentah dipertahankan sebagai referensi agar proses pengolahan dapat ditelusuri kembali ke sumber aslinya. Pengambilan data dilakukan melalui dataset yang telah dikumpulkan dan sumber publik terkait.

### 2. Transform

Transformasi dilakukan untuk menghasilkan data yang konsisten, valid, dan siap diintegrasikan.

**Transformasi data pertandingan:**

- Memeriksa struktur kolom dan tipe data pada setiap dataset.
- Menghapus baris kosong yang tidak berisi catatan pertandingan.
- Menstandarkan nama kolom agar memiliki struktur yang konsisten antarkompetisi.
- Menyeragamkan format tanggal pertandingan.
- Membersihkan dan menstandarkan nama kompetisi, kelompok usia, tim, dan venue.
- Memeriksa duplikasi catatan pertandingan tanpa menghapus pertandingan berbeda yang kebetulan berlangsung pada tanggal atau venue yang sama.
- Memeriksa kelengkapan informasi tim, skor, tanggal, dan venue.
- Menambahkan atribut kompetisi untuk membedakan Soeratin, Liga 1, dan AFF U-19 setelah data pertandingan digabungkan.

**Transformasi data fasilitas:**

- Menstandarkan nama stadion dan lapangan.
- Memeriksa kecocokan nama fasilitas dengan venue pada data pertandingan.
- Menyeragamkan nama kabupaten/kota, kecamatan, dan kelurahan jika tersedia.
- Mengubah nilai luas dan kapasitas ke tipe numerik.
- Menyeragamkan satuan luas menjadi meter persegi (m²).
- Memisahkan luas lapangan dari luas tanah atau kompleks stadion jika keduanya tersedia.
- Memeriksa kelengkapan alamat dan koordinat untuk kebutuhan pemetaan.
- Menangani nilai kosong tanpa menganggapnya sebagai nol.

**Transformasi integrasi:**

- Menggabungkan data Soeratin, Liga 1, dan AFF U-19 dengan struktur kolom yang seragam.
- Membentuk identitas unik `venue_id` untuk setiap venue yang telah diverifikasi.
- Menghubungkan data pertandingan dengan tabel fasilitas berdasarkan `venue_id`.
- Memisahkan catatan pertandingan yang belum dapat dicocokkan ke venue untuk proses verifikasi.
- Menghitung ulang jumlah pertandingan per venue dari data event yang telah dibersihkan.

Contoh alur transformasi:

```text
Raw Event Data
      |
      v
Cleaning & Standardization
      |
      v
Unified Event Structure
      |
      v
Venue Matching
      |
      +-------------------+
      |                   |
      v                   v
  Fact Event          Dim Venue
      |                   |
      +---------+---------+
                |
                v
       Integrated Data
```

### 3. Load

Data yang telah dibersihkan dan distandardisasi dimuat ke dalam DuckLake sebagai penyimpanan analitik terpusat.

Proses pemuatan dilakukan dengan mempertahankan pemisahan logis antarjenis data, sekaligus menyediakan tabel terintegrasi untuk kebutuhan analisis.

Rencana tabel yang dimuat ke DuckLake:

| Schema | Tabel | Fungsi |
|:---|:---|:---|
| `soeratin` | `event_soeratin` | Data pertandingan Piala Soeratin |
| `liga1` | `event_liga1` | Data pertandingan Liga 1 |
| `aff` | `event_aff` | Data pertandingan AFF U-19 |
| `fasilitas` | `dim_venue` | Identitas dan karakteristik venue |
| `analytics` | `fact_event` | Data pertandingan terintegrasi |
| `analytics` | `mart_aktivitas_venue` | Agregasi jumlah pertandingan per venue |
| `analytics` | `mart_kompetisi_venue` | Perbandingan aktivitas berdasarkan kompetisi |
| `analytics` | `mart_karakteristik_venue` | Dataset analitik karakteristik fasilitas dan aktivitas pertandingan |

Tabel analitik dibentuk setelah proses validasi integrasi selesai. Jumlah pertandingan pada setiap venue dihitung dari catatan pertandingan yang telah dibersihkan, bukan dijumlahkan kembali dengan kolom `jumlah_event` dari dataset fasilitas.

### 4. Validasi Hasil ETL / ELT

Validasi dilakukan untuk memastikan bahwa data yang dimuat ke DuckLake sesuai dengan data sumber dan siap digunakan dalam analisis.

Pemeriksaan meliputi:

- Kesesuaian jumlah catatan sebelum dan sesudah transformasi.
- Konsistensi tipe data dan format tanggal.
- Pemeriksaan duplikasi pertandingan.
- Pemeriksaan nama venue yang belum berhasil dicocokkan.
- Kelengkapan data luas, kapasitas, dan lokasi fasilitas.
- Konsistensi jumlah pertandingan pada tabel analitik dengan hasil agregasi tabel event.

Data yang belum lengkap tetap diberi penanda untuk ditinjau lebih lanjut. Nilai yang tidak ditemukan tidak diisi menggunakan perkiraan tanpa sumber yang dapat dipertanggungjawabkan.

### 5. Output Proses ETL / ELT

Hasil proses ETL / ELT adalah dataset analitik terintegrasi yang menghubungkan aktivitas pertandingan dengan karakteristik fasilitas sepak bola di Jawa Timur.

Data tersebut selanjutnya digunakan untuk:

- Menghitung jumlah pertandingan yang tercatat pada setiap venue.
- Membandingkan aktivitas pertandingan Soeratin, Liga 1, dan AFF U-19.
- Menganalisis persebaran stadion dan lapangan sepak bola.
- Mengeksplorasi hubungan antara luas lapangan, kapasitas penonton, dan jumlah pertandingan.
- Menyediakan data untuk dashboard interaktif berbasis Streamlit, termasuk peta persebaran venue.

## 📊 Dashboard Streamlit

Dashboard akan dikembangkan menggunakan **Streamlit** untuk menyajikan hasil analisis aktivitas pertandingan dan karakteristik fasilitas stadion serta lapangan sepak bola di Jawa Timur. Dashboard dirancang agar pengguna dapat mengeksplorasi persebaran venue, membandingkan aktivitas pertandingan antar kompetisi, dan melihat karakteristik fasilitas berdasarkan data yang tersedia.

### Halaman 1 — Activity Overview

Menampilkan ringkasan aktivitas pertandingan yang tercatat dalam dataset.

**Indikator utama:**

- jumlah pertandingan yang tercatat,
- jumlah venue unik,
- jumlah kompetisi yang dianalisis,
- jumlah venue dengan data fasilitas yang tersedia,
- venue dengan jumlah pertandingan terbanyak,
- distribusi pertandingan berdasarkan kompetisi.

**Visualisasi:**

- kartu statistik (*KPI cards*),
- diagram batang 10 venue dengan pertandingan terbanyak,
- diagram distribusi pertandingan berdasarkan kompetisi,
- ringkasan kelengkapan data fasilitas.

### Halaman 2 — Venue Distribution Map

Menampilkan peta interaktif persebaran stadion dan lapangan sepak bola di Jawa Timur.

**Filter:**

```text
Kompetisi
Periode / Tahun
Kelompok Usia Soeratin
Kabupaten / Kota
Nama Venue
```

**Visualisasi dan informasi:**

- peta persebaran venue berdasarkan koordinat geografis,
- ukuran penanda berdasarkan jumlah pertandingan yang tercatat,
- warna penanda untuk membedakan tingkat aktivitas pertandingan,
- informasi venue ketika penanda dipilih,
- detail lokasi, jumlah pertandingan, luas lapangan, dan kapasitas penonton jika tersedia.

Peta digunakan untuk mengidentifikasi persebaran fasilitas dan melihat konsentrasi aktivitas pertandingan berdasarkan lokasi geografis. Venue yang belum memiliki koordinat terverifikasi akan ditampilkan dalam tabel terpisah sampai lokasinya berhasil dilengkapi.

### Halaman 3 — Competition Analysis

Menganalisis dan membandingkan aktivitas pertandingan pada tiga kelompok kompetisi, yaitu Piala Soeratin, Liga 1, dan Piala AFF U-19.

**Filter:**

```text
Kompetisi
Periode / Musim
Kelompok Usia
Nama Venue
```

Filter kelompok usia hanya berlaku untuk data Soeratin, sedangkan filter musim digunakan untuk data Liga 1 jika informasi musim tersedia.

**Visualisasi:**

- diagram batang jumlah pertandingan per venue berdasarkan kompetisi,
- perbandingan distribusi pertandingan Soeratin U-13, U-15, dan U-17,
- grafik tren jumlah pertandingan per bulan atau tahun jika tanggal tersedia,
- tabel venue yang digunakan oleh lebih dari satu kompetisi,
- distribusi pertandingan berdasarkan babak atau level kompetisi jika datanya tersedia.

Analisis ini digunakan untuk mengidentifikasi pola distribusi pertandingan dan perbedaan penggunaan venue pada kompetisi yang tercakup dalam penelitian.

### Halaman 4 — Facility Analysis

Menganalisis karakteristik fasilitas stadion dan lapangan sepak bola serta mengeksplorasi hubungannya dengan jumlah pertandingan yang tercatat.

**Filter:**

```text
Kabupaten / Kota
Nama Venue
Rentang Luas Lapangan
Rentang Kapasitas Penonton
```

Filter hanya diterapkan pada atribut yang memiliki data valid.

**Visualisasi:**

- perbandingan kapasitas penonton antar venue,
- perbandingan luas lapangan berdasarkan data yang tersedia,
- diagram pencar luas lapangan terhadap jumlah pertandingan,
- diagram pencar kapasitas penonton terhadap jumlah pertandingan,
- tabel karakteristik fasilitas beserta jumlah pertandingan yang tercatat,
- ringkasan kelengkapan data luas dan kapasitas.

Analisis dilakukan secara eksploratif untuk melihat pola hubungan antara karakteristik fasilitas dan aktivitas pertandingan. Hubungan yang ditemukan tidak langsung diinterpretasikan sebagai hubungan sebab-akibat.

### Fitur Tambahan Dashboard

Dashboard juga dirancang untuk menyediakan:

- filter interaktif yang menghubungkan visualisasi dalam setiap halaman,
- tabel detail data berdasarkan kompetisi dan venue,
- informasi sumber data dan kelengkapan atribut,
- indikator data yang belum tersedia atau belum terverifikasi,
- unduhan data hasil penyaringan jika diperlukan.

### Teknologi Dashboard

| Teknologi | Fungsi |
|:---|:---|
| Streamlit | Antarmuka dashboard interaktif |
| Plotly | Grafik statistik dan visualisasi interaktif |
| PyDeck / Folium | Visualisasi peta persebaran venue |
| DuckDB | Pengambilan dan pengolahan data analitik |
| DuckLake | Penyimpanan data analitik terintegrasi |
