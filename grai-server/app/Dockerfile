# pull official base image
FROM python:3.11-slim-buster AS build

LABEL org.opencontainers.image.source="https://github.com/grai-io/grai-core"

WORKDIR /usr/src/app

ENV PATH=$PATH:/root/.cargo/bin

ARG PYTHONDONTWRITEBYTECODE="1" \
    PYTHONUNBUFFERED="1" \
    PYTHONFAULTHANDLER="1" \
    PYTHONHASHSEED="random" \
    PIP_NO_CACHE_DIR="off" \
    PIP_DISABLE_PIP_VERSION_CHECK="on" \
    PIP_DEFAULT_TIMEOUT="100" \
    POETRY_VERSION="1.3.1"

# libpq-dev, and gcc are used to install psycopg2.
# netcat is used to wait for the database to be ready.
# curl is used to support healthchecks
# unixodbc-dev, g++ are required for pyodbc (note gcc should come with g++)
RUN apt update \
    && apt install -y \
    apt-utils \
    netcat \
    libpq-dev \
    gcc \
    g++ \
    curl \
    unixodbc-dev \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# Install MS SQL driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18


COPY pyproject.toml poetry.lock ./

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false  \
    && poetry lock --no-update \
    && poetry install --no-interaction --no-ansi --no-root --only main \
    && rm -rf ~/.cache/pypoetry/cache \
    && rm -rf ~/.cache/pypoetry/artifacts


COPY ./worker.sh /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker \
    && chmod +x /start-celeryworker

COPY ./beat.sh /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat \
    && chmod +x /start-celerybeat

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh \
    && chmod +x /usr/src/app/entrypoint.sh

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
CMD gunicorn the_guide.wsgi -b 0.0.0.0:8000 -w 2
