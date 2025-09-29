################################
# vinos_ibericos/datatypes.py  #
#                              #
# Classes des types de données #
# ##############################

from typing import TypedDict


class Vinedo(TypedDict):
    nom: str
    coords: list[float]
    description: str
    img: str
