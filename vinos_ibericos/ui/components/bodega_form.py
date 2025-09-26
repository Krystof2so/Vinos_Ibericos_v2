from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QFrame,
    QLineEdit,
    QLabel,
    QMessageBox,
    QSpacerItem,
    QSizePolicy,
)

from vinos_ibericos.data.bodega_fields import FIELDS
from vinos_ibericos.data.bodega_manager import BodegaManager


FONT_SIZE = 16


class BodegaForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter une Bodega")

        item_space = QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)  # type: ignore
        layout_form = QFormLayout(self)  # Définition des champs : label et clé
        # Dictionnaire pour stocker les QLineEdit
        self.inputs = {}
        # Création des champs dans une boucle
        for key, label, required, typ in FIELDS:
            widget = QLineEdit()
            widget.setStyleSheet(f"font-size: {FONT_SIZE}pt;")
            label_widget = QLabel(f"{label}{' (*)' if required else ''}:")
            label_widget.setStyleSheet(f"font-size: {FONT_SIZE}pt;")
            layout_form.addRow(label_widget, widget)
            self.inputs[key] = (widget, required, typ)
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)  # type: ignore
        separator.setFrameShadow(QFrame.Sunken)  # type: ignore
        layout_form.addItem(item_space)
        layout_form.addRow(separator)
        layout_form.addItem(item_space)
        # Boutons
        buttons = QDialogButtonBox()
        btn_init = buttons.addButton("Réinitialiser", QDialogButtonBox.ResetRole)  # type: ignore
        btn_save = buttons.addButton("Sauvegarder", QDialogButtonBox.AcceptRole)  # type: ignore
        btn_cancel = buttons.addButton("Annuler", QDialogButtonBox.RejectRole)  # type: ignore
        # Connexions
        btn_init.clicked.connect(self._clear_form)
        btn_save.clicked.connect(self._on_accept)  # valide puis ferme avec accept()
        btn_cancel.clicked.connect(self.reject)  # ferme seulement le dialog
        layout_form.addRow(buttons)
        # Espace avant le label
        layout_form.addItem(item_space)
        # Label
        required_label = QLabel("(*) Champs obligatoires")
        required_label.setStyleSheet("font-size: {FONT_SIZE}pt; font-style: italic;")
        layout_form.addRow(required_label)

        self.adjustSize()
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        self_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        self_geometry.moveCenter(center_point)
        self.move(self_geometry.topLeft())

    def _clear_form(self) -> None:
        """Efface tous les champs du formulaire"""
        for widget, _, _ in self.inputs.values():
            widget.clear()

    def _validate_inputs(self) -> bool:
        """Vérifie que les champs sont valides"""
        label_text = {key: label for key, label, *_ in FIELDS}
        for key, (widget, required, expected_type) in self.inputs.items():
            value = widget.text().strip()
            label = label_text[key]
            # Vérification des champs obligatoires
            if required and not value:
                self._critical_message(label, "est obligaroire")
                return False
            # Vérification du type attendu
            if value:
                if expected_type is int:
                    try:
                        int(value)
                    except ValueError:
                        self._critical_message(
                            label, "doit contenir uniquement des chiffres"
                        )
                        return False
                elif expected_type is float:
                    try:
                        float(value)
                    except ValueError:
                        self._critical_message(
                            label, "doit contenir des chiffres décimaux"
                        )
                        return False
        return True

    def _critical_message(self, label: str, msg: str) -> None:
        QMessageBox.critical(
            self, "Erreur de validation", f"Le champ « {label} » {msg}"
        )

    def _on_accept(self) -> None:
        """Intercept OK pour valider et envoyer les données dans la db avant accept()"""
        if self._validate_inputs():
            # Envoi des données formatées à la db :
            data = self._format_dict_data()
            manager = BodegaManager()
            try:
                manager.add_bodega(data)
            except Exception as e:
                QMessageBox.critical(
                    self, "Erreur", f"Impossible d'ajouter la bodega :\n{e}"
                )

            QMessageBox.information(
                self,
                "Validation",
                f"La bodega {data['name']} a été ajoutée avec succés.",
            )
            self.accept()  # seulement si OK

    def _format_dict_data(self) -> dict:
        """Construction et formatage du dictionnaire avec les valeurs à envoyer à la db."""
        data: dict = {
            key: widget.text().strip() for key, (widget, _, _) in self.inputs.items()
        }
        title_data = ["name", "town", "street", "comp"]
        data = {
            k: v.title() if k in title_data and isinstance(v, str) else v
            for k, v in data.items()
        }
        return {k: None if v.strip() == "" else v for k, v in data.items()}
