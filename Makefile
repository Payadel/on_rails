.PHONY: help watch-actions release-action changelog-action version

# Variables
REF := $(if $(ref),$(ref),"dev")
VERSION := $(if $(version),$(version),"")
CREATE_PR_FOR_BRANCH := $(if $(create-pr-for-branch),$(create-pr-for-branch),"main")
GENERATE_CHANGELOG := $(if $(generate-changelog),$(generate-changelog),'auto')

# Targets for running workflow commands
watch-actions: ## Watch a run until it completes, showing its progress
	gh run watch; notify-send "run is done!"

release-action: ## Run release action
	gh workflow run Release --ref $(REF) \
		-f version=$(VERSION) \
		-f create-pr-for-branch=$(CREATE_PR_FOR_BRANCH) \
		-f generate-changelog=$(GENERATE_CHANGELOG)

changelog-action: ## Run changelog action
	gh workflow run Changelog --ref $(REF) -f version=$(VERSION)

# Targets for running standard-version commands
version: ## Get current program version
	node -p -e "require('./package.json').version"

help: ## Display this help message
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@awk -F ':|##' '/^[^\t].+?:.*?##/ { printf "  %-20s %s\n", $$1, $$NF }' $(MAKEFILE_LIST) | sort

.DEFAULT_GOAL := help
