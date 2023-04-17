.PHONY: help
.DEFAULT_GOAL := help


publish_all:  ## Run migrations
	bash publish_all.sh


#---------------------------------------------

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
