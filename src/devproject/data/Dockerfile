FROM SRC_IMAGE
RUN groupadd -o --gid SRC_GID SRC_USER \
    && useradd --uid SRC_UID --gid SRC_GID -d /home/SRC_USER-dev -m SRC_USER \
    && apt-get update \
    && apt-get install bash-completion sudo \
    && echo SRC_USER ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/SRC_USER \
    && chmod 0440 /etc/sudoers.d/SRC_USER
USER SRC_USER
RUN pip install --upgrade pip \
    && pip install mypy isort black pre-commit \
    && curl -fsSL https://get.docker.com | sh \
    && (getent group SRC_DOCKER || sudo groupadd --gid SRC_DOCKER docker || sudo groupmod --gid SRC_DOCKER docker) \
    && sudo usermod -aG SRC_DOCKER SRC_USER
WORKDIR SRC_WORKDIR
