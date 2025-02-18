# Contribuer à aides-calculatrice-back

Merci de votre volonté de contribuer au dépôt `aides-calculatrice-back` 🙂

Afin de faciliter cette contribution et d'améliorer la qualité du code, ce fichier décrit des règles d'usage structurantes.

## Description des évolutions

Les évolutions de `aides-calculatrice-back` doivent être compréhensibles pour des utilisateurs ne disposant pas du contexte complet de l'application. 

C'est pourquoi nous faisons le choix d'un versionnement distinguant les modifications non rétro-compatibles pour les utilisateurs, des évolutions intermédiaires ou mineures. Et d'une documentation des modifications dans un CHANGELOG.

### Versionnement des évolutions

Le mode de versionnement choisi est un [versionnement sémantique](https://semver.org/lang/fr/) de l'application où l'évaluation des changements majeurs se fait au regard des évolutions de l'API web.

La version est à mettre à jour dans le fichier `pyproject.toml`.

### CHANGELOG

La documentation des évolutions quel qu'en soit la nature est à mettre à jour avant chaque merge sur la branche `main` dans un fichier `CHANGELOG.md`, rédigé en français. 

Cette documentation doit être explicite, indiquer la Pull request d'origine et dans la mesure du possible décrire les changements du point de vue de l'impact pour l'usager du dépôt.

Un chapitre ou sous-chapitre décrit l'évolution apportée par une Pull request : 
* Un chapitre de premier niveau `#` décrit une évolution de version majeure (changement non rétro-compatible), 
* `##` décrit une évolution intermédiaire (comme l'ajout d'une fonctionnalité) 
* et `###` décrit une évolution de type patch (comme une mise à jour technique sans impact métier ou nécessité de migration de code pour les usagers de l'API web).
