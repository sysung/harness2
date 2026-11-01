FROM node:22-bookworm-slim AS node
FROM python:3.12-slim-bookworm
ARG HARNESS2_REV=1cfe254e8d25b15f37048c3730134686abe60335
ARG CODEX_VERSION=0.166.0
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules/npm /usr/local/lib/node_modules/npm
RUN ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
    && npm install -g @openai/codex@${CODEX_VERSION} \
    && git init /opt/harness2 \
    && git -C /opt/harness2 remote add origin https://github.com/google-research/harness2.git \
    && git -C /opt/harness2 fetch --depth 1 origin ${HARNESS2_REV} \
    && git -C /opt/harness2 checkout --detach FETCH_HEAD \
    && pip install --no-cache-dir /opt/harness2 \
    && useradd --create-home --uid 1000 researcher \
    && mkdir -p /workspace /home/researcher/.codex \
    && chown -R researcher:researcher /workspace /home/researcher
USER researcher
ENV CODEX_HOME=/home/researcher/.codex
WORKDIR /workspace
CMD ["harness2-demo", "--output", "/workspace/runs/demo", "--k", "1"]
