from pathlib import Path
import re
import unicodedata

import duckdb
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parent.parent
DUCKDB_DIR = ROOT_DIR / "data" / "duckdb"
CATALOG_PATH = ROOT_DIR / "shared_catalog.ducklake"
LAKEHOUSE_DIR = ROOT_DIR / "lakehouse_storage"

LAKEHOUSE_DIR.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "fasilitas": ("bebek_fasilitas.duckdb", "bebek_fasilitas"),
    "soeratin": ("bebek_soeratin.duckdb", "bebek_soeratin"),
    "liga1": ("bebek_liga1.duckdb", "bebek_liga1"),
    "aff": ("bebek_aff.duckdb", "bebek_aff"),
}

TARGETS = {
    "fasilitas": ("fasilitas", "raw_lapangan"),
    "soeratin": ("soeratin", "event_soeratin"),
    "liga1": ("liga1", "event_liga1"),
    "aff": ("aff", "event_aff"),
}


def normalize_name(value):
    """Menormalkan nama venue, termasuk singkatan Lap. menjadi Lapangan."""
    if pd.isna(value):
        return ""

    text = str(value).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(
        char for char in text
        if not unicodedata.combining(char)
    )
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = " ".join(text.split())

    # Samakan singkatan "lap" dengan "lapangan".
    text = re.sub(r"\blap\b", "lapangan", text)

    return " ".join(text.split())


def parse_date(value):
    """Mengubah tanggal sumber menjadi tanggal ISO."""
    if pd.isna(value) or not str(value).strip():
        return pd.NaT

    return pd.to_datetime(
        str(value).strip(),
        dayfirst=True,
        errors="coerce",
    )


def parse_score(value):
    """Mengambil dua angka dari skor seperti 00:04."""
    if pd.isna(value):
        return None, None, None

    text = str(value).strip()
    match = re.fullmatch(r"\s*(\d+)\s*[:\-]\s*(\d+)\s*", text)

    if not match:
        return None, None, text if text else None

    score_1 = int(match.group(1))
    score_2 = int(match.group(2))

    normalized = f"{score_1}:{score_2}"
    return score_1, score_2, normalized


def read_lake_table(con, schema, table):
    return con.execute(
        f'SELECT * FROM lake."{schema}"."{table}"'
    ).fetchdf()


def build_dim_venue(raw_df):
    """Membentuk dimensi venue dari tabel fasilitas terbaru."""
    df = raw_df.copy()
    df.columns = df.columns.str.strip()

    required = [
        "nama_venue",
        "kecamatan",
        "kelurahan",
        "nama_fasilitas_olahraga",
        "alamatlokasi",
        "luas_m2",
        "kapasitas_penonton",
        "latitude",
        "longitude",
    ]

    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(
            f"Kolom fasilitas tidak tersedia: {missing}"
        )

    # Bersihkan nama dan hilangkan duplikasi venue berdasarkan nama.
    df["nama_venue"] = df["nama_venue"].astype("string").str.strip()
    df = df[
        df["nama_venue"].notna()
        & (df["nama_venue"] != "")
    ].copy()

    df["_nama_key"] = df["nama_venue"].apply(normalize_name)
    df = df.drop_duplicates(subset="_nama_key", keep="first")
    df = df.sort_values("_nama_key").reset_index(drop=True)

    # ID stabil berdasarkan nama venue yang sudah dinormalisasi.
    df.insert(
        0,
        "venue_id",
        [f"VEN{i:03d}" for i in range(1, len(df) + 1)],
    )

    columns = [
        "venue_id",
        "nama_venue",
        "kecamatan",
        "kelurahan",
        "nama_fasilitas_olahraga",
        "alamatlokasi",
        "luas_m2",
        "kapasitas_penonton",
        "latitude",
        "longitude",
    ]

    return df[columns].copy()



def build_fact_event(event_sources, dim_venue):
    """Menggabungkan event dan mencocokkan venue secara bertahap."""

    def compact_name(value):
        """Normalisasi tambahan untuk nama venue."""
        return re.sub(r"[^a-z0-9]", "", normalize_name(value))

    # Lookup berdasarkan nama normalisasi standar dan nama tanpa pemisah.
    venue_lookup = {}
    compact_lookup = {}

    for _, row in dim_venue.iterrows():
        name = row["nama_venue"]
        venue_id = row["venue_id"]

        key = normalize_name(name)
        compact_key = compact_name(name)

        if key:
            venue_lookup.setdefault(key, venue_id)

        if compact_key:
            compact_lookup.setdefault(compact_key, venue_id)

    frames = []

    source_labels = {
        "soeratin": "Soeratin",
        "liga1": "Liga 1",
        "aff": "AFF U-19",
    }

    for source_key in ["soeratin", "liga1", "aff"]:
        df = event_sources[source_key].copy()
        df.columns = df.columns.str.strip()

        required = [
            "id_event",
            "nama_event",
            "tanggal_mulai",
            "tanggal_selesai",
            "nama_venue",
            "level_event",
            "peserta_tim",
            "hasil_skor",
            "sumber",
        ]

        for col in required:
            if col not in df.columns:
                df[col] = None

        # Pertahankan tanggal asli dan buat kolom tanggal ISO.
        df["tanggal_mulai_iso"] = df["tanggal_mulai"].apply(parse_date)
        df["tanggal_selesai_iso"] = df["tanggal_selesai"].apply(parse_date)

        def match_venue(name):
            key = normalize_name(name)
            if not key:
                return None

            # Tahap 1: nama normalisasi harus sama persis.
            if key in venue_lookup:
                return venue_lookup[key]

            # Tahap 2: nama sama setelah spasi dan tanda baca dihilangkan.
            return compact_lookup.get(compact_name(name))

        df["venue_id"] = df["nama_venue"].apply(match_venue)

        df["status_pencocokan_venue"] = df.apply(
            lambda row: (
                "cocok"
                if pd.notna(row["venue_id"])
                else (
                    "nama venue kosong"
                    if pd.isna(row["nama_venue"])
                    or not str(row["nama_venue"]).strip()
                    else "venue tidak ditemukan"
                )
            ),
            axis=1,
        )

        df["kompetisi_sumber"] = source_labels[source_key]

        # Ekstraksi skor.
        scores = df["hasil_skor"].apply(parse_score)
        df["skor_tim_1"] = scores.apply(lambda result: result[0])
        df["skor_tim_2"] = scores.apply(lambda result: result[1])
        df["hasil_skor_normalisasi"] = scores.apply(
            lambda result: result[2]
        )

        frames.append(df)

    fact = pd.concat(frames, ignore_index=True)

    for col in ["tanggal_mulai_iso", "tanggal_selesai_iso"]:
        fact[col] = pd.to_datetime(
            fact[col], errors="coerce"
        ).dt.date

    columns = [
        "id_event",
        "nama_event",
        "tanggal_mulai",
        "tanggal_selesai",
        "nama_venue",
        "level_event",
        "peserta_tim",
        "hasil_skor",
        "sumber",
        "skor_tim_1",
        "skor_tim_2",
        "hasil_skor_normalisasi",
        "tanggal_mulai_iso",
        "tanggal_selesai_iso",
        "kompetisi_sumber",
        "venue_id",
        "status_pencocokan_venue",
    ]

    return fact[columns].copy()


def main():
    con = duckdb.connect()

    try:
        print("=== MENYIAPKAN DUCKLAKE ===")
        con.execute("INSTALL ducklake")
        con.execute("LOAD ducklake")

        catalog = CATALOG_PATH.as_posix().replace("'", "''")
        storage = LAKEHOUSE_DIR.as_posix().replace("'", "''")

        con.execute(
            f"ATTACH 'ducklake:{catalog}' AS lake "
            f"(DATA_PATH '{storage}/')"
        )

        for schema in [
            "fasilitas", "soeratin", "liga1", "aff", "analytics"
        ]:
            con.execute(
                f'CREATE SCHEMA IF NOT EXISTS lake."{schema}"'
            )

        # 1. Muat ulang tabel sumber dari empat database DuckDB.
        for key, (filename, source_table) in SOURCES.items():
            db_path = DUCKDB_DIR / filename

            if not db_path.exists():
                raise FileNotFoundError(
                    f"Database sumber tidak ditemukan: {db_path}"
                )

            with duckdb.connect(str(db_path), read_only=True) as source:
                df = source.execute(
                    f'SELECT * FROM "{source_table}"'
                ).fetchdf()

            con.register("temp_source", df)
            schema, target_table = TARGETS[key]

            con.execute(
                f'CREATE OR REPLACE TABLE '
                f'lake."{schema}"."{target_table}" '
                f'AS SELECT * FROM temp_source'
            )
            con.unregister("temp_source")

            count = con.execute(
                f'SELECT COUNT(*) FROM '
                f'lake."{schema}"."{target_table}"'
            ).fetchone()[0]

            print(f"{schema}.{target_table}: {count} baris")

        # 2. Bentuk dim_venue langsung dari raw_lapangan.
        raw_facility = read_lake_table(
            con, "fasilitas", "raw_lapangan"
        )
        dim_venue = build_dim_venue(raw_facility)

        con.register("temp_dim_venue", dim_venue)
        con.execute("""
            CREATE OR REPLACE TABLE lake.fasilitas.dim_venue AS
            SELECT * FROM temp_dim_venue
        """)
        con.unregister("temp_dim_venue")

        print(
            "fasilitas.dim_venue:",
            con.execute(
                "SELECT COUNT(*) FROM lake.fasilitas.dim_venue"
            ).fetchone()[0],
            "baris",
        )

        # 3. Ambil tabel event sumber dari DuckLake.
        event_sources = {
            "soeratin": read_lake_table(
                con, "soeratin", "event_soeratin"
            ),
            "liga1": read_lake_table(
                con, "liga1", "event_liga1"
            ),
            "aff": read_lake_table(
                con, "aff", "event_aff"
            ),
        }

        # 4. Bentuk fact_event langsung dari tiga tabel event.
        fact_event = build_fact_event(event_sources, dim_venue)

        con.register("temp_fact_event", fact_event)
        con.execute("""
            CREATE OR REPLACE TABLE lake.analytics.fact_event AS
            SELECT * FROM temp_fact_event
        """)
        con.unregister("temp_fact_event")

        print(
            "analytics.fact_event:",
            con.execute(
                "SELECT COUNT(*) FROM lake.analytics.fact_event"
            ).fetchone()[0],
            "baris",
        )

        # 5. Ringkasan validasi integrasi.
        print("\n=== VALIDASI FACT EVENT ===")
        print(
            con.execute("""
                SELECT kompetisi_sumber, COUNT(*) AS jumlah_event
                FROM lake.analytics.fact_event
                GROUP BY kompetisi_sumber
                ORDER BY kompetisi_sumber
            """).fetchdf().to_string(index=False)
        )

        print("\nStatus pencocokan venue:")
        print(
            con.execute("""
                SELECT status_pencocokan_venue, COUNT(*) AS jumlah
                FROM lake.analytics.fact_event
                GROUP BY status_pencocokan_venue
                ORDER BY status_pencocokan_venue
            """).fetchdf().to_string(index=False)
        )

        print("\nEvent tanpa venue yang cocok:")
        print(
            con.execute("""
                SELECT id_event, nama_event, nama_venue, sumber
                FROM lake.analytics.fact_event
                WHERE venue_id IS NULL
                LIMIT 25
            """).fetchdf().to_string(index=False)
        )

        print("\n=== INTEGRASI DUCKLAKE SELESAI ===")
        print(f"Katalog: {CATALOG_PATH}")
        print(f"Penyimpanan: {LAKEHOUSE_DIR}")

    finally:
        con.close()


if __name__ == "__main__":
    main()
