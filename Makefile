#################################################################################
#
# Makefile to build the project
#
#################################################################################
PROJECT_NAME = de-final-project
REGION = eu-west-2
PYTHON_VERSION = 3.11
WD=$(shell pwd)
PYTHONPATH="$(WD):$(WD)/src"
SHELL := /bin/bash
PROFILE = default
PIP:=pip
MOTO = 'moto[ec2,s3,all]'

## Create python interpreter environment.

create-environment: 
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> Setting up python$(PYTHON_VERSION) VirtualEnv. "
	( \
		$(PIP) install -q virtualenv virtualenvwrapper; \
	    virtualenv venv --python=$(PYTHON_VERSION); \
	)

# Define utility variable to help calling Python from the virtual environment
ACTIVATE_ENV := source venv/bin/activate

# Execute python related functionalities from within the project's environment
define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

# Define the check_and_install_python_version target
check_and_install_python_version:
	@echo ">>> check pyenv versions installed..."
	( \
		pyenv versions; \
	)
	@pyenv versions | grep -q $(PYTHON_VERSION) || (pyenv install $(PYTHON_VERSION) && echo "Python $(PYTHON_VERSION) installed.")


## Build the environment requirements
requirements: create-environment
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)

################################################################################################################
# Set Up
## Install bandit
bandit:
	$(call execute_in_env, $(PIP) install bandit)

## Install safety
safety:
	$(call execute_in_env, $(PIP) install safety)

## Install flake8
black:
	$(call execute_in_env, $(PIP) install black)

## Install coverage
coverage:
	$(call execute_in_env, $(PIP) install coverage)

pytest: 
	$(call execute_in_env, $(PIP) install pytest)

moto:
	$(call execute_in_env, $(PIP) install $(MOTO))


## Set up dev requirements (bandit, safety, flake8, pytest, moto)
dev-setup: bandit safety black coverage pytest moto

# Build / Run

## Run the security test (bandit + safety)
security-test:
	$(call execute_in_env, safety check -r requirements.txt)
	$(call execute_in_env, bandit -lll */*.py *c/*/*.py)

## Run the flake8 code check
run-black:
	$(call execute_in_env, black  ./src/*/*.py ./test/*/*.py)

## Run the unit tests
unit-test:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest -v)

## Run the coverage check
check-coverage:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} coverage run --omit 'venv/*' -m pytest && coverage report -m)

## Run all checks
run-checks: security-test run-black unit-test check-coverage

## Make all
all: delete-venv check_and_install_python_version requirements dev-setup run-checks

#################################################### John additions ############################################################ 

## Delete venv
delete-venv:
	rm -rf venv

## Delete pycache
clean:
	@echo "Cleaning up Python __pycache__ directories..."
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@echo "Cleanup complete."

## Create new project venv from project_primary_dependencies and builds new requirements.txt file
new-project-requirements: delete-venv create-environment
	$(call execute_in_env, $(PIP) install -r project_primary_dependencies.txt)
	$(call execute_in_env, $(PIP) freeze > requirements.txt)

## Create new lambda venv from module_requirements and builds new lambda_requirements.txt file
new-lambda-one-requirements: delete-venv create-environment
	$(call execute_in_env, $(PIP) install -r ./src/lambda_one/lambda_primary_dependencies.txt)
	$(call execute_in_env, $(PIP) freeze > ./src/lambda_one/lambda_requirements.txt)

new-lambda-two-requirements: delete-venv create-environment
	$(call execute_in_env, $(PIP) install -r ./src/lambda_two/lambda_primary_dependencies.txt)
	$(call execute_in_env, $(PIP) freeze > ./src/lambda_two/lambda_requirements.txt)
