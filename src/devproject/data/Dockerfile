ARG FROM_IMAGE
FROM ${FROM_IMAGE}
ARG USER
RUN groupadd -o --gid SRC_GID ${USER} \
    && useradd --uid SRC_UID --gid SRC_GID -d /home/${USER}-dev -m ${USER} \
    && apt-get update \
    && apt-get install bash-completion sudo \
    && echo ${USER} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USER} \
    && chmod 0440 /etc/sudoers.d/${USER}
USER ${USER}
RUN pip install --upgrade pip \
    && pip install mypy isort black pre-commit \
    && curl -fsSL https://get.docker.com | sh \
    && (getent group SRC_DOCKER || sudo groupadd --gid SRC_DOCKER docker || sudo groupmod --gid SRC_DOCKER docker) \
    && sudo usermod -aG SRC_DOCKER ${USER} \
    && echo .devcontainer.json >> ~/.gitignore
