NAME = clscidapi
PKG_DIR = src/$(NAME)

.PHONY: help
help: # Display help for all Makefile commands
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: change-version
change-version: # Change the version of this project (requires VERSION=#.#.#)
	pipenv run python3 scripts/change-version.py $(VERSION)

.PHONY: build
build: # Build the package tarball and wheel
	pipenv run python3 -m build .

.PHONY: setup
setup: # Setup this project's pipenv environment
	pipenv install -d

.PHONY: install-self
install-self: # Install this project's python package using the pipenv's pip
	pipenv run pip3 install --editable .

.PHONY: clean-py
clean-py: # Clean up Python generated files
	rm -rf $(PKG_DIR)/__pycache__
	rm -rf src/*.egg-info

# Occassionally, this fails if a make release fails after this was run but before
# "dist/*" commited to git. Run "git add dist/*" and rerun make release.
.PHONY: clean
clean: clean-py # Remove build files - including a forced "git rm" of "dist/*"
	git rm -f dist/* --ignore-unmatch
	rm -rf dist

.PHONY: release
release: change-version clean setup build # Build a new versioned release and push it (requires VERSION=#.#.#)
	git add dist/* pyproject.toml $(PKG_DIR)/__init__.py
	git commit -m "build: release v$(VERSION)"
	git push
	git tag -a v$(VERSION) -m "Release v$(VERSION)"
	git push origin v$(VERSION)
	$(MAKE) clean-py
