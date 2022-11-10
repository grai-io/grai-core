.PHONY: help
.DEFAULT_GOAL := help

APP=grai-server_the_guide_1
ECR_REPOSITORY=grai-io/the_guide
ECR_REGISTRY=627169567483.dkr.ecr.us-east-2.amazonaws.com
GHCR_REPOSITORY=ghcr.io/grai-io/grai-core/grai-server
APP_VERSION:=`cd app; poetry version -s`
BUILD_DIRECTORY=app/

migrations:  ## Run migrations
	docker exec $(APP) sh -c "python manage.py makemigrations; exit $?"

run:  ## Run an optional $CMD
	docker-compose run the_guide python manage.py $(cmd)
	docker exec -it $(APP) sh -c "python manage.py $(cmd); exit $?"

create_admin_user:  ## Create a super user
	docker exec -it $(APP) python manage.py createsuperuser

build_ecr:  ## Build image and upload to ECR
	aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin $(ECR_REGISTRY)
	docker build -t $(ECR_REPOSITORY):dev app/
	docker tag $(ECR_REPOSITORY):dev $(ECR_REGISTRY)/$(ECR_REPOSITORY):dev
	aws ecr batch-delete-image --repository-name grai-io/the_guide --image-ids imageTag=dev &> /dev/null
	docker push $(ECR_REGISTRY)/$(ECR_REPOSITORY):dev
	kubectl delete -k k8s/dev
	make deploy_dev

deploy_dev:  ## Deploy to dev
	sops -d -i k8s/dev/secrets.env
	kubectl apply -k k8s/dev
	sops -e -i k8s/dev/secrets.env


build_ghcr:  ## Build image and upload to ghcr
	#echo $CR_PAT | docker login ghcr.io -u ieaves --password-stdin
	docker buildx build --platform linux/amd64,linux/arm64 -t $(GHCR_REPOSITORY):latest app/ --output=type=registry,dest=$(GHCR_REPOSITORY)
	docker push $(GHCR_REPOSITORY):latest
	docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/grai-io/grai-core/grai-server:$(APP_VERSION) app/ --output=type=registry,dest=ghcr.io/grai-io/grai-core/grai-server:$(APP_VERSION)
	docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/grai-io/grai-core/grai-server:latest app/ --output=type=registry,dest=ghcr.io/grai-io/grai-core/grai-server:latest


build_dev_ghcr:  ## Build image and upload to ghcr
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		-t $(GHCR_REPOSITORY):dev \
		--output=type=registry,dest=$(GHCR_REPOSITORY)\
		$(BUILD_DIRECTORY)

#---------------------------------------------

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
