# Vinos Ibéricos

(projet en construction, avec diverses idées, mais pour l'heure je continue mon exploration de [folium](https://python-visualization.github.io/folium/latest/index.html))

![Capture d'écran](assets/img/capture.png)

## 🇪🇸 Description

**Vinos Ibéricos** est une application Python interactive qui permet de découvrir les vignobles espagnols.  
L’utilisateur peut :

- Visualiser la carte de l’Espagne avec tous les vignobles indiqués.
- Cliquer sur un vignoble pour afficher une image et des informations détaillées.
- Recentrer la carte sur l’Espagne via un bouton de réinitialisation.

L’interface est construite avec [PySide6](https://doc.qt.io/qtforpython-6/index.html) pour la partie graphique et [Folium](https://python-visualization.github.io/folium/latest/index.html) pour la carte interactive.

---

## 🍷Fonctionnalités

1. **Carte interactive**  
   - Vue globale de l’Espagne avec tous les vignobles.
   - Vue détaillée sur un vignoble avec popup et image.

2. **Boutons dynamiques**  
   - Chaque vignoble est représenté par un bouton.
   - Un bouton sélectionné met à jour la carte et affiche l’image correspondante.
   - Bouton “Recentrer sur l’Espagne” pour réinitialiser la sélection.

3. **Gestion des images**  
   - Images des vignobles affichées dans l’interface.
   - Image par défaut si aucune image n’est disponible.

4. **Structure modulaire**  
   - Fichiers séparés pour la configuration, les boutons et la gestion de la carte.
   - Feuilles de style et constantes centralisées.

---

## 🍇 Description

**Vinos Ibéricos** est une application Python interactive qui permet de découvrir les vignobles espagnols.  
L’utilisateur peut :

- Visualiser la carte de l’Espagne avec tous les vignobles indiqués.
- Cliquer sur un vignoble pour afficher une image et des informations détaillées.
- Recentrer la carte sur l’Espagne via un bouton de réinitialisation.

L’interface est construite avec **PySide6** pour la partie graphique et **Folium** pour la carte interactive.

---

## 🇪🇸 Fonctionnalités

1. **Carte interactive**  
   - Vue globale de l’Espagne avec tous les vignobles.
   - Vue détaillée sur un vignoble avec popup et image.

2. **Boutons dynamiques**  
   - Chaque vignoble est représenté par un bouton.
   - Un bouton sélectionné met à jour la carte et affiche l’image correspondante.
   - Bouton “Recentrer sur l’Espagne” pour réinitialiser la sélection.

3. **Gestion des images**  
   - Images des vignobles affichées dans l’interface.
   - Image par défaut si aucune image n’est disponible.

4. **Structure modulaire**  
   - Fichiers séparés pour la configuration, les boutons et la gestion de la carte.
   - Feuilles de style et constantes centralisées.

---

## 🍷 Prérequis

- Python 3.11+ recommandé
- Packages Python :

```bash
pip install PySide6 folium
```

**WebEngine** pour l’affichage de la carte interactive (installé avec PySide6).

---

## 🍇 Installation

1. Cloner le dépôt :
 
```bash
git clone https://github.com/votre-utilisateur/vinos-ibericos.git
cd vinos-ibericos
```

2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

3. Lancer l’application :

```bash
python -m vinos_ibericos.main
```

--- 

## 🇪🇸 Structure du projet

```text
.
├── assets
│   ├── img/              # Images des vignobles et image par défaut
│   └── tinto.png         # Icône de marqueur sur la carte
├── vinos_ibericos
│   ├── main.py           # Point d’entrée de l’application
│   ├── map_manager.py    # Gestion de la carte et des marqueurs
│   └── vinedo_button.py  # Classe de bouton représentant un vignoble
├── vinedos.json          # Données des vignobles
└── README.md 
```

--- 

## 🍷Utilisation (avec modération...😃)

1. Afficher la carte
Au lancement, la carte de l’Espagne s’affiche avec tous les vignobles.

2. Sélectionner un vignoble
Cliquer sur un bouton dans le panneau droit :
- Affiche l’image du vignoble.
- Centre la carte sur le vignoble.
- Affiche un popup avec la description.

3. Réinitialiser la carte
Cliquer sur le bouton “Recentrer la carte sur l’Espagne” :
- Supprime la sélection.
- Recentrage sur la carte globale.
- Efface l’image affichée.

--- 

## 🍇 Personnalisation

- Ajouter un vignoble :
  1. Ajouter un objet dans `vinedos.json` avec `nom`, `coords`, `description`, `img`.
  2. Ajouter l’image correspondante dans  ̀assets/img`.

- Modifier l’apparence des boutons :
  - Modifier les constantes et les styles dans `vinedo_button.py`.

- Modifier l’apparence de la carte :
  - Modifier `map_manager.py` (popup, icônes, zoom).


