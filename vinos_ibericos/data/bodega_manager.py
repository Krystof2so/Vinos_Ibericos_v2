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

from vinos_ibericos.data import bodega_fields


# Chemin par défaut du fichier de base de données (même répertoire que ce fichier) :
DEFAULT_DB_PATH = Path(__file__).parent / "bodegas.db"

# Schéma de la table bodegas (requête SQLite):
CREATE_BODEGAS_TABLE_SQL = bodega_fields.generate_create_table_sql()


class BodegaManager:
    def __init__(self, db_path: Optional[Union[str, Path]] = None):
        """Initialise le gestionnaire et ouvre la connexion à la base SQLite."""
        self.conn = init_db(db_path)

    def add_bodega(self, data: dict) -> Optional[int]:
        """Insère une bodega dans la base."""
        # Colonnes à insérer : toutes les clés du tuple FIELDS
        columns = [field[0] for field in bodega_fields.FIELDS]
        # Préparer les valeurs dans le bon ordre
        values = []
        for key, _, _, typ in bodega_fields.FIELDS:
            val = data.get(key)
            # Conversion de type automatique si nécessaire
            if val is not None:
                try:
                    val = typ(val)
                except ValueError:
                    raise ValueError(
                        f"Erreur de conversion pour le champ '{key}' avec la valeur '{val}'"
                    )
            values.append(val)
        placeholders = ", ".join(["?"] * len(columns))
        sql = f"INSERT INTO bodegas ({', '.join(columns)}) VALUES ({placeholders})"
        cur = self.conn.cursor()
        cur.execute(sql, values)
        self.conn.commit()
        return cur.lastrowid

    def update_bodega(self, id: int, data: dict):
        """Modifie une bodega."""
        pass

    def delete_bodega(self, id: int) -> bool:
        """
        Supprime une bodega à partir de son ID.
        Retourne True si une ligne a été supprimée, False sinon.
        """
        sql = "DELETE FROM bodegas WHERE id = ?"
        cur = self.conn.cursor()
        cur.execute(sql, (id,))
        self.conn.commit()
        return cur.rowcount > 0

    def get_bodega(self, id: int) -> Optional[dict]:
        """Retourne une bodega par son ID, ou None si introuvable."""
        sql = "SELECT * FROM bodegas WHERE id = ?"
        cur = self.conn.execute(sql, (id,))
        row = cur.fetchone()
        if row is None:
            return None
        # Conversion tuple -> dict
        columns = [col[0] for col in cur.description]  # noms des colonnes
        return dict(zip(columns, row))

    def get_all_bodegas(self) -> list[dict]:
        """Retourne la liste de toutes les bodegas sous forme de dictionnaires."""
        sql = "SELECT * FROM bodegas"
        cur = self.conn.execute(sql)
        rows = cur.fetchall()

        if not rows:
            return []

        columns = [col[0] for col in cur.description]  # noms des colonnes
        return [dict(zip(columns, row)) for row in rows]


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
    manager = BodegaManager()
    # Récupérer toutes les bodegas
    bodegas = manager.get_all_bodegas()
    for b in bodegas:
        print(b["id"], b["name"], b["do_name"])
