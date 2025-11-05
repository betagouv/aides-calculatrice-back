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

Il est alors possible de vérifier la version installée avec `poetry run python --version`.

## Installation des dépendances pour l'API web

À la racine du dépôt, exécuter :

```bash
poetry install
```

## Exécution de l'API web

Exécuter la commande suivante :

```bash
poetry run openfisca serve --country-package openfisca_france
```

L'API web est alors accessible localement sur `http://127.0.0.1:5000`.

### Tester une requête à l'API web

Conserver l'API web active dans un terminal.  
Dans un second terminal, interroger l'API web. Celle-ci dispose de [plusieurs endpoints](https://openfisca.org/doc/openfisca-web-api/endpoints.html).  
Pour tester une demande de calcul on transmettra une requête POST au format JSON à `/calculate` :

```bash
cd payloads/
curl -X POST http://127.0.0.1:5000/calculate -H 'Content-Type: application/json' -d @apl.json
```

> On peut également employer une commande supplémentaire comme [jq](https://jqlang.org) pour formater la réponse :
> `curl -X POST http://127.0.0.1:5000/calculate -H 'Content-Type: application/json' -d @apl.json | jq`

On s'attend à recevoir la réponse au format json. Pour en savoir plus sur `/calculate`, consulter sa [documentation sur openfisca.org](https://openfisca.org/doc/openfisca-web-api/input-output-data.html).

## Installation des dépendances supplémentaires pour les notebooks d'explicabilité

À la racine du dépôt, exécuter :

```bash
poetry install --with explain
```

## Exécution des notebooks en local

Pour exécuter avec Jupyter et dans un navigateur local un notebook tel que `apl_logement_ordinaire.ipynb`, exécuter la commande suivante à la racine du dépôt :

```bash
poetry run jupyter notebook ./notebooks/apl_logement_ordinaire.ipynb
```
