# [OpenFisca France] Moteur de calculs d'aides sociales (prime d'activité, RSA, etc...)

Ce projet permet de **conteneuriser** l'application **OpenFisca France** en utilisant Docker.

Ce projet a été conçu dans le cadre de la réalisation de l'application [Estime](https://git.beta.pole-emploi.fr/estime/estime-frontend/-/blob/master/README.md).

OpenFisca France est un moteur de calcul développé dans le language Python qui permet de faire des simulations sur le système socio-fiscal français.

- **Accéder au Github du projet** : https://github.com/openfisca/openfisca-france
- **Suivi des versions de OpenFisca France :** https://github.com/openfisca/openfisca-france/blob/master/CHANGELOG.md

# [Conteneurisation] Utilisation de Docker

- **local :** contient les fichiers de configuration pour lancer l'application en local avec Docker Compose
- **dist :** contient les fichiers de configuration pour l'environnement de recette et de production. Le conteneur est déployé sur un serveur Docker Swarm

## Démarrer l'application OpenFisca en local avec Docker Compose

**Prérequis :** installer [Docker](https://docs.docker.com/engine/install/) et [Docker Compose](https://docs.docker.com/compose/install/).

1. Exécuter la commande suivante pour construire l'image :

    ```shell
    foo@bar:~openfisca-france$ docker build . -f ./docker-image/Dockerfile -t openfisca-france
    ```
1. Exécuter la commande suivante pour démarrer le conteneur :

    ```shell
    foo@bar:~openfisca-france$ docker-compose  -f ./local/docker-compose.yml up -d
    ```

# [OpenFisca] Quelques trucs utiles

- Executer la commande suivante pour connaître la version du package openfisca-france d'installé dans le conteneur :

Remplacer la variable **%id_conteneur%** par l'id du conteneur. Utiliser la commande **docker container ls** pour connaître l'id du conteneur.

```shell
foo@bar:~$ docker exec -it %id_conteneur% pip show openfisca-france
```



