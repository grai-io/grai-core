.PHONY: help
.DEFAULT_GOAL := help

SRC_DIR=src/grai_source_fivetran/fivetran_api
MODEL_FILE=api_models.py


# JSON file from https://developers.fivetran.com/openapi/reference/v1/overview/
generate_models:  ## Generate pydantic models from swagger docs
	poetry run python data/fix_encodings.py
	poetry run datamodel-codegen  \
		--output $(SRC_DIR)/$(MODEL_FILE) \
        --input data/processed.json \
        --target-python-version 3.8 \
        --reuse-model
        #--input-file-type openapi \
        #--validation \
	rm data/processed.json


generate_fastapi:  ## Generate fastapi endpoints from swagger docs
	poetry run python data/fix_encodings.py
	poetry run fastapi-codegen  \
		--output $(SRC_DIR) \
		--model-file $(MODEL_FILE) \
        --input data/processed.json
	rm data/processed.json

#---------------------------------------------


help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
