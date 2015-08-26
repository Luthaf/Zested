# Zested

Zested est un éditeur hors-ligne pour [Zeste de Savoir](http://zestedesavoir.com/)

Pour les fonctionnalitées, voir le fichier [News](News.md)

## Installation

### Versions gelées

Le plus simple est d'utiliser les versions gelées de Zested, qui fournissent l'esemble des
dépendances en une seule fois. Ces versions sont disponibles pour OS X et pour Windows, et
sont disponibles sur la page des [*releases*](https://github.com/Luthaf/ZestEd/releases).

### Depuis les sources

Cette méthode fonctionne pour toutes les OS, et en particulier pour toutes les versions
de GNU/Linux. Il vous faut installer Python 3 et pip avec votre gestionaire de paquets,
puis utiliser la commande suivant :
```
pip3 install -e git+https://github.com/Luthaf/ZestEd#egg=zested
```

Le logiciel peut ensuite être démaré avec la commande `zested`. Si jamais le logiciel a
une *erreur de segmentation* ou segfault, lancez la commande suivante avant de rapporter
un bug :
```
pyside_postinstall.py -install
```

## Création des versions gelées

Voici les instructions pour créer les versions *gelées*. Il faut tout d'abord installer
l'intégralité des dépendances, puis suivre les instructions spécifiques.

### Windows

Le gel utilise `py2exe`, qu'il faut donc installer (`pip3 install py2exe`). Ensuite, c'est
aussi simple que
```
python3 setup.py py2exe
```
Les fichiers produits sont dans `dist\windows`.

### OsX

Le gel utilise `pyinstaller`, qu'il faut installer dans sa version python 3 :
```
pip3 install https://github.com/pyinstaller/pyinstaller/archive/python3.zip
pyinstaller Zested-OSX.spec
```
L'application est placée dans `dist`.

Note: La version de PySide installée avec pip cause des segfaults lorsqu'elle est gelée. Il faut donc utiliser la version disponible avec Homebrew :
```
brew install python3 qt
brew install pyside --with-python3
```

## Contribuer au projet

Il n'y a pas encore de liste de choses à faire, mais je prends toute aide sur ce projet !
Les points principaux d'amélioration concernent l'interface (fichier `.ui` de QtDesigner)
et le code bien entendu. Si vous voulez participer, envoyez-moi un MP sur ZdS pour
discuter de ce qu'il faut faire, ou ouvrez une issue sur Github !

## Bugs connus

- Les liens sont cliquables, mais ne mènent à rien
