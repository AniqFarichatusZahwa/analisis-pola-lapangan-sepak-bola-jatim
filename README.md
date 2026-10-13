# Analisis Pola Pemanfaatan Lapangan Sepak Bola di Jawa Timur

Project ini merupakan project akhir Data Warehousing yang mengintegrasikan data pertandingan sepak bola dan karakteristik fasilitas olahraga di Jawa Timur untuk menganalisis pola pemanfaatan lapangan berdasarkan aktivitas event dan karakteristik fasilitas. Project ini menggunakan **DuckDB, DuckLake, dan Streamlit** untuk mendukung proses penyimpanan, pengolahan, integrasi, analisis, dan visualisasi data.

## Kelompok Data: 4 Bebek

Project ini menggunakan empat kelompok data utama yang disebut sebagai **4 Bebek**:

1. **Bebek Soeratin** — data pertandingan Piala Soeratin kelompok usia U-13, U-15, dan U-17 yang bersumber dari [PSSI Jawa Timur](https://pssijatim.com/).
2. **Bebek Liga 1** — data pertandingan Liga 1 Indonesia musim 2023/2024 dan 2024/2025 yang bersumber dari [Liga Indonesia Baru](https://www.ligaindonesiabaru.com/).
3. **Bebek AFF U-19** — data pertandingan Piala AFF U-19 tahun 2024 yang bersumber dari [Bola.net](https://www.bola.net/).
4. **Bebek Fasilitas** — data karakteristik stadion dan lapangan sepak bola, meliputi nama venue, lokasi administratif, alamat, luas lapangan, dan kapasitas penonton. Sumber data mencakup [Open Data Surabaya](https://opendata.surabaya.go.id/kumpulan_dataset/z001-10646-3) serta sumber resmi lain yang relevan untuk melengkapi informasi fasilitas di Jawa Timur.

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
