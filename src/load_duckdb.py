
from pathlib import Path

import duckdb
import pandas as pd

# Lokasi utama project
ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT_DIR / "data" / "raw"
DB_DIR = ROOT_DIR / "data" / "processed"

DB_DIR.mkdir(parents=True, exist_ok=True)

# CSV: nama database, nama tabel
DATASETS = {
    "data_lapangan.csv": (
        "bebek_fasilitas.duckdb",
        "data_fasilitas",
    ),
    "data_event_soeratin.csv": (
        "bebek_soeratin.duckdb",
        "data_soeratin",
    ),
    "data_event_liga1.csv": (
        "bebek_liga1.duckdb",
        "data_liga1",
    ),
    "data_event_aff.csv": (
        "bebek_aff.duckdb",
        "data_aff",
    ),
}


def load_csv_to_duckdb(filename, db_filename, table_name):
    csv_path = RAW_DIR / filename
    db_path = DB_DIR / db_filename

    if not csv_path.exists():
        print(f"[GAGAL] File tidak ditemukan: {csv_path}")
        return

    # Membaca CSV dan mencoba mendeteksi pemisah kolom

    df = pd.read_csv(
        csv_path,
        sep=";",
        encoding="utf-8-sig",
        skip_blank_lines=True,
    )

    # Hapus baris yang seluruh kolomnya kosong
    df = df.dropna(how="all")

    # Hapus spasi pada kolom teks
    df = df.apply(
        lambda col: col.str.strip() if col.dtype == "object" else col
    )

    # Hapus baris yang isinya hanya string kosong
    df = df.replace(r"^\s*$", pd.NA, regex=True)
    df = df.dropna(how="all")

    # Rapikan nama kolom
    df.columns = [
        str(col).strip().replace("\ufeff", "")
        for col in df.columns
    ]

    # Impor data ke database DuckDB
    con = duckdb.connect(str(db_path))

    try:
        con.register("df_source", df)

        con.execute(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT * FROM df_source
        """)

        total_rows = con.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        ).fetchone()[0]

        schema = con.execute(
            f"DESCRIBE {table_name}"
        ).fetchdf()

        print(f"\n{'=' * 50}")
        print(f"File     : {filename}")
        print(f"Database : {db_filename}")
        print(f"Tabel    : {table_name}")
        print(f"Baris    : {total_rows}")
        print(f"Kolom    : {len(df.columns)}")
        print("\nStruktur tabel:")
        print(schema.to_string(index=False))

    finally:
        con.close()


if __name__ == "__main__":
    for filename, (db_filename, table_name) in DATASETS.items():
        load_csv_to_duckdb(
            filename,
            db_filename,
            table_name,
        )

    print("\nProses impor selesai.")
