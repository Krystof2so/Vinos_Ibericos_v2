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

from .map_manager import MapManager


# --- Fenêtre principale ---
class MainWindow(QMainWindow):
    def __init__(self, vinedos):
        super().__init__()
        self.setWindowTitle("Vinos Ibericos")
        self.selected_button = None  # bouton actuellement sélectionné
        self.vinedos = vinedos
        self.marker_coords = {v["nom"]: v["coords"] for v in vinedos}
        self.map_manager = MapManager(vinedos)

        # --- Widget central ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # --- Partie carte (QWebEngineView) ---
        self.browser = QWebEngineView()
        main_layout.addWidget(self.browser, stretch=3)  # plus large pour la carte
        self.update_map()  # Affiche la carte initiale

        # --- Partie boutons + cadre image ---
        right_frame = QFrame()
        right_layout = QVBoxLayout(right_frame)

        # Grille pour les boutons
        grid_buttons_layout = QGridLayout()
        right_layout.addLayout(grid_buttons_layout)

        # Zone pour l'image (label en bas)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)  # type: ignore
        self.image_label.setFixedSize(400, 300)
        right_layout.addWidget(
            self.image_label,
            alignment=Qt.AlignHCenter | Qt.AlignVCenter,  # type: ignore
        )

        # Bouton Réinitialiser la carte
        reset_btn = QPushButton("Recentrer la carte sur l'Espagne")
        reset_btn.setFixedHeight(40)
        reset_btn.clicked.connect(self.reset_interface)
        right_layout.addWidget(reset_btn)

        # Ajout des boutons dans la grille (tri alphabétique)
        vinedos_sorted = sorted(vinedos, key=itemgetter("nom"))
        cols, btn_height = 4, 60  # nombre de colonnes
        for i, vinedo in enumerate(vinedos_sorted):
            row = i // cols
            col = i % cols
            btn = QPushButton(self.split_text(vinedo["nom"], max_chars=11))
            btn.setFixedHeight(btn_height)
            img_path = os.path.join("assets", "img", vinedo["img"])
            btn.clicked.connect(
                partial(self.on_button_clicked, btn, img_path, vinedo["nom"])
            )
            grid_buttons_layout.addWidget(btn, row, col)

        main_layout.addWidget(right_frame, stretch=1)

    # --- Méthodes auxiliaires ---
    def split_text(self, text, max_chars):
        """Découpe le texte sur deux lignes si trop long"""
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n" + text[max_chars:]

    def on_button_clicked(self, btn, image_path, title):
        """Gère la sélection du bouton et l'affichage de l'image"""
        # Réinitialiser l’ancien bouton
        if self.selected_button is not None:
            self.selected_button.setStyleSheet("")  # style par défaut
        # Appliquer le style lie-de-vin au bouton cliqué
        btn.setStyleSheet(
            """
                QPushButton {
                    background-color: #f8d7da;       /* fond rose clair */
                    border: 4px solid #800020;       /* bordure lie-de-vin */
                    border-radius: 8px;              /* coins arrondis */
                    padding: 6px;
                    font-weight: bold;               /* texte en gras */
                    color: #4a0e1f;                  /* prune foncé pour le texte */
                }
                QPushButton:hover {
                    background-color: #f1bfc2;       /* rose un peu plus vif au survol */
                }
            """
        )
        self.selected_button = btn
        # Afficher l’image
        self.show_image(image_path, title)
        # Carte : regénérer centrée sur le vignoble
        coords = self.marker_coords[title]
        self.update_map(center=coords)

    def update_map(self, center=None):
        """Regénère la carte avec tous les marqueurs, centrée sur 'center'"""
        html_data = self.map_manager.generate_map_html(center=center)
        self.browser.setHtml(html_data)

    def show_image(self, image_path, title):
        """Affiche l'image sous les boutons"""
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(380, 280, Qt.KeepAspectRatio))  # type: ignore
            self.image_label.setToolTip(title)
        else:
            self.image_label.setText("Image introuvable")

    def reset_interface(self):
        """Réinitialise la carte, l'image et le bouton sélectionné"""
        self.update_map()
        self.image_label.setPixmap(QPixmap())
        if self.selected_button:
            self.selected_button.setStyleSheet("")
            self.selected_button = None


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
