####################################
# vinos_ibericos/config/general.py #
#                                  #
# Sont regroupées ici toutes les   #
# configurations générales         #
# utilisées pour l'ensemble de     #
# l'application.                   #
# ##################################

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ConfigPath:
    """Configuration des chemins de répertoires et de fichiers."""

    # Répertoires
    BASE_DIR_PROJECT: Path = Path(__file__).resolve().parent.parent.parent
    # fichiers
    JSON_FILE_PATH: Path = BASE_DIR_PROJECT / "vinedos.json"
