import sqlite3
import pytest
from vinos_ibericos.data.bodega_manager import CREATE_BODEGAS_TABLE_SQL


@pytest.fixture
def db_connection():
    # Base SQLite en mémoire (nouvelle BDD pour chaque test)
    conn = sqlite3.connect(":memory:")
    conn.execute(CREATE_BODEGAS_TABLE_SQL)
    yield conn
    conn.close()


def test_insert_bodega(db_connection):
    sql_insert = """
    INSERT INTO bodegas (name, cp, town, street, number, comp, lat, lon, website, do_name)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    values = (
        "Bodega Test",
        12345,
        "Testville",
        "Rue des Vins",
        42,
        "Batiment B",
        12.345,
        67.890,
        "https://bodega-test.com",
        "DO Test",
    )

    cur = db_connection.cursor()
    cur.execute(sql_insert, values)
    db_connection.commit()
    new_id = cur.lastrowid

    # Vérification
    cur = db_connection.execute("SELECT * FROM bodegas WHERE id = ?", (new_id,))
    row = cur.fetchone()

    assert row is not None
    assert row[1] == "Bodega Test"
    assert row[2] == 12345
    assert row[3] == "Testville"
    assert row[6] == 12.345  # lat
    assert row[7] == 67.890  # lon
    assert row[9] == "DO Test"
