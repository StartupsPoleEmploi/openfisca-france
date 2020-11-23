#connect to private container registry
echo "$3" | docker login -u $2 --password-stdin $1

container_name=openfisca
# if new version is passed and container exists, update openfisca image
if [ ! -z "$4" ] && [sudo docker container ls -a --format '{{.Names}}' | grep -Eq "^${container_name}\$"]; then
  docker service update --image registry.beta.pole-emploi.fr/estime/openfisca:$4 openfisca-france
else
  docker stack deploy --with-registry-auth -c openfisca-stack.yml openfisca-france
fi

#clean docker environment
docker image prune --force
docker container prune --force
docker volume prune --force

#logout docker registry
docker logout $1

