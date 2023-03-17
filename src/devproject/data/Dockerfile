FROM SRC_IMAGE
RUN groupadd -o --gid SRC_GID SRC_USER \
    && useradd --uid SRC_UID --gid SRC_GID -m SRC_USER \
    && apt-get update \
    && apt-get install bash-completion sudo \
    && echo SRC_USER ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/SRC_USER \
    && chmod 0440 /etc/sudoers.d/SRC_USER
WORKDIR /home/SRC_USER
COPY .bashrc .bash_logout .profile ./
USER SRC_USER
RUN sudo chown SRC_USER:SRC_GID .bashrc .bash_logout .profile \
    && pip install --upgrade pip \
    && pip install mypy isort black pre-commit \
    && git config --global user.name SRC_GIT_USER \
    && git config --global user.email SRC_GIT_EMAIL \
    && git config --global --add safe.directory SRC_WORKSPACE \
    && echo .devcontainer/ >> .gitignore \
    && echo .devtmp/ >> .gitignore \
    && git config --global core.excludesfile /home/SRC_USER/.gitignore \
    && curl -fsSL https://get.docker.com | sh
WORKDIR SRC_WORKDIR
