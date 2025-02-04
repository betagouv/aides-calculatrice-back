# aides-calculatrice-back

Bienvenue sur le code source du dorsal d'[aides-simplifiées](https://beta.gouv.fr/startups/droit-data-gouv-fr-simulateurs-de-droits.html). 🙂

## Pré-requis

Ce dépôt nécessite le langage [Python](https://www.python.org).  
Si vous disposez déjà de logiciels dans ce langage, nous vous conseillons l'utilisation d'un gestionnaire de versions de Python tel que [pyenv](https://github.com/pyenv/pyenv).

Les dépendances sont définies par le fichier `pyproject.toml`.  
Celui-ci peut-être utilisé avec Poetry ([documentation d'installation](https://python-poetry.org/docs/#installation)). 

### Quelle version de Python ?

Ce dépôt s'appuie sur des modèles de la législation open source. Le modèle Python appelé étant [OpenFisca](https://openfisca.org/fr), ce dépôt choisira la version de Python la plus récente supportée par la librairie [openfisca-france](https://github.com/openfisca/openfisca-france) dont il dépend.

Dans le cas de l'usage de pyenv et de poetry, exécuter les commandes suivantes pour choisir la version de Python et la transmettre à l'environnement virtuel : 

```bash
pyenv install 3.11
poetry env use python3.11
```
