FROM SRC_IMAGE
WORKDIR SRC_WORKDIR
RUN groupadd -o --gid SRC_GID SRC_USER \
    && useradd --uid SRC_UID --gid SRC_GID -m SRC_USER \
    && apt-get update \
    && apt-get install bash-completion sudo \
    && echo SRC_USER ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/SRC_USER \
    && chmod 0440 /etc/sudoers.d/SRC_USER
USER SRC_USER
COPY .bashrc .profile /home/SRC_USER/
RUN sudo chown SRC_USER:SRC_GID /home/SRC_USER/.bashrc /home/SRC_USER/.profile \
    && pip install mypy \
    && git config --global user.name SRC_GIT_USER \
    && git config --global user.email SRC_GIT_EMAIL \
    && git config --global --add safe.directory SRC_WORKSPACE \
    && echo .devcontainer/ >> /home/SRC_USER/.gitignore \
    && echo .devtmp/ >> /home/SRC_USER/.gitignore \
    && git config --global core.excludesfile /home/SRC_USER/.gitignore
