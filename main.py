import sys
from functools import partial
import json
import os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
import folium


# --- Fenêtre Image ---
class ImageWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image du vignoble")
        layout = QVBoxLayout()
        self.label = QLabel("Aucune vignoble sélectionné")
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


# --- Fenêtre principale ---
class MainWindow(QMainWindow):
    vinedo_selected = Signal(str, str)  # (image_path, nom)

    def __init__(self, vinedos):
        super().__init__()
        self.setWindowTitle("Vinos Ibericos")
        self.setGeometry(150, 150, 1700, 1000)  # Position et dimensions

        # --- Widget central ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # --- Partie carte (QWebEngineView) ---
        self.browser = QWebEngineView()
        layout.addWidget(self.browser, stretch=3)  # plus large pour la carte

        # Générer la carte Folium
        spain_map = folium.Map(location=[40.0, -3.3], zoom_start=7)

        for vinedo in vinedos:
            folium.Marker(
                location=vinedo["coords"],
                tooltip=vinedo["nom"],
                popup=vinedo["description"],
                icon=folium.CustomIcon(icon_image="tinto.png", icon_size=(40, 40)),
            ).add_to(spain_map)

        html_data = spain_map.get_root().render()
        self.browser.setHtml(html_data)

        # --- Partie boutons ---
        button_frame = QFrame()
        button_layout = QVBoxLayout(button_frame)
        button_layout.setAlignment(Qt.AlignTop)

        for vinedo in vinedos:
            btn = QPushButton(vinedo["nom"])
            img_path = os.path.join("assets", "img", vinedo["img"])  # chemin complet
            btn.clicked.connect(
                partial(self.vinedo_selected.emit, img_path, vinedo["nom"])
            )
            button_layout.addWidget(btn)

        layout.addWidget(button_frame, stretch=1)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Charger les données
    with open("vinedos.json", encoding="utf-8") as f:
        vinedos = json.load(f)

    image_win = ImageWindow()
    main_win = MainWindow(vinedos)

    # Connexion : clic bouton → ouvrir image
    main_win.vinedo_selected.connect(image_win.show_image)

    main_win.show()
    sys.exit(app.exec())
