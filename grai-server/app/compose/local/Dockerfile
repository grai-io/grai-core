# pull official base image
FROM python:3.11-slim-buster AS build

LABEL org.opencontainers.image.source="https://github.com/grai-io/grai-core"

WORKDIR /usr/src/app

ENV PATH=$PATH:/root/.cargo/bin

ARG PYTHONDONTWRITEBYTECODE="1" \
    PYTHONUNBUFFERED="1" \
    OUR_ENV="${YOUR_ENV}" \
    PYTHONFAULTHANDLER="1" \
    PYTHONHASHSEED="random" \
    PIP_NO_CACHE_DIR="off" \
    PIP_DISABLE_PIP_VERSION_CHECK="on" \
    PIP_DEFAULT_TIMEOUT="100" \
    POETRY_VERSION="1.3.1"

# libpq-dev, and gcc are used to install psycopg2.
# netcat is used to wait for the database to be ready.
# curl is used to support healthchecks
RUN apt update \
    && apt install -y \
    apt-utils \
    netcat \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl https://sh.rustup.rs -sSf | bash -s -- -y

COPY pyproject.toml poetry.lock ./

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false  \
    && poetry install --no-interaction --no-ansi --no-root --only main \
    && rm -rf ~/.cache/pypoetry/cache \
    && rm -rf ~/.cache/pypoetry/artifacts

COPY . .

COPY ./compose/local/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh


COPY ./compose/local/worker.sh /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

# COPY ./compose/local/django/celery/beat/start /start-celerybeat
# RUN sed -i 's/\r$//g' /start-celerybeat
# RUN chmod +x /start-celerybeat

ENTRYPOINT ["/entrypoint.sh"]
CMD gunicorn the_guide.wsgi -b 0.0.0.0:8000 -w 2