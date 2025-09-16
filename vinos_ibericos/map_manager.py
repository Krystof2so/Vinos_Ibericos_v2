from dataclasses import dataclass
from pathlib import Path
from typing import Optional, TypedDict

import folium


@dataclass(frozen=True)
class MapConfig:
    CENTRE_OF_SPAIN: tuple[float, float] = (40.0, -3.3)
    INIT_ZOOM: int = 7
    FOCUS_ZOOM: int = 10


@dataclass(frozen=True)
class IconConfig:
    INIT_SIZE: tuple[int, int] = (40, 40)
    FOCUS_SIZE: tuple[int, int] = (60, 60)
    WINE_ICON: Path = Path(__file__).parent.parent / "assets" / "tinto.png"


class Vinedo(TypedDict):
    nom: str
    coords: list[float]
    description: str
    img: str


class MapManager:
    def __init__(self, vinedos: list[Vinedo]) -> None:
        self.vinedos: list[Vinedo] = vinedos

    def generate_map_html(self, vinedo_filter: Optional[str] = None) -> str:
        """
        Génère le HTML de la carte.
        - vinedo_filter=None => vue globale avec tous les marqueurs
        - vinedo_filter="Nom du vignoble" => vue détaillée avec uniquement ce vignoble
        """
        return (
            self._generate_detailed_map(vinedo_filter)
            if vinedo_filter
            else self._generate_global_map()
        )

    def _generate_global_map(self) -> str:
        """
        Carte avec tous les vignobles.
        Figurent seulement les icônes et les tooltips.
        """
        spain_map = folium.Map(
            location=MapConfig.CENTRE_OF_SPAIN, zoom_start=MapConfig.INIT_ZOOM
        )
        for v in self.vinedos:  # Boucle sur tous les vignobles
            folium.Marker(
                location=v["coords"],
                tooltip=self._format_tooltip(v["nom"]),
                icon=folium.CustomIcon(
                    str(IconConfig.WINE_ICON), icon_size=IconConfig.INIT_SIZE
                ),
            ).add_to(spain_map)
        return spain_map.get_root().render()

    def _generate_detailed_map(self, vinedo_name: str) -> str:
        """Carte centrée sur un seul vignoble"""
        # On récupère les infos du vignoble demandé :
        v = next((x for x in self.vinedos if x["nom"] == vinedo_name), None)
        if not v:
            return self._generate_global_map()  # fallback si erreur (carte générale)
        spain_map = folium.Map(location=v["coords"], zoom_start=MapConfig.FOCUS_ZOOM)
        folium.Marker(
            location=v["coords"],
            tooltip=self._format_tooltip(v["nom"]),
            popup=folium.Popup(self._format_popup(v), max_width=400, show=True),
            icon=folium.CustomIcon(
                str(IconConfig.WINE_ICON), icon_size=IconConfig.FOCUS_SIZE
            ),
        ).add_to(spain_map)
        return spain_map.get_root().render()

    def _format_tooltip(self, name: str) -> str:
        return f"""
            <span style='
                font-size:18px;
                font-weight:bold;
                color:purple;
                background-color:lightgrey;
                padding:2px 4px;
                border-radius:3px;
            '>{name}</span>
        """

    def _format_popup(self, vinedo: Vinedo) -> str:
        return f"""
            <div style='
                font-size:16px;
                line-height:1.4;
                color:#333;
                background-color:#f0f0f0;
                padding:8px;
                border-radius:6px;
                width:400px;
            '>
                <strong style="font-size:20px;color:red;">{vinedo["nom"]}</strong><br>
                {vinedo["description"]}
            </div>
        """
