# pull official base image
FROM python:3.10.5-slim-buster AS build

WORKDIR /usr/src/app
ARG PYTHONDONTWRITEBYTECODE="1" \
    PYTHONUNBUFFERED="1" \
    OUR_ENV="${YOUR_ENV}" \
    PYTHONFAULTHANDLER="1" \
    PYTHONHASHSEED="random" \
    PIP_NO_CACHE_DIR="off" \
    PIP_DISABLE_PIP_VERSION_CHECK="on" \
    PIP_DEFAULT_TIMEOUT="100" \
    POETRY_VERSION="1.2.2"

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

COPY pyproject.toml poetry.lock ./

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false  \
    && poetry install --no-interaction --no-ansi --no-root --only main \
    && rm -rf ~/.cache/pypoetry/cache \
    && rm -rf ~/.cache/pypoetry/artifacts

COPY . .

RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
CMD gunicorn the_guide.wsgi -b 0.0.0.0:8000 -w 2
