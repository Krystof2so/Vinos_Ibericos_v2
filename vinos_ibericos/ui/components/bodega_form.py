from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QFrame,
    QLineEdit,
    QLabel,
    QSpacerItem,
    QSizePolicy,
)

from vinos_ibericos.data.bodega_fields import FIELDS


class BodegaForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter une Bodega")
        self.setModal(True)  # Bloque l'accès aux autres fenêtres
        ## POSITIONNEMENT A PREVOIR ##

        item_space = QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)  # type: ignore
        layout_form = QFormLayout(self)  # Définition des champs : label et clé
        # Dictionnaire pour stocker les QLineEdit
        self.inputs = {}
        # Création des champs dans une boucle
        for key, label, required, typ in FIELDS:
            widget = QLineEdit()
            layout_form.addRow(f"{label}{' (*) ' if required else ''}:", widget)
            self.inputs[key] = (widget, required, typ)
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)  # type: ignore
        separator.setFrameShadow(QFrame.Sunken)  # type: ignore
        layout_form.addItem(item_space)
        layout_form.addRow(separator)
        layout_form.addItem(item_space)
        # Crée un QDialogButtonBox avec boutons 'Annuler' et 'Sauvegarder'
        buttons = QDialogButtonBox()
        btn_init = buttons.addButton("Réinitialiser", QDialogButtonBox.ResetRole)  # type: ignore
        btn_save = buttons.addButton("Sauvegarder", QDialogButtonBox.ActionRole)  # type: ignore
        btn_cancel = buttons.addButton("Annuler", QDialogButtonBox.ActionRole)  # type: ignore
        # Connecte les signaux aux slots du QDialog
        btn_init.clicked.connect(self._clear_form)
        btn_save.clicked.connect(self.accept)  # ferme avec Accepted
        btn_cancel.clicked.connect(self.reject)  # ferme avec Rejected
        layout_form.addRow(buttons)
        # Espace avant le label
        layout_form.addItem(item_space)
        # Label
        required_label = QLabel("(*) Champs obligatoires")
        required_label.setStyleSheet("font-style: italic;")
        layout_form.addRow(required_label)

    def _clear_form(self):
        """Efface tous les champs du formulaire"""
        for widget, _, _ in self.inputs.values():
            widget.clear()


# Utilisation :
if __name__ == "__main__":
    app = QApplication([])
    dialog = BodegaForm()
    if dialog.exec():  # exécution modale
        # Récupération des valeurs si OK
        print(dialog.inputs)
        print("Formulaire validé")
    else:
        print("Formulaire annulé")
