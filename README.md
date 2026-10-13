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

### 🔗 Integrasi Data

Ketiga dataset pertandingan, yaitu Soeratin, Liga 1, dan AFF U-19, serta dataset fasilitas akan dikelola dalam empat database DuckDB yang terpisah.

Data kemudian melalui proses *Extract, Transform, Load* (ETL), yang meliputi pembersihan data, standardisasi nama venue, penyesuaian format tanggal, pemeriksaan duplikasi pertandingan, serta penanganan nilai yang belum tersedia.

Selanjutnya, data yang telah dibersihkan akan diintegrasikan melalui DuckLake untuk membentuk penyimpanan data analitik terpusat. Integrasi dilakukan dengan menghubungkan catatan pertandingan dari setiap kompetisi dengan identitas venue pada dataset fasilitas.

Data terintegrasi akan digunakan untuk menganalisis jumlah pertandingan per venue, membandingkan aktivitas antarkompetisi, mengeksplorasi hubungan antara luas dan kapasitas fasilitas dengan jumlah pertandingan, serta memvisualisasikan persebaran stadion dan lapangan sepak bola di Jawa Timur melalui dashboard interaktif berbasis Streamlit.
