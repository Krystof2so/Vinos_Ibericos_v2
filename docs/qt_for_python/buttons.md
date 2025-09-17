# Fonctionnement des boutons

## `QButtonGroup`

- `QButtonGroup` permet de regrouper des boutons.
- Avec `setExclusive(True)`, un seul bouton à la fois est coché dans le groupe (gestion automatique).


## Rendre `QPushButton` *checkable*

- Par défaut, un `QPushButton` ne garde pas d'état coché, cela s'active via `setCheckable(True)`.
- Cela permet à `Qt` d'utiliser le style `QPushButton: checked` en **QSS** (style dans une seule chaîne).


## Utilisation du signal

- `QButtonGroup.buttonClicked` fournit le bouton cliqué (objet `QAbstracButton`).
- Vérification si `button.isChecked()` dans le *slot* `on_group_button_clicked` (vérification si coché ou décoché).
- Coché : on charge une image dans le panneau de droite (sous les boutons) et on centre la carte sur la région viticole sélectionnée, avec ouverture d'un *popup*.
- Décoché : On efface l'image. Avec le bouton *reset* (`reset_interface()`) on boucle sur `self.btn_group_buttons()` et l'on fait `setChecked(False)` : aucune sélection et affichage de la carte globale.


## Séparation 

- `VinedoButton` contient l'UI des boutons et le style (via **QSS**).
- `MainWindow` orchestre le flux via `QButtonGroup`.

