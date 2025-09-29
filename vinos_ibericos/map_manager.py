from dataclasses import dataclass
from json import load, JSONDecodeError
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import folium

from vinos_ibericos.ui.config_ui import Colors
from vinos_ibericos.datatypes import Vinedo


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


@dataclass(frozen=True)
class PathConfig:
    WINE_ICON: Path = Path(__file__).parent.parent / "assets" / "tinto.png"
    GEOJSON_DIR: Path = Path(__file__).parent.parent / "assets" / "geojson"


class MapManager:
    def __init__(self, vinedos: list[Vinedo]) -> None:
        self.vinedos: list[Vinedo] = vinedos
        self._current_vinedos: list[Vinedo] = []

    def generate_map_html(self, vinedo_filter: Optional[str] = None) -> str:
        """
        Génère le HTML de la carte.
        - vinedo_filter=None => vue globale avec tous les marqueurs
        - vinedo_filter="Nom du vignoble" => vue détaillée avec uniquement ce vignoble
        """
        if vinedo_filter:
            self._current_vinedos = [
                v for v in self.vinedos if v["nom"] == vinedo_filter
            ] or self.vinedos  # fallback global si nom non trouvé
        else:
            self._current_vinedos = self.vinedos

        focus = vinedo_filter is not None
        return self._generate_map(focus=focus)

    def _generate_map(self, focus: bool = False) -> str:
        """
        Crée une carte folium avec un ou plusieurs vignobles.
        - focus=True => zoom + popup
        """
        if self._current_vinedos and focus:
            center = self._current_vinedos[0]["coords"]
            zoom = MapConfig.FOCUS_ZOOM
        else:
            center = MapConfig.CENTRE_OF_SPAIN
            zoom = MapConfig.INIT_ZOOM

        fmap = folium.Map(location=center, zoom_start=zoom)
        for vinedo in self._current_vinedos:
            self._add_marker(fmap, vinedo, focus)
        return fmap.get_root().render()

    def _add_marker(self, fmap: folium.Map, vinedo: Vinedo, focus: bool) -> None:
        """
        Ajoute un marqueur pour un vignoble donné.
        - focus=True => plus gros icône + popup
        - Ajout d'un polygone représentant la région si coordonnées présentes dans le .json
        """
        # Définitions des paramètres du marqueur selon le focus :
        icon_size = IconConfig.FOCUS_SIZE if focus else IconConfig.INIT_SIZE
        folium.Marker(
            location=vinedo["coords"],
            tooltip=self._format_tooltip(vinedo["nom"]),
            icon=folium.CustomIcon(str(PathConfig.WINE_ICON), icon_size=icon_size),
        ).add_to(fmap)

        # Pour le polygone
        if focus:
            polygone, coords_polygone = self._f_polygone(vinedo["nom"])
            if polygone:
                polygone.add_to(fmap)
                fmap.fit_bounds(coords_polygone)

    def _format_tooltip(self, name: str) -> str:
        return f"""
            <div style='
                font-size:18px;
                font-weight:bold;
                color:{Colors.BACKGROUND_LIGHT};
                background-color:{Colors.PRIMARY_MAIN};
                padding:2px 4px; 
                border-radius:3px;
                border: 2px solid {Colors.BORDER_COLOR};
            '>{name}</div>
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

    def _f_polygone(
        self, name: str, geojson_dir: Path = PathConfig.GEOJSON_DIR
    ) -> Tuple[Optional[folium.Polygon], List[List[float]]]:
        """
        Création du polygone permettant de tracer la région viticole sélectionnée.
        - Extraction des données depuis un fichier .geojson. Retourne un objet folium.Polygon.
        """
        geojson_file: Path = geojson_dir / f"{name.lower().replace(' ', '_')}.geojson"
        # Charger le fichier GeoJSON s'il existe :
        try:
            with open(geojson_file, "r", encoding="utf-8") as f:
                geojson_data = load(f)
        except FileNotFoundError:
            return None, []
        except JSONDecodeError:
            return None, []
        # Extraire les coordonnées du polygone (si fichier .geojson bien formaté)
        try:
            # GeoJSON : geojson_data['features'][0]['geometry']['coordinates'][0]
            raw_coords = geojson_data["features"][0]["geometry"]["coordinates"][0]
        except (KeyError, IndexError):
            return None, []
        # Inverser chaque coordonnée (lon, lat) -> (lat, lon)
        polygon_coords = [[lat, lon] for lon, lat in raw_coords]
        return folium.Polygon(
            locations=polygon_coords,
            color=Colors.PRIMARY_MAIN,
            fill=True,
            fill_color=Colors.PRIMARY_MAIN,
            fill_opacity=0.4,
            weight=3,
        ), polygon_coords
