from pathlib import Path
import folium

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


class MapManager:
    def __init__(self, vinedos, default_center=[40.0, -3.3], default_zoom=7):
        self.vinedos = vinedos
        self.default_center = default_center
        self.default_zoom = default_zoom
        self.icon_path = ASSETS_DIR / "tinto.png"

    def generate_map_html(self, center=None, zoom=None):
        """Génère le HTML de la carte avec tous les marqueurs"""
        center = center or self.default_center
        zoom = zoom or (10 if center != self.default_center else self.default_zoom)
        spain_map = folium.Map(location=center, zoom_start=zoom)

        for v in self.vinedos:
            folium.Marker(
                location=v["coords"],
                tooltip=self._format_tooltip(v["nom"]),
                popup=self._format_popup(v),
                icon=folium.CustomIcon(
                    icon_image=str(self.icon_path), icon_size=(40, 40)
                ),
            ).add_to(spain_map)

        return spain_map.get_root().render()

    def _format_tooltip(self, name):
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

    def _format_popup(self, vinedo):
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
