from functools import partial
import json
from operator import itemgetter
import os
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import folium


# --- Fenêtre principale ---
class MainWindow(QMainWindow):
    def __init__(self, vinedos):
        super().__init__()
        self.setWindowTitle("Vinos Ibericos")

        # --- Widget central ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # --- Partie carte (QWebEngineView) ---
        self.browser = QWebEngineView()
        main_layout.addWidget(self.browser, stretch=3)  # plus large pour la carte

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

        # --- Partie boutons + cadre image ---
        right_frame = QFrame()
        right_layout = QVBoxLayout(right_frame)

        # Grille pour les boutons
        grid_buttons_layout = QGridLayout()
        right_layout.addLayout(grid_buttons_layout)

        # Zone pour l'image (label en bas)
        self.image_label = QLabel("Aucune image sélectionnée")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(400, 300)
        right_layout.addWidget(
            self.image_label, alignment=Qt.AlignHCenter | Qt.AlignVCenter
        )

        # Ajout des boutons dans la grille (tri alphabétique)
        vinedos_sorted = sorted(vinedos, key=itemgetter("nom"))
        cols, btn_height = 3, 50  # nombre de colonnes
        for i, vinedo in enumerate(vinedos_sorted):
            row = i // cols
            col = i % cols
            btn = QPushButton(self.split_text(vinedo["nom"], max_chars=10))
            btn.setFixedHeight(btn_height)
            img_path = os.path.join("assets", "img", vinedo["img"])
            btn.clicked.connect(partial(self.show_image, img_path, vinedo["nom"]))
            grid_buttons_layout.addWidget(btn, row, col)

        main_layout.addWidget(right_frame, stretch=1)

    # --- Méthodes auxiliaires ---
    def split_text(self, text, max_chars=10):
        """Découpe le texte sur deux lignes si trop long"""
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n" + text[max_chars:]

    def show_image(self, image_path, title):
        """Affiche l'image sous les boutons"""
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(380, 280, Qt.KeepAspectRatio))
            self.image_label.setToolTip(title)
        else:
            self.image_label.setText("Image introuvable")


# --- Fonctions utilitaires ---
def load_datas() -> dict:
    """Chargement des données depuis JSON"""
    with open("vinedos.json", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    app = QApplication([])
    main_win = MainWindow(load_datas())
    main_win.showMaximized()  # Plein écran avec barre de titre
    app.exec()


if __name__ == "__main__":
    main()
