####################################
# vinos_ibericos/config/strings.py #
#                                  #
# Données textuelles de            #
# l'application, sous forme de     #
# chaînes de caractères            #
####################################

from dataclasses import dataclass

from vinos_ibericos.config.general import ConfigPath


@dataclass(frozen=True)
class ErrorMsg:
    JSON_DECODE_ERROR: str = "Erreur JSON:"
    NOT_FOUND_FILE: str = f"Fichier {ConfigPath.JSON_FILE_PATH.name} introuvable"
