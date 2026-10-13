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

