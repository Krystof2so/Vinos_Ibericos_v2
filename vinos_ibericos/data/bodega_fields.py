# vinos_ibericos/data/bodega_fields.py

TABLE_NAME = "bodegas"

# Tuple : (clé, label, obligatoire, type)
FIELDS = (
    ("name", "Nom de la Bodega", True, str),
    ("cp", "Code postal", False, int),
    ("town", "Nom de la ville", True, str),
    ("street", "Rue", False, str),
    ("number", "Numéro", False, int),
    ("comp", "Complément", False, str),
    ("lat", "Latitude", True, float),
    ("lon", "Longitude", True, float),
    ("website", "Site web", False, str),
    ("do_name", "Nom de la DO", True, str),
)


def generate_create_table_sql() -> str:
    """
    Génère la requête SQL CREATE TABLE à partir de FIELDS.
    """
    sql_fields = []
    for key, _, required, typ in FIELDS:
        if isinstance(typ, int):
            sql_type = "INTEGER"
        elif isinstance(typ, float):
            sql_type = "REAL"
        else:
            sql_type = "TEXT"
        not_null = "NOT NULL" if required else ""
        sql_fields.append(f"{key} {sql_type} {not_null}".strip())

    # Ajouter la colonne id en PK
    sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER PRIMARY KEY,
        {",\n        ".join(sql_fields)}
    );
    """
    return sql
