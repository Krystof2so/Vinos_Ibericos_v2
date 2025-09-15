# Ajout de marqueurs

Ajout, par exemple, d'un marqueur sur Madrid :

```python
folium.Marker(
    location=[40.4168, -3.7038],   # Coordonnées GPS
    popup="Madrid, capitale de l'Espagne",  # Texte affiché au clic
    tooltip="Cliquez pour plus d'infos",    # Texte au survol
    icon=folium.Icon(color="red", icon="info-sign")  # Icône personnalisée
).add_to(map_fol)
```

La classe **`folium.Marker`** est très flexible. Elle accepte plusieurs paramètres (avec des valeurs par défaut). Voici un **tableau récapitulatif** des principaux paramètres :

| Paramètre       | Type attendu                      | Exemple d’utilisation                             | Explication                                                         |
| --------------- | --------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------- |
| `location`      | list/tuple `[lat, lon]`           | `location=[40.4168, -3.7038]`                     | **Obligatoire**. Coordonnées GPS du marqueur (latitude, longitude). |
| `popup`         | str ou `folium.Popup`             | `popup="Madrid, capitale"`                        | Texte ou widget affiché quand on clique sur le marqueur.            |
| `tooltip`       | str ou `folium.Tooltip`           | `tooltip="Cliquez ici"`                           | Texte affiché au survol du marqueur.                                |
| `icon`          | `folium.Icon` ou `folium.DivIcon` | `icon=folium.Icon(color="red", icon="info-sign")` | Personnalisation du marqueur (couleur, symbole, etc.).              |
| `draggable`     | bool (`True`/`False`)             | `draggable=True`                                  | Rend le marqueur déplaçable par l’utilisateur.                      |
| `parse_html`    | bool (`True`/`False`)             | `popup="<b>Texte</b>" , parse_html=True`          | Permet d’interpréter le contenu du `popup` comme du HTML.           |
| `extra_classes` | str (classes CSS)                 | `extra_classes="my-marker-class"`                 | Ajoute des classes CSS personnalisées au marqueur.                  |
| `options`       | dict                              | `options={"riseOnHover": True}`                   | Passe des options supplémentaires directement à Leaflet (avancé).   |
| `**kwargs`      | divers                            | dépend du contexte                                | Tous les paramètres additionnels transmis à Leaflet.js.             |

## Les icônes

Pour les icônes, nous avons à disposition les icônes [Glyphicons](https://getbootstrap.com/docs/3.3/components/#glyphicons). Mais nous pouvons utiliser, à condition de le préfixer, les icônes de [Font Awesome](https://fontawesome.com/v4/icons/), beaucoup plus nombreux (Ex: `icon=folium.Icon(color="blue", icon="flag", prefix="fa")`). Il également possible de créer des icônes 100% **HTML/CSS** avec `folium.DivIcon` (Ex: `icon=folium.DivIcon(html='<div style="font-size:24px; color:blue;">★</div>')` - ici une étoile bleue). `folium.CustomIcon` nous permet d'utiliser une image (Ex: `icon=folium.CustomIcon(icon_image="mon_image.png", icon_size=(40, 40))`).

Concernant les couleurs, les valeurs sont les suivantes : `"red"`, `"blue"`, `"green"`, `"purple"`, `"orange"`, `"darkred"`, `"lightred"`, `"beige"`, `"darkblue"`, `"darkgreen"`, `"cadetblue"`, `"darkpurple"`, `"white"`, `"pink"`, `"lightblue"`, `"lightgreen"`, `"gray"`, `"black"`, `"lightgray"`.

Le pictogramme peut également avoir sa propre couleur : `folium.Icon(icon="star", icon_color="yellow")`.

