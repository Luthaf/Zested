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

Le gel utilise `pyinstaller`, qu'il faut installer dans sa version python 3 :
```
pip3 install https://github.com/pyinstaller/pyinstaller/archive/python3.zip
```

### Dépendances supplémentaires

#### Windows

Sous Windows, vous aurez besoin de [pywin32](sourceforge.net/projects/pywin32/files/pywin32/)
avant de pouvoir installed pyinstaller.

### OS X

La version de PySide installée avec pip cause des segfaults lorsqu'elle est gelée. Il faut
donc utiliser la version disponible avec Homebrew :
```
brew install python3 qt brew
install pyside --with-python3
```

### Création des versions gelées

Ensuite, un script est fourni à chaque fois, et il vous suffit de faire lancer la commande
`make` pour créer les versions gelées dans le dossier `dist`.

Sous OS X, `make dist` permet de créer l'ensemble des artefacts sous réserve que la
version Windows existe déjà dans `dist/Zested-Windows` (avec une machine virtuelle par
exemple).

## Contribuer au projet

Il n'y a pas encore de liste de choses à faire, mais je prends toute aide sur ce projet !
Les points principaux d'amélioration concernent l'interface (fichier `.ui` de QtDesigner)
et le code bien entendu. Si vous voulez participer, envoyez-moi un MP sur ZdS pour
discuter de ce qu'il faut faire, ou ouvrez une issue sur Github !

## Bugs connus

- Les liens sont cliquables, mais ne mènent à rien
