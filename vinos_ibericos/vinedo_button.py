from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class VinedoButton(QPushButton):
    DEFAULT_STYLE = """
        QPushButton {
            background-color: none;
            border: 1px solid grey;
            border-radius: 6px;
            padding: 6px;
        }
    """
    SELECTED_STYLE = """
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

    def __init__(self, name: str, image_path: str, parent=None):
        super().__init__(self._split_text(name), parent)
        self.name = name
        self.image_path = image_path
        self.setFixedHeight(60)
        self.setStyleSheet(self.DEFAULT_STYLE)

    def _split_text(self, text: str, max_chars: int = 11) -> str:
        """Découpe le texte si trop long"""
        return (
            text
            if len(text) <= max_chars
            else f"{text[:max_chars]}\n{text[max_chars:]}"
        )

    def select(self):
        """Met le bouton en mode sélectionné"""
        self.setStyleSheet(self.SELECTED_STYLE)

    def deselect(self):
        """Réinitialise le style du bouton"""
        self.setStyleSheet(self.DEFAULT_STYLE)

    def get_pixmap(self, size: tuple[int, int] = (380, 280)):
        """Retourne l'image du vignoble sous forme de QPixmap redimensionné"""
        pixmap = QPixmap(self.image_path)
        if pixmap.isNull():
            return None
        return pixmap.scaled(
            size[0],  # largeur
            size[1],  # hauteur
            Qt.KeepAspectRatio,  # type: ignore
            Qt.SmoothTransformation,  # type: ignore
        )
