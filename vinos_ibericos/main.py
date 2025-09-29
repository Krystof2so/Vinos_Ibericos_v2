from dataclasses import dataclass
from operator import itemgetter
from pathlib import Path
from typing import List, Optional

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWebEngineWidgets import QWebEngineView

from vinos_ibericos.ui.styles.global_style import GlobalStyle
from vinos_ibericos.map_manager import MapManager
from vinos_ibericos.ui.components.vinedo_detail import VinedoDetailDialog
from vinos_ibericos.utils import CheckVinedoJson, VinedoJsonError, suspend_signals
from vinos_ibericos.datatypes import Vinedo
from vinos_ibericos.config.strings import ErrorMsg
from vinos_ibericos.ui.components.message_box import MainBox


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
    NBRE_COL_BTN: int = 5
    IMG_DIR_PATH: Path = BASE_DIR / "assets" / "img"
    DEFAULT_IMG: Path = BASE_DIR / "assets"
    # Strings :
    RESET_BUTTON: str = "Recentrer la carte sur l'Espagne"
    NOT_IMG: str = "Image introuvable"


class MainWindow(QtWidgets.QMainWindow):
    """Construction de l'interface."""

    def __init__(self, vinedos: List[Vinedo]) -> None:
        super().__init__()
        self.setWindowTitle("Vinos Ibericos")
        self.vinedos: list[Vinedo] = vinedos
        self.marker_coords: dict[str, list[float]] = {
            v["nom"]: v["coords"] for v in vinedos
        }
        self.map_manager: MapManager = MapManager(vinedos)
        self.detail_window: Optional[VinedoDetailDialog] = None
        #  Widget central :
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QHBoxLayout(central_widget)
        # Partie carte :
        self.map_frame = self._setup_map_view()
        main_layout.addWidget(
            self.map_frame, stretch=Config.STRETCH_MAP_VIEW
        )  # plus large pour la carte
        # Partie panneau droit (ajout des boutons au groupe):
        right_frame = self._setup_right_panel(vinedos)
        main_layout.addWidget(right_frame, stretch=Config.STRETCH_RIGHT_PANEL)

    def _setup_map_view(self) -> QtWidgets.QFrame:
        """Construit et initialise la vue de la carte"""
        frame = QtWidgets.QFrame()
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)  # Pas de marges internes
        self.map_view = QWebEngineView()
        self.update_map()
        layout.addWidget(self.map_view)
        frame.setStyleSheet(GlobalStyle.widget_border())
        return frame

    def _setup_right_panel(self, vinedos: List[Vinedo]) -> QtWidgets.QFrame:
        """Construit le panneau droit avec une QListWidget triée (scrollable) et le reset."""
        right_frame = QtWidgets.QFrame()
        grid = QtWidgets.QGridLayout(right_frame)
        grid.setContentsMargins(5, 5, 5, 5)
        grid.setSpacing(5)
        # Label :
        title_label = QtWidgets.QLabel("Choisir un vignoble\ndans la liste suivante :")
        title_label.setStyleSheet("font-size: 18pt;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)  # type: ignore
        grid.addWidget(title_label, 0, 1, 1, 2)
        # Création de la QListWidget
        self.list_widget = self._create_list_widget(vinedos)
        grid.addWidget(self.list_widget, 1, 1, 4, 2)
        # Label pour afficher une image :
        self.image_label = QtWidgets.QLabel()
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)  # type: ignore
        default_image_path = Config.DEFAULT_IMG / "copa_vino.jpg"
        pixmap = QtGui.QPixmap(str(default_image_path))
        self.image_label.setPixmap(
            pixmap.scaled(
                400,
                300,  # taille fixe pour l'affichage initial
                QtCore.Qt.KeepAspectRatio,  # type: ignore
                QtCore.Qt.SmoothTransformation,  # type: ignore
            )
        )
        grid.addWidget(self.image_label, 5, 1, 4, 2)
        # Bouton pour réinitialiser la carte :
        reset_btn = QtWidgets.QPushButton(Config.RESET_BUTTON)
        reset_btn.setFixedHeight(Config.FIXED_H_RESET_BTN)
        reset_btn.clicked.connect(self.reset_interface)
        grid.addWidget(reset_btn, 9, 0, 1, 4)
        return right_frame

    def _create_list_widget(self, vinedos: List[Vinedo]) -> QtWidgets.QListWidget:
        """Construit la QListWidget des vignobles avec tri, stockage d'objet et style."""
        list_widget = QtWidgets.QListWidget()
        list_widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)  # type: ignore
        list_widget.setStyleSheet(GlobalStyle.get_list_widget_style())
        # Tri alphabétique et ajout des items
        vinedos_sorted = sorted(vinedos, key=itemgetter("nom"))
        for vinedo in vinedos_sorted:
            item = QtWidgets.QListWidgetItem(vinedo["nom"])
            item.setData(QtCore.Qt.UserRole, vinedo)  # type: ignore
            list_widget.addItem(item)
        # Limiter la taille visible à 10 lignes
        num_visible = 8
        if list_widget.count() > 0:
            row_height = list_widget.sizeHintForRow(0)
            frame_height = row_height * num_visible + 2 * list_widget.frameWidth()
            list_widget.setFixedHeight(frame_height)
        # Connexion du signal
        list_widget.itemSelectionChanged.connect(self.on_list_item_selected)
        return list_widget

    def on_list_item_selected(self) -> None:
        """Slot appelé quand la sélection dans la QListWidget change."""
        current = self.list_widget.currentItem()
        if current is None:  # Pas d'item sélectionné -> vue globale
            self._close_detail_window()
            self.update_map()
            return
        # Récupère le dictionnaire associé au vignoble :
        selected_vinedo = current.data(QtCore.Qt.UserRole)  # type: ignore
        self._close_detail_window()
        self._display_detail_window(selected_vinedo)
        # Mettre à jour la carte en filtrant sur le vignoble sélectionné
        self.update_map(vinedo_filter=selected_vinedo["nom"])

    def update_map(self, vinedo_filter: Optional[str] = None) -> None:
        """Regénère la carte avec tous les marqueurs, centrée sur 'center'"""
        html_data = self.map_manager.generate_map_html(vinedo_filter=vinedo_filter)
        self.map_view.setHtml(html_data)

    def reset_interface(self) -> None:
        """
        Réinitialise la carte et la sélection dans la QListWidget,
        et retire le focus clavier pour éviter toute sélection involontaire.
        """
        self._close_detail_window()
        # Vider la sélection de la QListWidget et bloquer temporairement les signaux :
        if hasattr(self, "list_widget") and self.list_widget is not None:
            with suspend_signals(self.list_widget):
                self.list_widget.clearSelection()
            self.list_widget.clearFocus()  # Retirer le focus clavier
        self.update_map()  # Réinitialiser la carte

    def _display_detail_window(self, vinedo: dict) -> None:
        """
        Positionnent et affichage de la fenêtre de détail d'un vignoble.
        - Positionnement : centrée sur la partie gauche de la carte.
        - Définition de sa taille (cf. 'VinedoDetailDialog').
        - La déplacer aux coordonnées voulues et l'afficher.
        """
        # Positionnement et affichage de la fenêtre de détail :
        self.detail_window = VinedoDetailDialog(self, vinedo, Config.IMG_DIR_PATH)
        # Récupérer la position globale du widget de la carte :
        map_top_left = self.map_view.mapToGlobal(self.map_view.rect().topLeft())
        mw, mh = self.map_view.width(), self.map_view.height()
        # Taille de la fenêtre de détail :
        dw, dh = self.detail_window.width(), self.detail_window.height()
        # Positionnent :
        x = map_top_left.x() + (mw // 2 - dw) // 2  # Centre gauche
        y = map_top_left.y() + (mh - dh) // 2  # Centre
        # Déplacer et afficher :
        self.detail_window.move(max(0, x), max(0, y))
        self.detail_window.show()

    def _close_detail_window(self) -> None:
        """Ferme la fenêtre de détail si elle est ouverte."""
        if self.detail_window:
            self.detail_window.close()
            self.detail_window = None


def main() -> None:
    app = QtWidgets.QApplication([])
    app.setStyleSheet(
        GlobalStyle.get_base_style()
    )  # Application du style global à toute l'UI
    loader_json_file: CheckVinedoJson = CheckVinedoJson()
    try:
        loader_json_file.load()  # Charge et valide les données
    except VinedoJsonError:
        msg_box = MainBox(
            text=ErrorMsg.MSG_ERROR_JSON_VINEDO,
            title=ErrorMsg.JSON_ERROR,
            icon="critical",
        )
        msg_box.exec()
        return  # Arrêt du lancement de l'application
    main_win: MainWindow = MainWindow(
        loader_json_file.data
    )  # Accès direct aux données via 'data'
    main_win.showMaximized()  # Plein écran avec barre de titre
    app.exec()


if __name__ == "__main__":
    main()
