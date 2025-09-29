###########################
# vinos_ibericos/utils.py #
#                         #
# Ensemble de fonctions   #
# utilitaires.            #
###########################

import json

from contextlib import contextmanager

from PySide6.QtCore import QObject

from vinos_ibericos.datatypes import Vinedo
from vinos_ibericos.config.general import ConfigPath
from vinos_ibericos.config.strings import ErrorMsg


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
            return []
    except FileNotFoundError:
        print(ErrorMsg.NOT_FOUND_FILE)
        return []
    except json.JSONDecodeError as e:
        print(ErrorMsg.JSON_DECODE_ERROR, e)
        return []
