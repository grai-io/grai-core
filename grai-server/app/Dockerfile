# pull official base image
FROM python:3.11-slim-bookworm AS builder

WORKDIR /usr/src/app

ARG PYTHONDONTWRITEBYTECODE="1" \
    PYTHONUNBUFFERED="1" \
    PYTHONFAULTHANDLER="1" \
    PYTHONHASHSEED="random" \
    PIP_NO_CACHE_DIR="off" \
    PIP_DISABLE_PIP_VERSION_CHECK="on" \
    PIP_DEFAULT_TIMEOUT="100" \
    POETRY_VERSION="1.5.1"

COPY pyproject.toml poetry.lock ./

# libpq-dev, and gcc are used to install psycopg2.
# unixodbc-dev, g++ are required for pyodbc (note gcc should come with g++)
RUN apt update \
    && apt install --no-install-recommends -y \
      apt-utils \
      libpq-dev \
      g++ \
      gcc \
      unixodbc-dev \
    && pip install "poetry==${POETRY_VERSION}" \
    && poetry config virtualenvs.create false \
    && poetry lock \
    && poetry install --no-root --no-interaction --no-ansi \
    && poetry version -s > /version.txt

COPY . .

RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh && chmod +x /usr/src/app/entrypoint.sh \
    && sed -i 's/\r$//g' /usr/src/app/initialize_db.sh && chmod +x /usr/src/app/initialize_db.sh \
    && sed -i 's/\r$//g' /usr/src/app/beat.sh && chmod +x /usr/src/app/beat.sh \
    && sed -i 's/\r$//g' /usr/src/app/worker.sh && chmod +x /usr/src/app/worker.sh


ENV SECRET_KEY="dummy"
RUN python manage.py collectstatic --noinput


# --------- base image --------------- #

FROM python:3.11-slim-bookworm AS base
LABEL org.opencontainers.image.source="https://github.com/grai-io/grai-core"
WORKDIR /usr/src/app


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    INSTANCE_TYPE=server \
    TIKTOKEN_CACHE_DIR=/opt/tiktoken_cache \
    PGSSLCERT=/tmp/postgresql.crt \
    SNOWFLAKE_HOME=/opt/snowflake


COPY --from=builder /version.txt /version.txt
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/src/app/ /usr/src/app/

# netcat is used to wait for the database to be ready.
# curl is used to support healthchecks
# The Snowflake code handles a SnowFlake error requiring a connections.toml file to exist
# https://github.com/snowflakedb/snowflake-connector-python/issues/2036
RUN apt update \
    && apt install --no-install-recommends -y  \
      curl  \
      netcat-openbsd \
      bash  \
      libpq-dev \
      unixodbc-dev \
      gnupg2 \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir ${TIKTOKEN_CACHE_DIR} \
    && python ai_build_script.py \
    && mkdir ${SNOWFLAKE_HOME} \
    && chmod 755 ${SNOWFLAKE_HOME} \
    && touch ${SNOWFLAKE_HOME}/connections.toml


# RUN mkdir ${SNOWFLAKE_HOME} \
#     && chmod 755 ${SNOWFLAKE_HOME} \
#     && touch ${SNOWFLAKE_HOME}/connections.toml

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# --------- final images --------------- #

FROM base AS grai-server
ENV TIKTOKEN_CACHE_DIR=/opt/tiktoken_cache
CMD ["gunicorn", "the_guide.asgi:application", "-b", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker"]


FROM base AS grai-worker
ENV INSTANCE_TYPE=worker \
    TIKTOKEN_CACHE_DIR=/opt/tiktoken_cache \
    SNOWFLAKE_HOME=/opt/snowflake
CMD ["/usr/src/app/worker.sh"]

FROM base AS grai-beat-worker
ENV INSTANCE_TYPE=beat \
    TIKTOKEN_CACHE_DIR=/opt/tiktoken_cache \
    SNOWFLAKE_HOME=/opt/snowflake
CMD ["/usr/src/app/beat.sh"]
