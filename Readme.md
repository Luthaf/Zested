# ZestEd

ZestEd est un éditeur hors-ligne pour [Zeste de Savoir](http://zestedesavoir.com/)

Pour les fonctionnalitées, voir le fichier [News](News.md)

## Installation

### Version pré-compilées

Ces versions fournissent l'ensemble des dépendances dans un seul fichier, il n'y a besoin de rien d'autre !

Elles existent pour OsX et Windows, et sont disponibles sur la page des [releases](https://github.com/Luthaf/ZestEd/releases).

### Depuis les sources

Cette méthode fonctionne pour toutes les OS. Il faut avoir Python 3 d'installé, puis lancer la commande
```
pip3 install -e https://github.com/Luthaf/ZestEd
```

Le logiciel peut ensuite être démaré avec la commande `zested`. Si jamais le logiciel a une *erreur de segmentation* ou segfault, lancez la commande suivante avant de rapporter un bug :
```
pyside_postinstall.py -install
```

## Packaging

Voici les instructions pour créer les versions *pré-compilées*. Il faut tout d'abord installer l'intégralité des dépendances, puis suivre les instructions spécifiques.

Ces versions *pré-compilées* sont simplement des interpréteurs Python gelés avec l'ensemble des bibliothèques nécessaires.

### Windows

Le *freezing* utilise `py2exe`, qu'il faut donc installer (`pip3 install py2exe`). Ensuite, c'est aussi simple que
```
python3 setup.py py2exe
```
Les fichiers produits sont dans `dist\windows`.

### OsX

Le *freezing* utilise `py2app`, qu'il faut donc installer (`pip3 install py2app`). Ensuite, c'est aussi simple que
```
python3 setup.py py2app
```
Le bundle `.app` créé est dans `dist`.

Note: La version de PySide installée avec pip cause des segfaults lorsqu'elle est gelée. Il faut donc utiliser la version disponible avec Homebrew :
```
brew install python3 qt
brew install pyside --with-python3
```

## Contribuer au projet

Il n'y a pas encore de liste de choses à faire, mais je prends toute aide sur ce projet ! Les points principaux d'amélioration concernent l'interface (fichier `.ui` de QtDesigner) et le code bien entendu. Si vous voulez participer, envoyez-moi un MP sur ZdS pour discuter de ce qu'il faut faire, ou ouvrez une issue sur Github !

## Bugs connus

- Les liens sont cliquables, mais ne mènent à rien

