from dataclasses import dataclass
from operator import itemgetter
from pathlib import Path
from typing import Any, Dict, List, Optional
import json

from PySide6 import QtWidgets, QtCore
from PySide6.QtWebEngineWidgets import QWebEngineView

from vinos_ibericos.map_manager import MapManager
from vinos_ibericos.vinedo_button import VinedoButton


@dataclass(frozen=True)
class Config:
    # load_datas() :
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    JSON_FILE_PATH: Path = BASE_DIR / "vinedos.json"
    JSON_DECODE_ERROR: str = "Erreur JSON:"
    NOT_FOUND_ERROR: str = f"Fichier {JSON_FILE_PATH.name} introuvable"
    # MainWindow :
    STRETCH_MAP_VIEW: int = 3
    STRETCH_RIGHT_PANEL: int = 1
    IMG_LABEL_SIZE: tuple[int, int] = (400, 300)
    FIXED_H_RESET_BTN: int = 40
    NBRE_COL_BTN: int = 4
    IMG_DIR_PATH: Path = BASE_DIR / "assets" / "img"
    # Strings :
    RESET_BUTTON: str = "Recentrer la carte sur l'Espagne"
    NOT_IMG: str = "Image introuvable"


class MainWindow(QtWidgets.QMainWindow):
    """Construction de l'interface."""

    def __init__(self, vinedos: List[Dict[str, Any]]) -> None:
        super().__init__()
        self.setWindowTitle("Vinos Ibericos")
        self.vinedos: list[Dict[str, Any]] = vinedos
        self.marker_coords: dict[str, list[float]] = {
            v["nom"]: v["coords"] for v in vinedos
        }
        self.map_manager: MapManager = MapManager(vinedos)

        # Groupement des boutons (pour une logique "un seul coché à la fois") :
        self.btn_group = QtWidgets.QButtonGroup(self)
        self.btn_group.setExclusive(True)  # Un seul bouton coché dans le groupe
        # Connexion au signal qui fournit le bouton cliqué :
        self.btn_group.buttonClicked.connect(self.on_group_button_clicked)

        #  Widget central :
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QHBoxLayout(central_widget)

        # Partie carte :
        map_view = self._setup_map_view()
        main_layout.addWidget(
            map_view, stretch=Config.STRETCH_MAP_VIEW
        )  # plus large pour la carte

        # Partie panneau droit (ajout des boutons au groupe):
        right_frame = self._setup_right_panel(vinedos)
        main_layout.addWidget(right_frame, stretch=Config.STRETCH_RIGHT_PANEL)

    def _setup_map_view(self) -> QWebEngineView:
        """Construit et initialise la vue de la carte"""
        self.browser = QWebEngineView()
        self.update_map()
        return self.browser

    def _setup_right_panel(self, vinedos: List[Dict[str, Any]]) -> QtWidgets.QFrame:
        """Construit le panneau droit avec la grille de boutons, l'image et le reset."""
        right_frame = QtWidgets.QFrame()
        right_layout = QtWidgets.QVBoxLayout(right_frame)
        # Grille pour les boutons :
        grid_buttons_layout = QtWidgets.QGridLayout()
        right_layout.addLayout(grid_buttons_layout)
        # Zone pour l'image :
        self.image_label = QtWidgets.QLabel()
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)  # type: ignore
        self.image_label.setFixedSize(*Config.IMG_LABEL_SIZE)
        right_layout.addWidget(
            self.image_label,
            alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,  # type: ignore
        )
        # Bouton pour réinitialiser la carte :
        reset_btn = QtWidgets.QPushButton(Config.RESET_BUTTON)
        reset_btn.setFixedHeight(Config.FIXED_H_RESET_BTN)
        reset_btn.clicked.connect(self.reset_interface)
        right_layout.addWidget(reset_btn)
        # Création des boutons et ajout au 'QButtonGroup' (tri alphabétique) :
        vinedos_sorted: list = sorted(vinedos, key=itemgetter("nom"))
        for i, vinedo in enumerate(vinedos_sorted):
            row: int = i // Config.NBRE_COL_BTN
            col: int = i % Config.NBRE_COL_BTN
            img_path: Path = Config.IMG_DIR_PATH / vinedo["img"]
            btn: QtWidgets.QPushButton = VinedoButton(vinedo["nom"], str(img_path))
            self.btn_group.addButton(btn)  # Ajout du bouton au groupe
            grid_buttons_layout.addWidget(btn, row, col)
        return right_frame

    def on_group_button_clicked(self, button: QtWidgets.QAbstractButton) -> None:
        """
        Slot connecté à 'QButtonGroup.buttonClicked'.
        - 'button.isChecked()' permet de savoir si le bouton est maintenant coché ou non.
        - Si décoché -> on considère la sélection annulée (on réinitialise la carte + image).
        - Si coché   -> on affiche l'image et on centre la carte sur le vignoble sélectionné.
        """
        vbtn: VinedoButton = button  # type: ignore
        if not vbtn.isChecked():  # Bouton décoché
            self.image_label.clear()
            self.update_map()  # vue globale
            return
        # bouton coché : affichage image + centrage carte
        pixmap = vbtn.get_pixmap()
        if pixmap:
            self.image_label.setPixmap(pixmap)
            self.image_label.setToolTip(vbtn.name)
        else:
            self.image_label.setText(Config.NOT_IMG)
        # Centrer la carte sur le vignoble sélectionné :
        self.update_map(vinedo_filter=vbtn.name)

    def update_map(self, vinedo_filter: Optional[str] = None) -> None:
        """Regénère la carte avec tous les marqueurs, centrée sur 'center'"""
        html_data = self.map_manager.generate_map_html(vinedo_filter=vinedo_filter)
        self.browser.setHtml(html_data)

    def reset_interface(self) -> None:
        """Réinitialise la carte, l'image et le bouton sélectionné"""
        self.update_map()  # Réinitialiser la carte
        self.image_label.clear()  # Vider l'image
        # récupère le bouton coché et le décoche (cela déclenchera toggled(False))
        checked_btn = self.btn_group.checkedButton()
        if checked_btn:
            checked_btn.setChecked(False)
            checked_btn.setStyleSheet(VinedoButton.DEFAULT_STYLE)


# --- Fonctions utilitaires ---
def load_datas() -> list[dict[str, Any]]:
    """Chargement des données depuis JSON"""
    try:
        with open(Config.JSON_FILE_PATH, encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except FileNotFoundError:
        print(Config.NOT_FOUND_ERROR)
        return []
    except json.JSONDecodeError as e:
        print(Config.JSON_DECODE_ERROR, e)
        return []


def main() -> None:
    app = QtWidgets.QApplication([])
    main_win: MainWindow = MainWindow(load_datas())
    main_win.showMaximized()  # Plein écran avec barre de titre
    app.exec()


if __name__ == "__main__":
    main()
