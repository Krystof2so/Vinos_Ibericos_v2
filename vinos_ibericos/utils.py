###########################
# vinos_ibericos/utils.py #
#                         #
# Ensemble de fonctions   #
# utilitaires.            #
###########################

import json

from contextlib import contextmanager
from pathlib import Path
from typing import Any

from PySide6.QtCore import QObject

from vinos_ibericos.datatypes import Vinedo
from vinos_ibericos.config.general import ConfigPath
from vinos_ibericos.config.strings import ErrorMsg


class CheckVinedoJson:
    def __init__(self, file_path: Path | None = None) -> None:
        # Possibilité de passer un autre chemin si besoin (tests, etc.)
        self.file_path: Path = file_path or ConfigPath.JSON_FILE_PATH
        self._data: list[Vinedo] = []

    def load(self) -> None:
        """Charge et valide les données depuis le JSON et les stocke en mémoire."""
        try:
            with open(self.file_path, encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Fichier introuvable: {self.file_path}")
            data = []
        except json.JSONDecodeError as e:
            print(f"Erreur JSON: {e}")
            data = []
        self._data = (
            [item for item in data if self._is_vinedo(item)]
            if isinstance(data, list)
            else []
        )

    @property
    def data(self) -> list[Vinedo]:
        """Retourne les données validées déjà chargées."""
        return self._data

    @staticmethod
    def _is_vinedo(item: dict[str, Any]) -> bool:
        """Vérifie la validité d'un Vinedo"""
        required_keys: dict[str, type] = {
            "nom": str,
            "coords": list,
            "description": str,
            "img": str,
        }
        # Vérifie la présence et le type de chaque clé :
        for key, expected_type in required_keys.items():
            if key not in item or not isinstance(item[key], expected_type):
                return False
        # Vérification spécifique : coords doit être une liste de float
        if not all(isinstance(x, float) for x in item["coords"]):
            return False
        return True


@contextmanager
def suspend_signals(widget: QObject):
    """Contexte pour bloquer temporairement les signaux d'un widget Qt."""
    widget.blockSignals(True)
    try:
        yield
    finally:
        widget.blockSignals(False)


def load_datas() -> list[Vinedo]:
    """Chargement des données depuis JSON"""
    try:
        with open(ConfigPath.JSON_FILE_PATH, encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except FileNotFoundError:
        print(ErrorMsg.NOT_FOUND_FILE)
    except json.JSONDecodeError as e:
        print(ErrorMsg.JSON_DECODE_ERROR, e)
    return []
