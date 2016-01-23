# Zested

Zested est un éditeur hors-ligne pour [Zeste de Savoir](http://zestedesavoir.com/)

Pour les fonctionnalitées, voir le fichier [News](News.md)

## Installation

La seule manière d'installer Zested est de le compiler depuis les sources. Vous aurez
besoin d'un compilateur C++ récent, de CMake et de Qt5.

Ensuite, il faut exécuter

```bash
git clone https://github.com/Luthaf/Zested
cd Zested
mkdir build
cd build
cmake ..
make
```

## Contribuer au projet

Il n'y a pas encore de liste de choses à faire, mais je prends toute aide sur ce projet !
Les points principaux d'amélioration concernent l'interface (fichier `.ui` de QtDesigner)
et le code bien entendu. Si vous voulez participer, envoyez-moi un MP sur ZdS pour
discuter de ce qu'il faut faire, ou ouvrez une issue sur Github !

## Bugs connus

- Les liens sont cliquables, mais ne mènent à rien
