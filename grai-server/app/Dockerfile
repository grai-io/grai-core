# pull official base image
FROM python:3.10.5-slim-buster

WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE="1" \
    PYTHONUNBUFFERED="1" \
    OUR_ENV="${YOUR_ENV}" \
    PYTHONFAULTHANDLER="1" \
    PYTHONHASHSEED="random" \
    PIP_NO_CACHE_DIR="off" \
    PIP_DISABLE_PIP_VERSION_CHECK="on" \
    PIP_DEFAULT_TIMEOUT="100" \
    POETRY_VERSION="1.2.2"

# libpq-dev and gcc are used to install psycopg2.
RUN apt update \
    && apt install -y apt-utils netcat libpq-dev gcc

COPY . .

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false  \
    && poetry install --no-interaction --no-ansi --no-root --no-dev \
    && rm -rf ~/.cache/pypoetry/cache \
    && rm -rf ~/.cache/pypoetry/artifacts

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# TODO: Switch to multistage builds
# https://docs.docker.com/develop/develop-images/multistage-build/#use-multi-stage-builds