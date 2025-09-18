from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional, TypedDict

import folium


@dataclass(frozen=True)
class MapConfig:
    CENTRE_OF_SPAIN: tuple[float, float] = (40.0, -3.3)
    INIT_ZOOM: int = 7
    FOCUS_ZOOM: int = 10
    WIDTH_POPUP: int = 400


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
    def __init__(self, vinedos: list[dict[str, Any]]) -> None:
        self.vinedos: list[dict[str, Any]] = vinedos

    def generate_map_html(self, vinedo_filter: Optional[str] = None) -> str:
        """
        Génère le HTML de la carte.
        - vinedo_filter=None => vue globale avec tous les marqueurs
        - vinedo_filter="Nom du vignoble" => vue détaillée avec uniquement ce vignoble
        """
        if vinedo_filter:
            v = next((x for x in self.vinedos if x["nom"] == vinedo_filter), None)
            if not v:
                return self._generate_map(self.vinedos)  # fallback global
            return self._generate_map([v], focus=True)
        else:
            return self._generate_map(self.vinedos)

    def _generate_map(self, vinedos: list[dict[str, Any]], focus: bool = False) -> str:
        """
        Crée une carte folium avec un ou plusieurs vignobles.
        - focus=True => zoom + popup
        """
        center, zoom = (
            (vinedos[0]["coords"], MapConfig.FOCUS_ZOOM)
            if focus and vinedos
            else (MapConfig.CENTRE_OF_SPAIN, MapConfig.INIT_ZOOM)
        )
        spain_map = folium.Map(location=center, zoom_start=zoom)
        for v in vinedos:
            self._add_marker(spain_map, v, focus)
        return spain_map.get_root().render()

    def _add_marker(
        self, fmap: folium.Map, vinedo: dict[str, Any], focus: bool
    ) -> None:
        """
        Ajoute un marqueur pour un vignoble donné.
        - focus=True => plus gros icône + popup
        """
        # Définitions des paramètres du marqueur selon le focus :
        icon_size = IconConfig.FOCUS_SIZE if focus else IconConfig.INIT_SIZE
        popup = (
            folium.Popup(
                self._format_popup(vinedo), max_width=MapConfig.WIDTH_POPUP, show=True
            )
            if focus
            else None
        )
        folium.Marker(
            location=vinedo["coords"],
            tooltip=self._format_tooltip(vinedo["nom"]),
            popup=popup,
            icon=folium.CustomIcon(str(IconConfig.WINE_ICON), icon_size=icon_size),
        ).add_to(fmap)

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

    def _format_popup(self, vinedo: Dict[str, Any]) -> str:
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
