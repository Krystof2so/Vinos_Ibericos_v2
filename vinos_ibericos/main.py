from dataclasses import dataclass
from operator import itemgetter
from pathlib import Path
from typing import Any, Dict, List, Optional
import json

from PySide6 import QtWidgets
from PySide6.QtWebEngineWidgets import QWebEngineView

from vinos_ibericos.map_manager import MapManager
from vinos_ibericos.vinedo_button import VinedoButton
from vinos_ibericos.vinedo_detail import VinedoDetailDialog


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
        self.detail_window: Optional[VinedoDetailDialog] = None

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
        """Construit le panneau droit avec la grille des boutons et le reset."""
        right_frame = QtWidgets.QFrame()
        right_layout = QtWidgets.QVBoxLayout(right_frame)
        # Grille pour les boutons :
        grid_buttons_layout = QtWidgets.QGridLayout()
        right_layout.addLayout(grid_buttons_layout)
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
            btn: QtWidgets.QPushButton = VinedoButton(
                vinedo["nom"], str(Config.IMG_DIR_PATH / vinedo["img"])
            )
            self.btn_group.addButton(btn)  # Ajout du bouton au groupe
            grid_buttons_layout.addWidget(btn, row, col)
        return right_frame

    def on_group_button_clicked(self, button: QtWidgets.QAbstractButton) -> None:
        """
        Slot connecté à 'QButtonGroup.buttonClicked'.
        - 'button.isChecked()' permet de savoir si le bouton est maintenant coché ou non.
        - Si décoché -> on considère la sélection annulée (on réinitialise la carte).
        - Si coché   -> on centre la carte sur le vignoble sélectionné.
        """
        vbtn: VinedoButton = button  # type: ignore
        if not vbtn.isChecked():  # Bouton décoché
            self._close_detail_window()
            self.update_map()  # vue globale
            return
        self._close_detail_window()
        selected_vinedo = next((v for v in self.vinedos if v["nom"] == vbtn.name), None)
        if selected_vinedo:
            self.detail_window = VinedoDetailDialog(
                self, selected_vinedo, Config.IMG_DIR_PATH
            )
            parent_geo = self.geometry()
            dw, dh = self.detail_window.width(), self.detail_window.height()
            x = parent_geo.x() + (parent_geo.width() - dw) // 2
            y = parent_geo.y() + (parent_geo.height() - dh) // 8
            self.detail_window.move(max(0, x), max(0, y))
            self.detail_window.show()
        self.update_map(vinedo_filter=vbtn.name)

    def update_map(self, vinedo_filter: Optional[str] = None) -> None:
        """Regénère la carte avec tous les marqueurs, centrée sur 'center'"""
        html_data = self.map_manager.generate_map_html(vinedo_filter=vinedo_filter)
        self.browser.setHtml(html_data)

    def reset_interface(self) -> None:
        """Réinitialise la carte et le bouton sélectionné"""
        self.update_map()  # Réinitialiser la carte
        self._close_detail_window()
        # récupère le bouton coché et le décoche (cela déclenchera toggled(False))
        checked_btn = self.btn_group.checkedButton()
        if checked_btn:
            checked_btn.setChecked(False)
            checked_btn.setStyleSheet(VinedoButton.DEFAULT_STYLE)

    def _close_detail_window(self) -> None:
        """Ferme la fenêtre de détail si elle est ouverte."""
        if self.detail_window:
            self.detail_window.close()
            self.detail_window = None


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
