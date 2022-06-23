ARG build_for=linux/amd64

FROM --platform=$build_for postgres:14.3-bullseye as grai

ARG grai_core_ref=grai-core@v0.1.0
ARG grai_db_ref=grai-db@v0.1.0

##
# grai-core
##

FROM base as grai-core

##
# grai-postgres
##
FROM base as grai-postgres
ENTRYPOINT ["grai"]
