###############################################
# vinos_ibericos/ui/components/message_box.py #
#                                             #
# Définition des QMessageBox                  #
###############################################

from PySide6.QtWidgets import QMessageBox, QWidget


class MainBox(QMessageBox):
    def __init__(
        self,
        parent: QWidget | None = None,
        title: str = "Information",
        text: str = "",
        icon: str | None = None,
    ):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setText(text)
        self.setIcon(self._type_icon(icon))
        self.setStyleSheet(self._global_style())

    @staticmethod
    def _global_style():
        return """
            QMessageBox QLabel {
                font-size: 16pt;
            }
            QPushButton {
                font-size: 14pt;
                min-width: 100px;
                min-height: 30px;
            }
        """

    @staticmethod
    def _type_icon(icon: str | None) -> QMessageBox.Icon:
        """Retourne l’icône correspondant au type."""
        mapping = {
            "critical": QMessageBox.Critical,  # type: ignore
            "information": QMessageBox.Information,  # type: ignore
            "warning": QMessageBox.Warning,  # type: ignore
            "question": QMessageBox.Question,  # type: ignore
        }
        # Par défaut : Information
        return mapping.get(icon, QMessageBox.Information)  # type: ignore
