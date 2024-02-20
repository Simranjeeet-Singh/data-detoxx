# DE-project-DataDetox
Github repo for our final project

### Development Setup

- **Python Version Enforcement**: Python version 3.11 is now enforced for the virtual environment (venv). Previously, this was unspecified and would use whatever pyenv you had installed.
- **`make all`**  Run this command to set up project enviroment - deletes exisiting venv, creates python 3.11 venv, install project requirements, install dev tools, run tests, run checks

### Pull Requests
- All merges into main require pull request with at least 1 reviewer
- Must pass all CI/CD checks for merge to be approved

### Makefile Commands

- **`make dev-setup`**: Installs all development dependencies. Future dev dependencies should be added to the Makefile, not `requirements.txt`.
- **`make new-project-requirements`**: Creates a new project virtual environment from `project_primary_dependencies` and builds a new `requirements.txt` file.
- **`make new-lambda-requirements`**: Creates a new lambda virtual environment from `module_requirements` and builds a new `lambda_requirements.txt` file.

These `make new` functions enable us to build a `requirements.txt` file from the primary dependencies specified, making it easier to identify and remove unused dependencies.

### Dependency management

- If you are adding a new dependency to the lambda:
  - Add the module name to the `lambda_primary_dependencies.txt` file located in `src/lambda_code/`.
  - Then run `make new-lambda-requirements`.
- If you are adding a new project dependency:
  - Add the module name to the `project_primary_dependencies.txt` file.
  - Then run `make new-lambda-requirements`.
