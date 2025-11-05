# CHANGELOG

# 1.0.0 [#7](https://github.com/betagouv/aides-calculatrice-back/pull/7)

* Évolution technique pouvant impacter la réutilisation.
* Détail :
  * Met à jour `openfisca-france` de v`^170.1.12` à `^174.2.8`
    * Obtient ainsi les revalorisations d'APL d'octobre 2025
    * Inclut une réorganisation des paramètres d'APL (mais notebooks pas encore mis à jour)
    * Met à jour `openfisca-core` à la même version que celle employée par `openfisca-france`
  * Met à jour les payloads d'exemple de calcul d'APL et ajoute les payloads de résultat pour illustrer la mise à jour
  * Documente dans le `README` un envoi de requête à l'API web openfisca-france

### 0.0.4 [#5](https://github.com/betagouv/aides-calculatrice-back/pull/5)

* Ajouts sans impact sur la réutilisation de l'API web.
* Détail :
  * Met à jour `openfisca-france` de sa version `^169.15.0` vers `^170.1.12`
  * Ajoute un notebook d'explication de l'`APL` en logement ordinaire `notebooks/apl_logement_ordinaire.ipynb`, part spécifique de `notebooks/apl.ipynb`
  * Expérimente l'emploi d'`ipywidgets` dans `notebooks/apl_logement_ordinaire_interactif.ipynb`
  * Initialise un notebook d'explication de la `garantie visale`
  * Ajoute un exemple de requête de Garantie visale `payloads/visale.json`
  * Documente dans le `README` l'usage des notebooks d'explicabilité
  

### 0.0.3 [#4](https://github.com/betagouv/aides-calculatrice-back/pull/4)

* Évolution technique.
* Détail :
  * Allonge la durée de timeout par défaut à l'exécution par `Procfile`
  * Permet de limiter le risque d'erreur `504` en passant de 60s. à 120s. de temps alloué

### 0.0.2 [#3](https://github.com/betagouv/aides-calculatrice-back/pull/3)

* Évolutions techniques.
* Détail : 
  * Ajoute la configuration pour le déploiement sur Scalingo
    * Ajoute `.python-version` définissant la version de Python par défaut pour le Python buildpack de Scalingo
    * Ajoute la commande d'exécution de l'API web dans `Procfile` utilisant `$PORT` de Scalingo
    * Anticipe la création du module `aides_calculatrice_back` pour la bonne exécution du `poetry install` appelé par défaut par Scalingo

### 0.0.1 [#2](https://github.com/betagouv/aides-calculatrice-back/pull/2)

* Ajouts sans impact sur la réutilisation de l'API web.
* Détail : 
  * Ajoute des requêtes types de calcul et de debug d'`APL` (aide personnalisée au logement) dans `payloads/`
  * Ajoute un `Makefile` avec cibles d'installation et d'exécution de l'API web ainsi que des cibles de calcul d'APL
  * Initialise une documentation des modalités de contribution dans `CONTRIBUTING.md`

# 0.0.0 [#1](https://github.com/betagouv/aides-calculatrice-back/pull/1)

* Évolutions techniques et ajout de fonctionnalité.
* Détail : 
  * Initialisation d'une configuration Python avec Poetry (`pyproject.toml`).
  * Initialisation de dépendances pour exécution d'une API web openfisca-france.
  * Documentation de l'installation d'un environnement Python et de l'exécution de l'API web.
