.PHONY: help
.DEFAULT_GOAL := help



build_docs:  ## Run migrations
	# --logo, --logo-link, --favicon,
	poetry run pdoc grai_client -o ./docs/html --mermaid --math
	find ./docs/html -iname "*.html" -type f -exec sh -c 'pandoc "${0}" -o "./docs/md/$(basename ${0%.html}.md)"' {} \;


#---------------------------------------------

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
