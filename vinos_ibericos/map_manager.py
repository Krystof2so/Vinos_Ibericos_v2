from pathlib import Path
import folium


class MapManager:
    def __init__(self, vinedos):
        self.vinedos = vinedos
        self.icon_path = Path(__file__).parent.parent / "assets" / "tinto.png"

    def generate_map_html(self, center=None):
        """Génère le HTML de la carte avec tous les marqueurs"""
        zoom = 10 if center else 7
        spain_map = folium.Map(location=center or [40.0, -3.3], zoom_start=zoom)

        for v in self.vinedos:
            auto_open = center == v["coords"]
            folium.Marker(
                location=v["coords"],
                tooltip=self._format_tooltip(v["nom"]),
                popup=folium.Popup(
                    self._format_popup(v), max_width=400, show=auto_open
                ),
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
