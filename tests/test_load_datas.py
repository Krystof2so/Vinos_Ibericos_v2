# tests/test_load_datas.py
import json

from vinos_ibericos.main import load_datas, Config


def test_load_datas_returns_list_of_dicts(tmp_path, monkeypatch):
    # Fixtures de 'pytest' pour isoler les tests du projet :
    # 'tmp_path' crée un répertoire temporaire unique pour ce test.
    # 'monkeypatch' permet de remplacer temporairement une variable, une fonction ou un attribut.
    # 1. Création du fichier temporaire avec des valeurs de test :
    test_values = [{"nom": "TestVinedo", "coords": [40.0, -3.3]}]
    json_file = tmp_path / "vinedos.json"
    json_file.write_text(json.dumps(test_values), encoding="utf-8")
    # 2. Forcer Config à pointer vers ce fichier :
    monkeypatch.setattr(Config, "JSON_FILE_PATH", json_file)
    # 3. Exécution de la fonction load_datas et récupération du return :
    result = load_datas()
    # 4. Vérifications simples :
    assert isinstance(result, list)  # Retourne une liste
    assert all(
        isinstance(item, dict) for item in result
    )  # Chaque élément de la liste = dictionnaire
    assert result == test_values  # Comparaison
