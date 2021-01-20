![logo OpenFisca](.gitlab/images/openfisca.png)

# [OpenFisca France] Moteur de calculs d'aides sociales (prime d'activité, RSA, etc...)

Ce projet permet de **conteneuriser** l'application **OpenFisca France** en utilisant Docker.

Ce projet a été conçu dans le cadre de la réalisation de l'application [Estime](https://git.beta.pole-emploi.fr/estime/estime-frontend/-/blob/master/README.md).

OpenFisca France est un moteur de calcul Open source développé dans le language Python qui permet de faire des simulations sur le système socio-fiscal français.

- **Accéder au Github du projet** : https://github.com/openfisca/openfisca-france
- **Suivi des versions de OpenFisca France :** https://github.com/openfisca/openfisca-france/blob/master/CHANGELOG.md
- **Documentation de l'api :** https://fr.openfisca.org/legislation/swagger
- **Explorateur du modèle de données OpenFisca :** https://fr.openfisca.org/legislation

# [Conteneurisation] Utilisation de Docker

**Structuration du projet :**

- **local :** contient les fichiers de configuration pour lancer l'application en local avec Docker Compose
- **dist :** contient les fichiers de configuration pour l'environnement de recette et de production. Le conteneur est déployé sur un serveur Docker Swarm

## Démarrer l'application OpenFisca en local avec Docker Compose

**Prérequis :** installer [Docker](https://docs.docker.com/engine/install/) et [Docker Compose](https://docs.docker.com/compose/install/).

1. Contruire l'image Docker **openfisca-france** 

   1. Se positionner dans le répertoire **docker-image**
   1. Exécuter la commande suivante pour construire l'image :

      ```shell
      foo@bar:~openfisca-france/docker-image$ docker build -t openfisca-france .
      ```
1. Exécuter la commande suivante pour démarrer le conteneur :

    ```shell
    foo@bar:~openfisca-france$ docker-compose  -f ./local/docker-compose.yml up -d
    ```
1. L'application est accessible sur http://localhost:5000

# [OpenFisca] Quelques trucs utiles

## Connaître la version de OpenFisca France

Executer la commande ci-dessous pour connaître la version du package openfisca-france installé dans le conteneur.

Remplacer la variable **%id_conteneur%** par l'id du conteneur. Utiliser la commande **docker container ls** pour connaître l'id du conteneur.

```shell
foo@bar:~$ docker exec -it %id_conteneur% pip show openfisca-france
```

# [Suivi opérationnel] Comment dépanner l'application sur les environnements distants (recette et production) ?

Il faut au préablable se connecter sur une des machines distantes avec un **utilisateur ayant les droits Docker**.

Le fichier de la stack Docker Swarm se trouve dans le répertoire **/home/docker/openfisca**.

- Vérifier que le service est bien au statut **running** en exécutant la commande suivante :

   ```
   foo@bar:~$ docker stack ps openfisca-france
   ```
   2 replicas ont été déclarés, vous devriez donc voir 2 services à l'état **running**

- Voir les logs du service en exécutant la commande suivante :

   ```
   foo@bar:~$ docker service logs openfisca-france_openfisca-france
   ```

- Démarrer ou relancer les services

   - Se positionner dans le répertoire **/home/docker/openfisca**
   - Se connecter au registry privé du Gitlab de l'incubateur en executant la commande suivante :

      Vous devez au préalable avoir récupéré un token depuis votre compte Gitlab. Ce token vous servira de mot de passe.

      ```
      foo@bar:~$ docker login registry.beta.pole-emploi.fr
      ```
   - Une fois connecté au registry, vous devez exécuter la commande suivante pour démarrer ou relancer les services :

      ```
      foo@bar:/home/docker/openfisca$ docker stack deploy --with-registry-auth -c openfisca-production-stack.yml openfisca-france
      ```

- Stopper les services en exécutant la commande suivante :

   ```
   foo@bar:~$ docker stack rm openfisca-france
   ```
