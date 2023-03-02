clean:
	@echo "Execute cleaning ..."
	rm -f *.pyc
	rm -f .coverage
	rm -f coverage.xml

create-pre-commit:
	@echo "Creating pre-commit hook..."
	bash create_precommit.sh

lint:
	pylint --rcfile=.pylintrc --django-settings-module=core.settings */

test:
	python manage.py test

commit-test:
	python manage.py test --exclude-tag=exclude_git_commit

build:
	@echo "Building docker images..."
	bash build-containers.sh

up-containers:
	@echo "Bringing containers up..."
	bash up-containers.sh

down-containers:
	@echo "Bringing containers down..."
	bash down-containers.sh