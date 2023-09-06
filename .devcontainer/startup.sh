IMAGE=$(cat .devcontainer/devcontainer.json | grep '"image":' | sed -n 's/.*: "\([^",]*\)"\{0,1\},\{0,1\}/\1/p')
FROM_IMAGE=$(echo $IMAGE | sed 's/\(.*\)---.*/\1/')
docker inspect ${IMAGE} 1>/dev/null || docker build \
    -t ${IMAGE} \
    --build-arg FROM_IMAGE=${FROM_IMAGE} \
    --build-arg USER=$(id -un) \
    --build-arg USER_UID=$(id -u) \
    --build-arg USER_GID=$(id -g) \
    --build-arg DOCKER_GID=$(getent group docker | cut -d: -f3) \
    .devcontainer
