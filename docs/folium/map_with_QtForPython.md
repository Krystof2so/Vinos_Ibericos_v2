# Insérer une carte dans une UI avec QtForPython

```python
import folium  # sert à générer une carte interactive (basée sur Leaflet.js)
from PySide6.QtWidgets import QApplication, QMainWindow
# Composant Qt qui affiche du contenu web (HTML, CSS, JavaScript) :
from PySide6.QtWebEngineWidgets import QWebEngineView


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # La fenêtre :
        self.setWindowTitle("Carte Folium avec PySide6")
        self.setGeometry(200, 200, 1000, 800) # Position et dimensions

        # Création de la carte folium (centrée sur Madrid):
        map_fol = folium.Map(location=[40.4168, -3.7038], zoom_start=6)

        # Rendu HTML en mémoire :
        html_data = map_fol.get_root().render()

        # Création du widget WebEngineView (navigateur intégré):
        self.browser = QWebEngineView()
        self.browser.setHtml(html_data) # Chargement direct du HTML
        self.setCentralWidget(self.browser) # Navigateur comme unique widget central


if __name__ == "__main__":
    app = QApplication()
    window = MapWindow()
    window.show()
    app.exec()
```


