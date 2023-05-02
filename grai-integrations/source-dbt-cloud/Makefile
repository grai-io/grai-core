.PHONY: help
.DEFAULT_GOAL := help

build_manifest:  ## Run migrations
	poetry run datamodel-codegen --input v8.json --output src/grai_source_dbt/models/manifest/v8.py


#---------------------------------------------

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
