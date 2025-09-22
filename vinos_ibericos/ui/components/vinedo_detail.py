from pathlib import Path
from typing import Any, Dict, Optional

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt

from vinos_ibericos.ui.config_ui import ConfigUI
from vinos_ibericos.ui.styles.global_style import GlobalStyle


class VinedoDetailDialog(QtWidgets.QDialog):
    def __init__(
        self, parent: Optional[QtWidgets.QWidget], vinedo: Dict[str, Any], img_dir: Path
    ) -> None:
        super().__init__(parent)
        self.vinedo = vinedo
        self.img_dir = img_dir

        # Config fenêtre
        self.setWindowTitle(vinedo.get("nom", ConfigUI.DEFAULT_TITLE))
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)  # type: ignore
        self.setFixedSize(*ConfigUI.DETAIL_WIN_SIZE)

        # Layout principal
        layout = QtWidgets.QVBoxLayout(self)

        # Image
        self.img_label = QtWidgets.QLabel()
        self.img_label.setAlignment(Qt.AlignCenter)  # type: ignore
        self.img_label.setFixedHeight(ConfigUI.DETAIL_IMG_SIZE[1])

        # Titre
        title_details = QtWidgets.QLabel(
            f"<h1 style='color:{ConfigUI.COLOR_PRIMARY}; font-weight:bold;'>{vinedo.get('nom', '')}</h1>"
        )
        title_details.setTextFormat(Qt.RichText)  # type: ignore

        # Description
        self.desc_label = QtWidgets.QTextBrowser()
        self._ad_description()

        # Bouton fermer
        btn_close = QtWidgets.QPushButton("Fermer")
        btn_close.clicked.connect(self.close)

        # Ajout au layout
        layout.addWidget(self.img_label)
        layout.addWidget(title_details, alignment=Qt.AlignCenter)  # type: ignore
        layout.addWidget(self.desc_label)
        layout.addWidget(btn_close, alignment=Qt.AlignRight)  # type: ignore

        self._load_image()

    def _ad_description(self):
        self.desc_label.setReadOnly(True)
        self.desc_label.setHtml(self.vinedo.get("description", ""))
        self.desc_label.setStyleSheet(GlobalStyle.get_text_browser_style())
        self.desc_label.setOpenExternalLinks(True)

    def _load_image(self) -> None:
        img_path = self.vinedo.get("img", "")
        candidate = Path(img_path)
        if not candidate.is_absolute():
            candidate = self.img_dir / img_path
        pixmap = QtGui.QPixmap(str(candidate))
        if pixmap.isNull():
            pixmap = QtGui.QPixmap(str(self.img_dir / "default_img.jpg"))
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
