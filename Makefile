.PHONY: help watch-actions release-action changelog-action version

# Variables
REF := $(if $(ref),$(ref),"dev")
SKIP_RELEASE_FILE := $(if $(skip_release_file),$(skip_release_file),false)
RELEASE_FILE_NAME := $(if $(release_file_name),$(release_file_name),"release")
RELEASE_DIRECTORY := $(if $(release_directory),$(release_directory),"on_rails")
VERSION := $(if $(version),$(version),"")
SKIP_CHANGELOG := $(if $(skip_changelog),$(skip_changelog),true)
CREATE_PR_FOR_BRANCH := $(if $(create_pr_for_branch),$(create_pr_for_branch),"main")

# Targets for running workflow commands
watch-actions: ## Watch a run until it completes, showing its progress
	gh run watch; notify-send "run is done!"

changelog-action: ## Run changelog action
	gh workflow run Changelog --ref $(REF) -f version=$(VERSION)

release-action: ## Run release action
	gh workflow run Release --ref $(REF) -f skip_release_file=$(SKIP_RELEASE_FILE) -f release_file_name=$(RELEASE_FILE_NAME) -f release_directory=$(RELEASE_DIRECTORY) -f skip_changelog=$(SKIP_CHANGELOG) -f version=$(VERSION) -f create_pr_for_branch=$(CREATE_PR_FOR_BRANCH)

publish-test-action: ## Run publish test action
	gh workflow run 'Publish to Test.PyPI' --ref $(REF) -f version=$(VERSION)

publish-action: ## Run publish action
	gh workflow run 'Publish to PyPI' --ref $(REF) -f version=$(VERSION)

build-action: ## Run build action
	gh workflow run build --ref $(REF)

coverage-action:
	gh workflow run 'Coverage Report' --ref $(REF)

# Targets for running standard-version commands
version: ## Get current program version
	node -p -e "require('./package.json').version"

help: ## Display this help message
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@awk -F ':|##' '/^[^\t].+?:.*?##/ { printf "  %-20s %s\n", $$1, $$NF }' $(MAKEFILE_LIST) | sort

.DEFAULT_GOAL := help
