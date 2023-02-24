.PHONY: help
.DEFAULT_GOAL := help


APP=grai-server_the_guide_1
GHCR_REPOSITORY=ghcr.io/grai-io/grai-core/grai-frontend
APP_VERSION=`npm -j ls grai-frontend | jq -r .version`
BUILD_DIRECTORY="."


build_ghcr:  ## Build image and upload to ghcr
	# echo $CR_PAT | docker login ghcr.io -u ieaves --password-stdin
	docker buildx build \
		--platform linux/arm64,linux/amd64 \
		-t $(GHCR_REPOSITORY):latest \
		-t $(GHCR_REPOSITORY):$(APP_VERSION) \
		--output=type=registry,dest=$(GHCR_REPOSITORY)\
		$(BUILD_DIRECTORY)


build_dev_ghcr:  ## Build dev image and upload to ghcr
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		-t $(GHCR_REPOSITORY):dev \
		--output=type=registry,dest=$(GHCR_REPOSITORY)\
		$(BUILD_DIRECTORY)


#---------------------------------------------

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
