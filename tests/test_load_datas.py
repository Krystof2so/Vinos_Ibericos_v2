# tests/test_load_datas.py
import json
import pytest

from vinos_ibericos.main import load_datas, Config


@pytest.fixture
def prepare_json(tmp_path, monkeypatch):
    """
    Fixture qui prépare un fichier JSON temporaire et monkeypatch Config.
    Renvoie une fonction interne que le test peut appeler avec ses propres données.
    """

    # Fixtures de 'pytest' pour isoler les tests du projet :
    # 'tmp_path' crée un répertoire temporaire unique pour ce test.
    # 'monkeypatch' permet de remplacer temporairement une variable, une fonction ou un attribut.
    def _prepare(file_content=None, file_exists=True):
        # 1. Création du fichier temporaire avec des valeurs de test :
        json_file = tmp_path / "vinedos.json"
        if file_exists and file_content is not None:
            # Si le contenu est une liste Python, on le convertit en JSON
            json_file.write_text(
                json.dumps(file_content)
                if isinstance(file_content, list)
                else file_content,
                encoding="utf-8",
            )
        elif not file_exists:
            # On s'assure que le fichier n'existe pas
            if json_file.exists():
                json_file.unlink()
        # 2. Forcer Config à pointer vers le fichier temporaire
        monkeypatch.setattr(Config, "JSON_FILE_PATH", json_file)
        return json_file

    return _prepare


def test_load_datas_returns_list_of_dicts(prepare_json):
    """Test du scénario “succès” avec JSON valide."""
    test_values = [{"nom": "TestVinedo", "coords": [40.0, -3.3]}]
    prepare_json(file_content=test_values)
    # Exécution de la fonction load_datas et récupération du return :
    result = load_datas()
    # Vérifications :
    assert isinstance(result, list)  # Retourne une liste
    assert all(
        isinstance(item, dict) for item in result
    )  # Chaque élément de la liste = dictionnaire
    assert result == test_values  # Comparaison


@pytest.mark.parametrize(
    "file_content, file_exists",
    [
        ("", True),  # fichier vide
        ("INVALID_JSON", True),  # fichier mal formé
        (None, False),  # fichier absent
    ],
)
def test_load_datas_returns_empty_list_on_error(
    prepare_json, file_content, file_exists
):
    prepare_json(file_content=file_content, file_exists=file_exists)
    result = load_datas()
    assert isinstance(result, list)
    assert result == []
