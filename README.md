# [OpenFisca France] Moteur de calculs d'aides sociales (prime d'activité, RSA, etc...)

Ce projet permet de **conteneuriser** l'application **OpenFisca France** en utilisant Docker.

Ce projet a été conçu dans le cadre de la réalisation de l'application [Estime](https://git.beta.pole-emploi.fr/estime/estime-frontend/-/blob/master/README.md).

OpenFisca France est un moteur de calcul développé dans le language Python qui permet de faire des simulations sur le système socio-fiscal français.

- **Accéder au Github du projet** : https://github.com/openfisca/openfisca-france
- **Suivi des versions de OpenFisca France :** https://github.com/openfisca/openfisca-france/blob/master/CHANGELOG.md

# [Conteneurisation] Utilisation de Docker

- ./local : contient les fichiers de configuration pour lancer l'application en local avec Docker Compose
- ./dist : contient les fichiers de configuration pour l'environnement de recette et de production. Le conteneur est déployé sur un serveur Docker Swarm

## Installer OpenFisca en local avec Docker Compose

**Prérequis :** installer [Docker](https://docs.docker.com/engine/install/) et [Docker Compose](https://docs.docker.com/compose/install/).

1. Exécuter la commande suivante pour construire l'image :

    ```
    foo@bar:~openfisca-france$ docker build . -f ./docker-image/Dockerfile -t openfisca-france
    ```
1. Exécuter la commande suivante pour démarrer le conteneur :

    ```
    foo@bar:~openfisca-france$ docker-compose  -f ./local/docker-compose.yml up -d
    ```

#see openfisca-france python package version
pip show openfisca-france


#descriptions des versions de openfisca-france


