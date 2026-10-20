
import duckdb

con = duckdb.connect()

try:
    con.execute("""
        ATTACH 'ducklake:shared_catalog.ducklake' AS lake
    """)

    print("=== MEMBUAT TABEL MART ===")

    # 1. Aktivitas setiap venue, termasuk venue tanpa event
    con.execute("""
        CREATE OR REPLACE TABLE lake.analytics.mart_aktivitas_venue AS
        WITH aktivitas AS (
            SELECT
                venue_id,
                COUNT(id_event) AS total_event,
                COUNT(*) FILTER (
                    WHERE kompetisi_sumber = 'Soeratin'
                ) AS total_soeratin,
                COUNT(*) FILTER (
                    WHERE kompetisi_sumber = 'Liga 1'
                ) AS total_liga1,
                COUNT(*) FILTER (
                    WHERE kompetisi_sumber = 'AFF U-19'
                ) AS total_aff_u19,
                MIN(TRY_CAST(tanggal_mulai_iso AS DATE)) AS event_pertama,
                MAX(TRY_CAST(tanggal_mulai_iso AS DATE)) AS event_terakhir
            FROM lake.analytics.fact_event
            WHERE venue_id IS NOT NULL
              AND LOWER(status_pencocokan_venue) = 'cocok'
            GROUP BY venue_id
        )
        SELECT
            d.venue_id,
            d.nama_venue,
            COALESCE(a.total_event, 0) AS total_event,
            COALESCE(a.total_soeratin, 0) AS total_soeratin,
            COALESCE(a.total_liga1, 0) AS total_liga1,
            COALESCE(a.total_aff_u19, 0) AS total_aff_u19,
            a.event_pertama,
            a.event_terakhir
        FROM lake.fasilitas.dim_venue d
        LEFT JOIN aktivitas a ON d.venue_id = a.venue_id
    """)

    print("mart_aktivitas_venue selesai")

    # 2. Aktivitas venue berdasarkan kompetisi
    con.execute("""
        CREATE OR REPLACE TABLE lake.analytics.mart_kompetisi_venue AS
        SELECT
            f.venue_id,
            d.nama_venue,
            f.kompetisi_sumber,
            COUNT(f.id_event) AS total_event
        FROM lake.analytics.fact_event f
        INNER JOIN lake.fasilitas.dim_venue d
            ON f.venue_id = d.venue_id
        WHERE LOWER(f.status_pencocokan_venue) = 'cocok'
        GROUP BY
            f.venue_id,
            d.nama_venue,
            f.kompetisi_sumber
    """)

    print("mart_kompetisi_venue selesai")

    # 3. Karakteristik venue digabung dengan aktivitasnya
    con.execute("""
        CREATE OR REPLACE TABLE lake.analytics.mart_karakteristik_venue AS
        SELECT
            d.*,
            a.total_event,
            a.total_soeratin,
            a.total_liga1,
            a.total_aff_u19,
            a.event_pertama,
            a.event_terakhir
        FROM lake.fasilitas.dim_venue d
        LEFT JOIN lake.analytics.mart_aktivitas_venue a
            ON d.venue_id = a.venue_id
    """)

    print("mart_karakteristik_venue selesai")

    print("\n=== HASIL PEMBUATAN MART ===")

    for table in [
        "mart_aktivitas_venue",
        "mart_kompetisi_venue",
        "mart_karakteristik_venue",
    ]:
        count = con.execute(
            f"SELECT COUNT(*) FROM lake.analytics.{table}"
        ).fetchone()[0]
        print(f"{table}: {count} baris")

    unmatched = con.execute("""
        SELECT COUNT(*)
        FROM lake.analytics.fact_event
        WHERE venue_id IS NULL
    """).fetchone()[0]

    print(f"\nEvent tanpa venue cocok: {unmatched}")
    print("Pembuatan tabel mart selesai.")

finally:
    con.close()
