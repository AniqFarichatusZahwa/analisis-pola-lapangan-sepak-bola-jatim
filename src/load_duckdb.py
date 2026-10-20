
from pathlib import Path
import re

import duckdb
import pandas as pd


# Lokasi project
ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT_DIR / "data" / "raw"
DB_DIR = ROOT_DIR / "data" / "duckdb"

DB_DIR.mkdir(parents=True, exist_ok=True)


# Pemetaan empat kelompok data
DATASETS = {
    "bebek_fasilitas": "data_lapangan.csv",
    "bebek_soeratin": "data_event_soeratin.csv",
    "bebek_liga1": "data_event_liga1.csv",
    "bebek_aff": "data_event_aff.csv",
}


def parse_indonesian_number(value):
    """Mengubah angka berformat Indonesia menjadi angka numerik."""
    if pd.isna(value):
        return None

    text = str(value).strip()

    if not text or text.lower() in {"nan", "none", "null", "-"}:
        return None

    # Format Indonesia: 53.144,00 -> 53144.00
    if "," in text:
        text = text.replace(".", "").replace(",", ".")
    else:
        # Angka tanpa koma, misalnya 64215, tetap dipertahankan.
        text = text.replace(",", "")

    try:
        return float(text)
    except ValueError:
        return None


def fix_coordinate(value, coordinate_type):
    """
    Memperbaiki koordinat yang kehilangan tanda desimal.
    Contoh:
    latitude  -77626776   -> -7.7626776
    longitude 1121848437  -> 112.1848437

    Koordinat yang sudah benar tidak diubah.
    """
    if pd.isna(value):
        return None

    text = str(value).strip()

    if not text or text.lower() in {"nan", "none", "null", "-"}:
        return None

    # Normalisasi angka yang memakai koma desimal.
    text = text.replace(",", ".")

    try:
        number = float(text)
    except ValueError:
        return None

    # Jika sudah berada dalam rentang koordinat yang valid,
    # pertahankan nilainya.
    limit = 90 if coordinate_type == "latitude" else 180

    if -limit <= number <= limit:
        return number

    # Koordinat rusak biasanya berupa angka bulat tanpa desimal.
    # Sisipkan desimal setelah 1 digit latitude atau 3 digit longitude.
    if not re.fullmatch(r"[+-]?\d+", text):
        return None

    sign = "-" if text.startswith("-") else ""
    digits = text.lstrip("+-")

    decimal_position = 1 if coordinate_type == "latitude" else 3

    if len(digits) <= decimal_position:
        return None

    corrected = (
        sign
        + digits[:decimal_position]
        + "."
        + digits[decimal_position:]
    )

    try:
        number = float(corrected)
    except ValueError:
        return None

    # Validasi rentang koordinat.
    if not -limit <= number <= limit:
        return None

    return number


def clean_facility_data(df):
    """Membersihkan kolom luas dan koordinat fasilitas."""
    # Hilangkan spasi pada nama kolom.
    df.columns = df.columns.str.strip()

    # Pastikan kolom yang diperlukan tersedia.
    required_columns = [
        "luas_m2",
        "latitude",
        "longitude",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(
            f"Kolom fasilitas tidak ditemukan: {missing}. "
            f"Kolom tersedia: {list(df.columns)}"
        )

    # Luas lapangan menjadi tipe numerik.
    df["luas_m2"] = df["luas_m2"].apply(parse_indonesian_number)

    # Latitude dan longitude menjadi tipe numerik.
    df["latitude"] = df["latitude"].apply(
        lambda value: fix_coordinate(value, "latitude")
    )
    df["longitude"] = df["longitude"].apply(
        lambda value: fix_coordinate(value, "longitude")
    )

    # Validasi pasangan koordinat.
    invalid_pair = df["latitude"].isna() | df["longitude"].isna()

    print("\nPemeriksaan data fasilitas:")
    print(f"Jumlah fasilitas: {len(df):,}")
    print(f"Luas kosong/tidak valid: {df['luas_m2'].isna().sum():,}")
    print(f"Latitude kosong/tidak valid: {df['latitude'].isna().sum():,}")
    print(f"Longitude kosong/tidak valid: {df['longitude'].isna().sum():,}")
    print(f"Pasangan koordinat belum lengkap: {invalid_pair.sum():,}")

    # Tampilkan sampel untuk pemeriksaan manual.
    preview_columns = [
        col for col in [
            "nama_venue",
            "luas_m2",
            "latitude",
            "longitude",
        ]
        if col in df.columns
    ]

    print("\nContoh hasil pembersihan:")
    print(df[preview_columns].head(10).to_string(index=False))

    return df


def load_csv_to_duckdb(database_name: str, csv_name: str) -> None:
    csv_path = RAW_DIR / csv_name
    db_path = DB_DIR / f"{database_name}.duckdb"

    if not csv_path.exists():
        raise FileNotFoundError(f"File CSV tidak ditemukan: {csv_path}")

    # Baca CSV dengan delimiter titik koma.
    df = pd.read_csv(
        csv_path,
        sep=";",
        encoding="utf-8-sig",
        dtype={"latitude": "string", "longitude": "string"},
    )

    df.columns = df.columns.str.strip()

    print(f"\n{'=' * 55}")
    print(f"Memproses: {csv_name}")
    print(f"Jumlah baris: {len(df):,}")
    print(f"Kolom: {list(df.columns)}")

    # Pembersihan khusus fasilitas.
    if database_name == "bebek_fasilitas":
        df = clean_facility_data(df)

    # Ganti tabel lama dengan data terbaru dari CSV.
    with duckdb.connect(str(db_path)) as con:
        con.register("source_df", df)

        con.execute(
            f'CREATE OR REPLACE TABLE "{database_name}" AS '
            "SELECT * FROM source_df"
        )

        con.unregister("source_df")

        total_rows = con.execute(
            f'SELECT COUNT(*) FROM "{database_name}"'
        ).fetchone()[0]

        print("\nTipe data di DuckDB:")
        schema = con.execute(
            f'DESCRIBE SELECT * FROM "{database_name}"'
        ).fetchdf()
        print(schema.to_string(index=False))

        if database_name == "bebek_fasilitas":
            print("\nValidasi nilai yang tersimpan:")
            print(
                con.execute(
                    """
                    SELECT
                        nama_venue,
                        luas_m2,
                        latitude,
                        longitude
                    FROM bebek_fasilitas
                    LIMIT 10
                    """
                ).fetchdf().to_string(index=False)
            )

    print(f"\nDatabase: {db_path.name}")
    print(f"Tabel: {database_name}")
    print(f"Baris tersimpan: {total_rows:,}")


def main() -> None:
    print("=== LOAD DATA KE DUCKDB ===")

    for database_name, csv_name in DATASETS.items():
        load_csv_to_duckdb(database_name, csv_name)

    print("\nSemua dataset selesai dimuat.")


if __name__ == "__main__":
    main()
