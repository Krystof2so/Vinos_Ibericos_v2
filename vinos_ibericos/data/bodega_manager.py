#########################################
# vinos_ibericos/data/bodega_manager.py #
#                                       #
# Gestionnaire Python de la db :        #
# - Se charge de la connexion à SQLite  #
# - Fournit les méthodes CRUD           #
#########################################

from pathlib import Path
from typing import Optional, Union

import sqlite3


# Chemin par défaut du fichier de base de données (même répertoire que ce fichier) :
DEFAULT_DB_PATH = Path(__file__).parent / "bodegas.db"

# Schéma de la table bodegas (requête SQLite):
CREATE_BODEGAS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS bodegas (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    cp INTEGER,
    town TEXT NOT NULL,
    street TEXT,
    number INTEGER,
    comp TEXT,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    website TEXT,
    do_name TEXT NOT NULL
);
"""


def create_bodegas_table(conn: sqlite3.Connection) -> None:
    """Crée la table `bodegas` si n'existe pas."""
    cursor = conn.cursor()
    cursor.execute(CREATE_BODEGAS_TABLE_SQL)
    conn.commit()


def init_db(db_path: Optional[Union[str, Path]] = None) -> sqlite3.Connection:
    """
    Initialise la base SQLite et s'assure que la table `bodegas` existe.
    - db_path: chemin vers le fichier sqlite (str ou Path). Par défaut vinos_ibericos/data/bodegas.db
    Retourne la connexion sqlite3.Connection ouverte.
    """
    db_path = (
        Path(db_path) if db_path else DEFAULT_DB_PATH
    )  # répertoire à créer si nécessaire
    db_path.parent.mkdir(parents=True, exist_ok=True)  # s'assurer que le dossier existe
    conn = sqlite3.connect(str(db_path))
    conn.execute(
        "PRAGMA foreign_keys = ON;"
    )  # activer les clés étrangères (si ajout plus tard)
    create_bodegas_table(conn)  # Exécution de la requête + commit
    return conn


if __name__ == "__main__":
    # A utiliser localement pour vérification sans lancer toute l'application
    conn = init_db()
    print(f"Database initialisée : {DEFAULT_DB_PATH.resolve()}")
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='bodegas';"
    )  # vérifier la présence de la table
    found = cur.fetchone() is not None
    print("Table 'bodegas' créée :", found)
    conn.close()
