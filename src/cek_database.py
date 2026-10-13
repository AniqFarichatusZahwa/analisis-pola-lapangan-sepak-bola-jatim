
from pathlib import Path
import duckdb

ROOT_DIR = Path(__file__).resolve().parent.parent
DB_DIR = ROOT_DIR / "data" / "processed"

databases = {
    "Fasilitas": ("bebek_fasilitas.duckdb", "data_fasilitas"),
    "Soeratin": ("bebek_soeratin.duckdb", "data_soeratin"),
    "Liga 1": ("bebek_liga1.duckdb", "data_liga1"),
    "AFF U-19": ("bebek_aff.duckdb", "data_aff"),
}

for nama, (db_file, tabel) in databases.items():
    db_path = DB_DIR / db_file
    con = duckdb.connect(str(db_path), read_only=True)

    print(f"\n{'=' * 45}")
    print(f"DATASET: {nama}")

    print("\nContoh 5 baris data:")
    print(con.execute(
        f'SELECT * FROM "{tabel}" LIMIT 5'
    ).df().to_string(index=False))

    print("\nJumlah baris:")
    print(con.execute(
        f'SELECT COUNT(*) FROM "{tabel}"'
    ).fetchone()[0])

    con.close()
