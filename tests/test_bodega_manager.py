import pytest
import sqlite3
from vinos_ibericos.data.bodega_manager import BodegaManager, CREATE_BODEGAS_TABLE_SQL


# ========================
# Fixtures
# ========================


@pytest.fixture
def db_manager():
    """Retourne un BodegaManager avec une BDD SQLite en mémoire (propre à chaque test)."""
    conn = sqlite3.connect(":memory:")
    conn.execute(CREATE_BODEGAS_TABLE_SQL)
    manager = BodegaManager()
    manager.conn = conn  # injection de la connexion in-memory
    yield manager
    conn.close()


@pytest.fixture
def sample_bodega_data():
    """Données de test de base pour une bodega."""
    return {
        "name": "Bodega Test",
        "cp": 12345,
        "town": "Testville",
        "street": "Rue des Vins",
        "number": 42,
        "comp": "Batiment B",
        "lat": 12.345,
        "lon": 67.890,
        "website": "https://bodega-test.com",
        "do_name": "DO Test",
    }


# ========================
# Helpers
# ========================


def assert_bodega_exists(conn, bodega_id, expected_data=None):
    """Vérifie qu'une bodega existe et correspond aux données attendues (optionnel)."""
    cur = conn.execute("SELECT * FROM bodegas WHERE id = ?", (bodega_id,))
    row = cur.fetchone()
    assert row is not None, f"Bodega {bodega_id} introuvable dans la BDD."
    if expected_data:
        assert row[1] == expected_data["name"]
        assert row[2] == expected_data["cp"]
        assert row[3] == expected_data["town"]
        assert row[7] == expected_data["lat"]
        assert row[8] == expected_data["lon"]
        assert row[10] == expected_data["do_name"]
    return row


def assert_bodega_not_exists(conn, bodega_id):
    """Vérifie qu'une bodega n'existe pas dans la table."""
    cur = conn.execute("SELECT COUNT(*) FROM bodegas WHERE id = ?", (bodega_id,))
    assert cur.fetchone()[0] == 0


# ========================
# Tests
# ========================


def test_add_bodega(db_manager, sample_bodega_data):
    new_id = db_manager.add_bodega(sample_bodega_data)
    assert isinstance(new_id, int) and new_id > 0
    assert_bodega_exists(db_manager.conn, new_id, sample_bodega_data)


def test_delete_bodega(db_manager, sample_bodega_data):
    # 1️⃣ Insérer une bodega à supprimer
    data = sample_bodega_data.copy()
    data["name"] = "Bodega à supprimer"
    data["number"] = 1
    new_id = db_manager.add_bodega(data)
    # 2️⃣ Vérifier qu'elle existe
    assert_bodega_exists(db_manager.conn, new_id)
    # 3️⃣ Supprimer
    deleted = db_manager.delete_bodega(new_id)
    assert deleted is True
    # 4️⃣ Vérifier qu'elle n'existe plus
    assert_bodega_not_exists(db_manager.conn, new_id)
    # 5️⃣ Supprimer un ID inexistant
    assert db_manager.delete_bodega(9999) is False


def test_get_bodega_existing(db_manager, sample_bodega_data):
    # 1️⃣ On insère une bodega
    new_id = db_manager.add_bodega(sample_bodega_data)

    # 2️⃣ On la récupère via la méthode
    bodega = db_manager.get_bodega(new_id)

    # 3️⃣ Vérifications
    assert bodega is not None
    assert bodega["id"] == new_id
    assert bodega["name"] == sample_bodega_data["name"]
    assert bodega["town"] == sample_bodega_data["town"]
    assert bodega["lat"] == sample_bodega_data["lat"]
    assert bodega["lon"] == sample_bodega_data["lon"]
    assert bodega["do_name"] == sample_bodega_data["do_name"]


def test_get_bodega_nonexistent(db_manager):
    # 1️⃣ On tente de récupérer une bodega qui n’existe pas
    bodega = db_manager.get_bodega(9999)

    # 2️⃣ Vérification : None attendu
    assert bodega is None


def test_get_all_bodegas(db_manager, sample_bodega_data):
    # On commence avec une base vide
    bodegas = db_manager.get_all_bodegas()
    assert bodegas == [], "La liste doit être vide au départ"

    # On ajoute deux bodegas
    bodega1_id = db_manager.add_bodega(sample_bodega_data)
    bodega2_id = db_manager.add_bodega(
        {
            "name": "Bodega Dos",
            "cp": 54321,
            "town": "Ville B",
            "street": "Avenida de la Uva",
            "number": 22,
            "comp": "",
            "lat": 41.0,
            "lon": -4.0,
            "website": "http://dos.com",
            "do_name": "DO B",
        }
    )

    bodegas = db_manager.get_all_bodegas()
    assert len(bodegas) == 2, "Il devrait y avoir exactement deux bodegas"

    ids = [b["id"] for b in bodegas]
    assert bodega1_id in ids
    assert bodega2_id in ids

    names = [b["name"] for b in bodegas]
    assert "Bodega Test" in names
    assert "Bodega Dos" in names
