from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt


@dataclass(frozen=True)
class ConfigUI:
    DEFAULT_TITLE: str = "Détails vignoble"
    DETAIL_WIN_SIZE: tuple[int, int] = (650, 680)
    DETAIL_IMG_SIZE: tuple[int, int] = (600, 320)


class VinedoDetailDialog(QtWidgets.QDialog):
    """
    Fenêtre séparée affichant l'image et la description d'un vignoble.
    - Non modale (se superpose à la fenêtre principale).
    - Reste au-dessus de la fenêtre principale (WindowStaysOnTopHint).
    """

    def __init__(
        self, parent: Optional[QtWidgets.QWidget], vinedo: Dict[str, Any], img_dir: Path
    ) -> None:
        super().__init__(parent)
        self.vinedo = vinedo
        self.img_dir = img_dir
        self.setWindowTitle(vinedo.get("nom", ConfigUI.DEFAULT_TITLE))
        flags = Qt.Window | Qt.WindowStaysOnTopHint  # type: ignore
        self.setWindowFlags(flags)
        self.setFixedSize(*ConfigUI.DETAIL_WIN_SIZE)
        # Widget principale de la fenêtre de détail :
        layout = QtWidgets.QVBoxLayout(self)
        # Image (widget 'QLabel'):
        self.img_label = QtWidgets.QLabel()
        self.img_label.setAlignment(Qt.AlignCenter)  # type: ignore
        self.img_label.setFixedHeight(ConfigUI.DETAIL_IMG_SIZE[1])
        # Titre (widget 'QLabel'):
        title_details = QtWidgets.QLabel(
            f"<h1 style='color:#d08770;'><b>{vinedo.get('nom', '')}<\b>"
        )
        title_details.setTextFormat(Qt.RichText)  # type: ignore
        # Description (widget 'QTextBrowser'):
        self.desc_label = QtWidgets.QTextBrowser()
        self._ad_description()
        # Bouton fermer (widget 'QPushButton'):
        btn_close = QtWidgets.QPushButton("Fermer")
        btn_close.clicked.connect(self.close)
        # Ajout des widgets à la fenêtre :
        layout.addWidget(self.img_label)
        layout.addWidget(title_details, alignment=Qt.AlignCenter)  # type: ignore
        layout.addWidget(self.desc_label)
        layout.addWidget(btn_close, alignment=Qt.AlignRight)  # type: ignore
        self._load_image()

    def _ad_description(self):
        """Insertion de la description (format HTML)."""
        self.desc_label.setReadOnly(True)
        self.desc_label.setHtml(self.vinedo.get("description", ""))
        # Couleur du texte et style du widget :
        self.desc_label.setStyleSheet("""
            QTextBrowser {
                color: #88c0d0;             /* couleur du texte */
                border: 1px solid #8fbcbb;  /* liseré */
                border-radius: 6px;         /* angles arrondis */
                padding: 8px;
            }
            /* QScrollBar du QTextBrowser (fond + largeur) */
            QTextBrowser QScrollBar:vertical {
                background: #4f5664;   /* fond de la zone scrollbar */
                width: 8px;
                margin: 0px 0px 0px 0px;
                border-radius: 6px;
            }
            /* Curseur du curseur de la QScrollBar */
            QScrollBar::handle:vertical {background: #d08770;}
            /* Curseur hover */
            QScrollBar::handle:vertical:hover {background: #d09b80;}
            /* Suppression des flèches haut/bas (optionnel) */
            QTextBrowser QScrollBar::add-line:vertical,
            QTextBrowser QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
            }
        """)
        self.desc_label.setOpenExternalLinks(
            True
        )  # Active l'ouverture des liens dans le navigateur externe

    def _load_image(self) -> None:
        img_path = self.vinedo.get("img", "")
        candidate = Path(img_path)
        if not candidate.is_absolute():
            candidate = self.img_dir / img_path
        pixmap = QtGui.QPixmap(str(candidate))
        if pixmap.isNull():
            default = self.img_dir / "default_img.jpg"
            pixmap = QtGui.QPixmap(str(default))
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                ConfigUI.DETAIL_IMG_SIZE[0],
                ConfigUI.DETAIL_IMG_SIZE[1],
                Qt.KeepAspectRatio,  # type: ignore
                Qt.SmoothTransformation,  # type: ignore
            )
            self.img_label.setPixmap(scaled)
        else:
            self.img_label.setText("Image introuvable")
