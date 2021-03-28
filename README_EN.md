![logo OpenFisca](.gitlab/images/openfisca.png)

# [OpenFisca France] use Docker

This project contains Docker configutions to containerized **OpenFisca France** application

This project has been realized within the scope of the realization of [Estime](https://github.com/StartupsPoleEmploi/estime-frontend).

- **Access to OpenFisca Github project** : https://github.com/openfisca/openfisca-france
- **API documentation :** https://fr.openfisca.org/legislation/swagger
- **Explore OpenFisca data model :** https://fr.openfisca.org/legislation

# [Project Structuration] Utilisation de Docker

- **local :** configuration files to launch the application in local environment with Docker Compose
- **dist :** configuration files for staging and production environments and a deployment on a Docker Swarm server

## Launch OpenFisca application in your local environment with Docker Compose

**Prerequisites :** install [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/).

1. Build **openfisca-france** Docker image

   ```shell
   foo@bar:~openfisca-france/docker-image$ docker build -t openfisca-france .
   ```
1. Start the container :

    ```shell
    foo@bar:~openfisca-france$ docker-compose  -f ./local/docker-compose.yml up -d
    ```
1. The application is accessible on http://localhost:5000

# [OpenFisca] Know OpenFisca France version used

```shell
foo@bar:~$ docker exec -it %container id% pip show openfisca-france
```

# [Server Environment] How to manage the application on a Docker Swarm server ?

- Check application status :

   ```
   foo@bar:~$ docker stack ps openfisca-france
   ```
   Containers must be in status UP and healthy.

- Watch logs :

   ```
   foo@bar:~$ docker service logs openfisca-france_openfisca-france
   ```

- Start or restart the service

   - Go to **/home/docker/openfisca** directory
   - Execute the next command :

      ```
      foo@bar:/home/docker/openfisca$ docker stack deploy --with-registry-auth -c openfisca-production-stack.yml openfisca-france
      ```

- Stop the service :

   ```
   foo@bar:~$ docker stack rm openfisca-france
   ```
