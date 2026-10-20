from pathlib import Path
import duckdb

ROOT_DIR = Path(__file__).resolve().parent.parent
DUCKDB_DIR = ROOT_DIR / "data" / "duckdb"

sources = {
    "bebek_fasilitas.duckdb": "bebek_fasilitas",
    "bebek_soeratin.duckdb": "bebek_soeratin",
    "bebek_liga1.duckdb": "bebek_liga1",
    "bebek_aff.duckdb": "bebek_aff",
}

for db_file, table in sources.items():
    print(f"\n{'=' * 60}")
    print(f"DATABASE: {db_file}")
    con = duckdb.connect(str(DUCKDB_DIR / db_file), read_only=True)

    print(f"\nSTRUKTUR TABEL: {table}")
    print(con.execute(f'DESCRIBE "{table}"').fetchdf().to_string(index=False))

    print(f"\nCONTOH DATA: {table}")
    print(con.execute(f'SELECT * FROM "{table}" LIMIT 3').fetchdf().to_string(index=False))

    con.close()