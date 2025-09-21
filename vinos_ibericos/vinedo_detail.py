from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt


@dataclass(frozen=True)
class ConfigUI:
    DETAIL_WIN_SIZE: tuple[int, int] = (600, 480)
    DETAIL_IMG_SIZE: tuple[int, int] = (560, 320)


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

        self.setWindowTitle(vinedo.get("nom", "Détails vignoble"))
        flags = Qt.Window | Qt.WindowStaysOnTopHint  # type: ignore
        self.setWindowFlags(flags)
        self.setFixedSize(*ConfigUI.DETAIL_WIN_SIZE)

        layout = QtWidgets.QVBoxLayout(self)

        # --- Image ---
        self.img_label = QtWidgets.QLabel()
        self.img_label.setAlignment(Qt.AlignCenter)  # type: ignore
        self.img_label.setFixedHeight(ConfigUI.DETAIL_IMG_SIZE[1])
        layout.addWidget(self.img_label)

        # --- Titre ---
        title = QtWidgets.QLabel(f"<h2>{vinedo.get('nom', '')}</h2>")
        title.setTextFormat(Qt.RichText)  # type: ignore
        layout.addWidget(title)

        # --- Description ---
        self.desc_label = QtWidgets.QTextEdit()
        self.desc_label.setReadOnly(True)
        self.desc_label.setText(vinedo.get("description", ""))
        layout.addWidget(self.desc_label)

        # --- Bouton fermer ---
        btn_close = QtWidgets.QPushButton("Fermer")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close, alignment=Qt.AlignRight)  # type: ignore

        self._load_image()

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
