![logo OpenFisca](.gitlab/images/openfisca.png)

:gb: [English version](https://github.com/StartupsPoleEmploi/openfisca-france/blob/9c3f813f04f7c94b47984982fce9aa12c9eab6f1/README_EN.md)

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

# [Suivi opérationnel] Comment dépanner l'application sur un serveur Docker Swarm ?

- Vérifier que l'application fonctionne correctement :

   ```
   foo@bar:~$ docker container ls | grep openfisca-france
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

## Zero Downtime Deployment

Le service Docker a été configuré afin d'éviter un temps de coupure du service au redémarrage de l'application.

```
healthcheck:
  test: curl -v --silent http://localhost:5000/variables || exit 1
  timeout: 30s
  interval: 1m
  retries: 10
  start_period: 30s
deploy:
  replicas: 2
  update_config:
    parallelism: 1
    order: start-first
    failure_action: rollback
    delay: 10s
  rollback_config:
    parallelism: 0
    order: stop-first
  restart_policy:
    condition: any
    delay: 5s
    max_attempts: 3
    window: 180s
```

Cette configuration permet une réplication du service avec 2 replicas. Lors d'un redémarrage, un service sera considéré opérationnel que si le test du healthcheck a réussi. Si un redémarrage est lancé, Docker va mettre à jour un premier service et s'assurer que le conteneur soit au statut healthy avant de mettre à jour le second service.

## Limitation des ressources CPU et RAM

Afin de gérer au mieux les ressources du serveur, la quantité de ressources CPU et de mémoire que peut utliser un conteneur a été limitée :

```
resources:
  reservations:
    cpus: '0.20'
    memory: 512Mi
  limits:
    cpus: '0.75'
    memory: 2048Mi
```

Voir la consommation CPU et mémoire des conteneurs Docker :
```
foo@bar:~$ docker stats
```

# [Livraison] Livrer une nouvelle version en production

Une image Docker Python contenant le code source de l'application OpenFisca est livrée sur les différents environnements (recette, production). Cette image est versionnée en **release-candidate pour la recette** et en **release pour la production**.

## Procédure de build et de livraison d'une version release en production

Après s'être assuré du bon fonctionnement de l'application sur l'environnement de recette, voici les étapes à suivre pour livrer la version de l'application de recette en production.

### La veille de la mise en prodction

* lancer dans le pipeline GitLab CI, le job **build-docker-image-production** 

### Mise en production le lendemain

* lancer le job **deploy_application_production**

* se connecter sur la machine pour vérifier que tout se passe bien, voir section [Suivi opérationnel](#suivi-opérationnel-comment-dépanner-lapplication-sur-un-serveur-docker-swarm-)

*  envoyer une notification à l'équipe
