import sys
import json
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap
import folium


# --- Fenêtre Image ---
class ImageWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image de la ville")
        layout = QVBoxLayout()
        self.label = QLabel("Aucune ville sélectionnée")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.resize(500, 400)

    def show_image(self, image_path, title):
        self.setWindowTitle(title)
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.label.setPixmap(pixmap.scaled(480, 360, Qt.KeepAspectRatio))
        else:
            self.label.setText("Image introuvable")
        self.show()


# --- Fenêtre Boutons ---
class ButtonWindow(QWidget):
    city_selected = Signal(str)  # Signal émet le chemin de l'image

    def __init__(self, towns):
        super().__init__()
        self.setWindowTitle("Sélection de ville")
        layout = QVBoxLayout()
        for town in towns:
            btn = QPushButton(town["nom"])
            btn.clicked.connect(
                lambda checked,
                img=town["img"],
                name=town["nom"]: self.city_selected.emit(img + "||" + name)
            )
            layout.addWidget(btn)
        self.setLayout(layout)
        self.resize(200, 300)


# --- Fenêtre Carte ---
class MapWindow(QMainWindow):
    def __init__(self, towns):
        super().__init__()
        self.setWindowTitle("Carte Folium")
        self.setGeometry(100, 100, 800, 600)
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        spain_map = folium.Map(location=[40.0, -3.3], zoom_start=6)
        for town in towns:
            folium.Marker(
                location=town["coords"],
                tooltip=town["nom"],
                icon=folium.CustomIcon(icon_image="tinto.png", icon_size=(40, 40)),
            ).add_to(spain_map)

        html_data = spain_map.get_root().render()
        self.browser.setHtml(html_data)


# --- Exemple JSON en mémoire ---
towns = [
    {"nom": "Madrid", "coords": [40.4168, -3.7038], "img": "madrid.jpg"},
    {"nom": "Zaragoza", "coords": [41.6488, -0.8891], "img": "zaragoza.jpg"},
    {"nom": "Vigo", "coords": [42.2406, -8.7207], "img": "vigo.jpg"},
]

# --- Application ---
app = QApplication(sys.argv)

image_win = ImageWindow()
button_win = ButtonWindow(towns)
map_win = MapWindow(towns)


# Connecter le signal
def handle_city_selection(data):
    img_path, title = data.split("||")
    image_win.show_image(img_path, title)


button_win.city_selected.connect(handle_city_selection)

button_win.show()
map_win.show()

sys.exit(app.exec())
