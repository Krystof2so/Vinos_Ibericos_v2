from dataclasses import dataclass
from typing import Optional, Tuple

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


@dataclass(frozen=True)
class Config:
    BTN_FIXED_H: int = 60
    BTN_MAX_CHARS: int = 11
    IMG_SIZE: tuple[int, int] = (380, 280)
    SCALED_PIXMAP_W: int = 0
    SCALED_PIXMAP_H: int = 1


class VinedoButton(QPushButton):
    """
    Bouton représentant un vignoble.
    - est 'checkable' (toggle)
    - applique explicitement le style quand il est togglé via toggled(bool)
    """

    # style par défaut (non coché)
    DEFAULT_STYLE: str = """
        QPushButton {
            background-color: none;
            border: 1px solid grey;
            border-radius: 6px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: #f1bfc2;
            font-weight: bold;
            color: #6b5556;
        }
    """

    # style sélectionné (coché)
    SELECTED_STYLE: str = """
        QPushButton {
            background-color: #f8d7da;
            border: 4px solid #800020;
            border-radius: 8px;
            font-weight: bold;
            color: #4a0e1f;
        }
        QPushButton:hover {
            background-color: #f1bfc2;
        }
    """

    def __init__(
        self, name: str, image_path: str, parent: Optional[QPushButton] = None
    ) -> None:
        super().__init__(
            self._split_text(name), parent
        )  # Texte potentiellement coupé sur deux lignes
        self.name: str = name
        self.image_path: str = image_path
        # Toggleable + style initial
        self.setCheckable(True)
        self.setStyleSheet(self.DEFAULT_STYLE)
        self.setFixedHeight(Config.BTN_FIXED_H)
        # Connexion au signal toggled pour appliquer le style en direct
        self.toggled.connect(self._on_toggled)

    def _split_text(self, text: str, max_chars: int = Config.BTN_MAX_CHARS) -> str:
        """Découpe le texte si trop long"""
        return (
            text
            if len(text) <= max_chars
            else f"{text[:max_chars]}\n{text[max_chars:]}"
        )

    def _on_toggled(self, checked: bool) -> None:
        """
        Slot appelé quand l'état checked change.
        On applique le style correspondant pour forcer la mise à jour visuelle.
        """
        if checked:
            self.setStyleSheet(self.SELECTED_STYLE)
        else:
            self.setStyleSheet(self.DEFAULT_STYLE)

    def get_pixmap(self, size: Tuple[int, int] = Config.IMG_SIZE) -> Optional[QPixmap]:
        """Retourne l'image du vignoble sous forme de QPixmap redimensionné"""
        pixmap: QPixmap = QPixmap(self.image_path)
        if pixmap.isNull():
            return None
        return pixmap.scaled(
            size[Config.SCALED_PIXMAP_W],  # largeur
            size[Config.SCALED_PIXMAP_H],  # hauteur
            Qt.KeepAspectRatio,  # type: ignore
            Qt.SmoothTransformation,  # type: ignore
        )
