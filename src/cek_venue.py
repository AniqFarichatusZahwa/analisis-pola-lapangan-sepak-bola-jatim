
import duckdb

con = duckdb.connect(
    "data/duckdb/bebek_fasilitas.duckdb",
    read_only=True
)

query = """
SELECT nama_venue, kecamatan, kelurahan
FROM bebek_fasilitas
WHERE lower(nama_venue) LIKE '%arhanud%'
   OR lower(nama_venue) LIKE '%pusdik%'
   OR lower(nama_venue) LIKE '%batu%'
"""

hasil = con.execute(query).fetchdf()

if hasil.empty:
    print("Tidak ditemukan venue dengan kata arhanud, pusdik, atau batu.")
else:
    print(hasil.to_string(index=False))

con.close()
