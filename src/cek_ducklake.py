
import duckdb

con = duckdb.connect()

con.execute("""
    ATTACH 'ducklake:shared_catalog.ducklake'
    AS lake (READ_ONLY)
""")

print("=== STATUS PENCOCOKAN VENUE ===")
hasil = con.execute("""
    SELECT status_pencocokan_venue, COUNT(*) AS jumlah
    FROM lake.analytics.fact_event
    GROUP BY 1
    ORDER BY 1
""").fetchdf()
print(hasil.to_string(index=False))

print("\n=== CONTOH DATA VENUE ===")
venue = con.execute("""
    SELECT venue_id, nama_venue, latitude, longitude
    FROM lake.fasilitas.dim_venue
    LIMIT 5
""").fetchdf()
print(venue.to_string(index=False))

con.close()
