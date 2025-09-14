# Connexions avec Signal

`PySide6.QtCore.Signal`

## Déclaration d'un signal

```python
nom_de_la_connexion = Signal(type1, type2, type3...)
```

Création d'un objet `Signal` qui est finalement un canal de communication. 

Exemple d'un objet signal capable de transporter deux chaînes de caractères : 

```python
vinedo_selected = Signal(str, str)
```


## Emission du signal

```python
nom_de_la_connexion.emit(*args)
```

`*args` sont les valeurs envoyées aux *slots* connectés. Ici, il s'agit d'adresser un message dans le canal de communication.

Exemple :

```python
self.vinedo_selected.emit(img_path, vinedo["nom"])
```

Ici, `img_path` et `vinedo["nom"]` (notre message) sont transmis à toutes les fonctions connectées avec `.connect()`.

Associer le clic d'un bouton à l'émission du signal :

```python
mon_bouton.clicked.connect(functools.partial(self.vinedo_selected.emit, img_path, vinedo["nom"]))
```

On utilise la méthode `partial` de `functools` afin de "créer" une nouvelle fonction : `vinedo_selected.emit(img_path, vinedo["nom"])`.


## Connexion 

```python
nom_de_la_connexion.connect(fonction_récéptrice_des_données).
```

Cela consiste à abonner une fonction au canal de communication.

Avec :

```python
main_win.vinedo_selected.connect(image_win.show_image)
```

Cela signifie qu'à chaque fois que le signal `vinedo_selected` est émis, la fonction `show_image()` sera appelée avec les arguments prévus (le message).


