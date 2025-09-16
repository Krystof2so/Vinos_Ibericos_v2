from dataclasses import dataclass
from functools import partial
from operator import itemgetter
from pathlib import Path
import json
import os

from PySide6 import QtWidgets, QtCore
from PySide6.QtWebEngineWidgets import QWebEngineView

from vinos_ibericos.map_manager import MapManager
from vinos_ibericos.vinedo_button import VinedoButton


@dataclass(frozen=True)
class Config:
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    JSON_FILE_PATH: Path = BASE_DIR / "vinedos.json"
    JSON_FILE: str = JSON_FILE_PATH.name
    JSON_DECODE_ERROR: str = "Erreur JSON:"
    NOT_FOUND_ERROR: str = f"Fichier {JSON_FILE} introuvable"


# --- Fenêtre principale ---
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, vinedos):
        super().__init__()
        self.setWindowTitle("Vinos Ibericos")
        self.selected_button = None  # bouton actuellement sélectionné
        self.vinedos = vinedos
        self.marker_coords = {v["nom"]: v["coords"] for v in vinedos}
        self.map_manager = MapManager(vinedos)

        # --- Widget central ---
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QHBoxLayout(central_widget)

        # --- Partie carte ---
        self.browser = QWebEngineView()
        main_layout.addWidget(self.browser, stretch=3)  # plus large pour la carte
        self.update_map()  # Affiche la carte initiale

        # --- Partie boutons + cadre image ---
        right_frame = QtWidgets.QFrame()
        right_layout = QtWidgets.QVBoxLayout(right_frame)

        # Grille pour les boutons
        grid_buttons_layout = QtWidgets.QGridLayout()
        right_layout.addLayout(grid_buttons_layout)

        # Zone pour l'image (label en bas)
        self.image_label = QtWidgets.QLabel()
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)  # type: ignore
        self.image_label.setFixedSize(400, 300)
        right_layout.addWidget(
            self.image_label,
            alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,  # type: ignore
        )

        # Bouton Réinitialiser la carte
        reset_btn = QtWidgets.QPushButton("Recentrer la carte sur l'Espagne")
        reset_btn.setFixedHeight(40)
        reset_btn.clicked.connect(self.reset_interface)
        right_layout.addWidget(reset_btn)

        # Ajout des boutons dans la grille (tri alphabétique)
        vinedos_sorted = sorted(vinedos, key=itemgetter("nom"))
        cols = 4  # nombre de colonnes
        for i, vinedo in enumerate(vinedos_sorted):
            row = i // cols
            col = i % cols
            img_path = os.path.join("assets", "img", vinedo["img"])
            btn = VinedoButton(vinedo["nom"], img_path)
            btn.clicked.connect(partial(self.on_button_clicked, btn))
            grid_buttons_layout.addWidget(btn, row, col)

        main_layout.addWidget(right_frame, stretch=1)

    # --- Méthodes auxiliaires ---
    def on_button_clicked(self, btn):
        """Gère la sélection du bouton et l'affichage de l'image"""
        # Désélectionner le bouton précédent
        if self.selected_button:
            self.selected_button.deselect()

        # Sélectionner le bouton cliqué
        btn.select()
        self.selected_button = btn

        # Afficher l’image
        pixmap = btn.get_pixmap()
        if pixmap:
            self.image_label.setPixmap(pixmap)
            self.image_label.setToolTip(btn.name)
        else:
            self.image_label.setText("Image introuvable")

        # Centrer la carte sur ce vignoble
        self.update_map(vinedo_filter=btn.name)

    def update_map(self, vinedo_filter=None):
        """Regénère la carte avec tous les marqueurs, centrée sur 'center'"""
        html_data = self.map_manager.generate_map_html(vinedo_filter=vinedo_filter)
        self.browser.setHtml(html_data)

    def reset_interface(self):
        """Réinitialise la carte, l'image et le bouton sélectionné"""
        self.update_map()  # Réinitialiser la carte
        self.image_label.clear()  # Vider l'image
        # Réinitialiser le bouton sélectionné
        if self.selected_button:
            self.selected_button.deselect()
            self.selected_button = None


# --- Fonctions utilitaires ---
def load_datas() -> dict:
    """Chargement des données depuis JSON"""
    try:
        with open(Config.JSON_FILE, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(Config.NOT_FOUND_ERROR)
        return {}
    except json.JSONDecodeError as e:
        print(Config.JSON_DECODE_ERROR, e)
        return {}


def main() -> None:
    app = QtWidgets.QApplication([])
    main_win = MainWindow(load_datas())
    main_win.showMaximized()  # Plein écran avec barre de titre
    app.exec()


if __name__ == "__main__":
    main()
