![logo OpenFisca](.gitlab/images/openfisca.png)

# [OpenFisca France] Moteur de calculs d'aides sociales (prime d'activité, RSA, etc...)

Ce projet permet de **conteneuriser** l'application **OpenFisca France** avec Docker.

Ce projet a été conçu dans le cadre de la réalisation de l'application [Estime](https://git.beta.pole-emploi.fr/estime/estime-frontend/-/blob/master/README.md).

OpenFisca France est un moteur de calcul Open source développé dans le language Python qui permet de faire des simulations sur le système socio-fiscal français.

- **Accéder au Github du projet** : https://github.com/openfisca/openfisca-france
- **Suivi des versions de OpenFisca France :** https://github.com/openfisca/openfisca-france/blob/master/CHANGELOG.md
- **Documentation de l'api :** https://fr.openfisca.org/legislation/swagger
- **Explorateur du modèle de données OpenFisca :** https://fr.openfisca.org/legislation

# [Conteneurisation] Utilisation de Docker

**Structuration du projet :**

- **local :** fichiers de configuration pour lancer l'application en local avec Docker Compose
- **dist :** fichiers de configuration pour l'environnement de recette et de production. Le conteneur est déployé sur un serveur Docker Swarm

## Démarrer l'application OpenFisca en local avec Docker Compose

**Prérequis :** installer [Docker](https://docs.docker.com/engine/install/) et [Docker Compose](https://docs.docker.com/compose/install/).

1. Contruire l'image Docker

   ```shell
   foo@bar:~openfisca-france/docker-image$ docker build -t openfisca-france .
   ```
1. Démarrer le conteneur :

    ```shell
    foo@bar:~openfisca-france$ docker-compose  -f ./local/docker-compose.yml up -d
    ```
1. L'application est accessible sur http://localhost:5000

# [OpenFisca] Connaître la version de OpenFisca France

```shell
foo@bar:~$ docker exec -it %id_conteneur% pip show openfisca-france
```

# [Suivi opérationnel] Comment dépanner l'application sur les environnements distants (recette et production) ?

- Vérifier que l'application fonctionne correctement :

   ```
   foo@bar:~$ docker stack ps openfisca-france
   ```
   Les conteneurs doivent être au statut UP et healthy.

- Consulter les logs :

   ```
   foo@bar:~$ docker service logs openfisca-france_openfisca-france
   ```

- Démarrer ou relancer les services

   - Se positionner dans le répertoire **/home/docker/openfisca**
   - Exécuter la commande suivante :

     ```
     foo@bar:/home/docker/openfisca$ docker stack deploy --with-registry-auth -c openfisca-production-stack.yml openfisca-france
     ```

- Stopper le service :

   ```
   foo@bar:~$ docker stack rm openfisca-france
   ```
