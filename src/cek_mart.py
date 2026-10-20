
import duckdb

con = duckdb.connect()

try:
    con.execute("""
        ATTACH 'ducklake:shared_catalog.ducklake' AS lake
    """)

    print("\n=== STATUS PENCOCOKAN VENUE ===")
    print(con.execute("""
        SELECT
            status_pencocokan_venue,
            COUNT(*) AS jumlah
        FROM lake.analytics.fact_event
        GROUP BY status_pencocokan_venue
    """).fetchdf().to_string(index=False))

    print("\n=== JUMLAH EVENT PER KOMPETISI ===")
    print(con.execute("""
        SELECT
            kompetisi_sumber,
            COUNT(*) AS jumlah
        FROM lake.analytics.fact_event
        GROUP BY kompetisi_sumber
    """).fetchdf().to_string(index=False))

    print("\n=== JUMLAH VENUE_ID KOSONG ===")
    print(con.execute("""
        SELECT COUNT(*) AS jumlah
        FROM lake.analytics.fact_event
        WHERE venue_id IS NULL
    """).fetchdf().to_string(index=False))

finally:
    con.close()
