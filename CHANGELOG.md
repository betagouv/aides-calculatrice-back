# CHANGELOG

### 0.0.2 [#3](https://github.com/betagouv/aides-calculatrice-back/pull/3)

* Évolutions techniques.
* Détail : 
  * Ajoute la configuration pour le déploiement sur Scalingo
    * Ajoute `.python-version` définissant la version de Python par défaut pour le Python buildpack de Scalingo
    * Ajoute la commande d'exécution de l'API web dans `Procfile` utilisant $PORT de Scalingo
    * Anticipe la création du module `aides_calculatrice_back` pour la bonne exécution du `poetry install` appelé par défaut par Scalingo

### 0.0.1 [#2](https://github.com/betagouv/aides-calculatrice-back/pull/2)

* Ajouts sans impact sur la réutilisation de l'API web.
* Détail : 
  * Ajoute des requêtes types de calcul et de debug d'`APL` (aide personnalisée au logement) dans `payloads/`
  * Ajoute un `Makefile` avec cibles d'installation et d'exécution de l'API web ainsi que des cibles de calcul d'APL
  * Initialise une documentation des modalités de contribution dans `CONTRIBUTING.md`

# 0.0.0 [#1](https://github.com/betagouv/aides-calculatrice-back/pull/1)

* Évolutions techniques et ajout de fonctionnalité
* Détail : 
  * Initialisation d'une configuration Python avec Poetry (`pyproject.toml`).
  * Initialisation de dépendances pour exécution d'une API web openfisca-france.
  * Documentation de l'installation d'un environnement Python et de l'exécution de l'API web.
