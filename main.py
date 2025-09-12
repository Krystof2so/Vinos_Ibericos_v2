import folium  # sert à générer une carte interactive (basée sur Leaflet.js)
import json

from PySide6.QtWidgets import QApplication, QMainWindow

# Composant Qt qui affiche du contenu web (HTML, CSS, JavaScript) :
from PySide6.QtWebEngineWidgets import QWebEngineView


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # La fenêtre :
        self.setWindowTitle("Vinos Ibericos")
        self.setGeometry(150, 150, 1200, 950)  # Position et dimensions

        # Création de la carte folium (centrée sur Madrid):
        spain_map = folium.Map(location=[40.0, -3.3], zoom_start=7)

        # Lecture du fichier JSON et ajout des marqueurs
        with open("towns.json", encoding="utf-8") as f:
            towns = json.load(f)

        for town in towns:
            folium.Marker(
                location=town["coords"],
                popup=town["popup"],
                tooltip=town["nom"],
                icon=folium.CustomIcon(icon_image="tinto.png", icon_size=(40, 40)),
            ).add_to(spain_map)

        # Rendu HTML en mémoire :
        html_data = spain_map.get_root().render()

        # Création du widget WebEngineView (navigateur intégré):
        self.browser = QWebEngineView()
        self.browser.setHtml(html_data)  # Chargement direct du HTML
        self.setCentralWidget(self.browser)  # Navigateur comme unique widget central


if __name__ == "__main__":
    app = QApplication()
    window = MapWindow()
    window.show()
    app.exec()
