FROM ghcr.io/astral-sh/uv:0.11.0 AS uv
FROM ubuntu:24.04

ARG USER=vscode
ARG GROUP=${USER}
ARG UID
ARG GID
ARG WORKDIR=/app

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    bash-completion \
    sudo \
    ca-certificates \
    git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd --gid ${GID} ${GROUP} && \
    useradd --uid ${UID} --gid ${GID} --groups sudo --shell /bin/bash --create-home ${USER} && \
    echo "$USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

COPY --from=uv /uv /uvx /bin/

USER ${USER}
WORKDIR ${WORKDIR}
COPY --chown=${USER}:${GROUP} .python-version pyproject.toml uv.lock requirements.yml ./
RUN uv python install && uv sync --frozen
RUN uv run ansible-galaxy collection install -r requirements.yml
