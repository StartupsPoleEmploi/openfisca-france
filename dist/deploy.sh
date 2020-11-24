#connect to private container registry
echo "$3" | docker login -u $2 --password-stdin $1

container_name=openfisca
# if new version is passed and container exists, update openfisca image
docker stack deploy --with-registry-auth -c openfisca-$4-stack.yml openfisca-france

#clean docker environment
docker system prune --force

#logout docker registry
docker logout $1

