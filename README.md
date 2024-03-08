# DE-project-DataDetox
Github repo for our Northcoders Data Engineering final project

## Background
Our client Terrific Totes is a manufacturing company that makes customised tote bags for retail and corporate customers. Team Data-Detox has been commissioned to develop a data pipeline to Extract, Transform and Load data from their Online Transactional Processing database (OLTP) to a data lake and Online Analytical Processing (OLAP) data warehouse. All components of the pipeline is hosted in AWS and checked using a CI/CD pipeline implemented using GitHub Actions before being deployed using Terraform.

### Overview
- Full project specification: https://github.com/northcoders/de-project-specification
- OLTP schema: https://dbdiagram.io/d/SampleDB-6332fecf7b3d2034ffcaaa92
- OLAP schema: https://dbdiagram.io/d/RevisedDW-63a19c5399cb1f3b55a27eca

The data pipeline we built uses 3 lambda functions to deliver the ETL process:

1. Ingestor Lambda - extracts data at regular 5min intervals from the client's OLTP database, and stores as .csv file into a s3 ingestion bucket.
2. Processor Lambda - transforms the data from the ingestion bucket into the OLAP star schema, and stores as .parquet file into a s3 processed bucket. Triggered by completion of Ingestor Lambda.
3. Loader Lambda - loads the data from the processed bucket into the client's Online Analytics Processing (OLAP) SQL database hosted in AWS RDS. Triggered by completion of Processor Lambda.
   Robust logging and alarms is implemented for each Lambda. An email notification is sent when an alarm is triggered. A visual overview of the data pipeline is shown below: 
![A visual overview of the data pipeline](/readme_files/PipelineDiagram.png "Data Pipeline - Team Data-Detox")

### Pull Requests
- All merges into main require pull request with at least 1 reviewer
- Must pass all CI/CD checks for merge to be approved

### Development Setup

- **Python Version Enforcement**: Python version 3.11 is enforced for the virtual environment (venv) to ensure compatibility with the AWS Lambda Python 3.11 runtime.
- **`make all`**  Run this command to set up project environment - deletes existing venv, creates python 3.11 venv, install project requirements, install dev tools, run tests, run checks

### Deploying the pipeline via GitHub Actions

This project contains a test-and-deploy.yml file which allows the data pipeline to be deployed automatically via a CI-CD pipeline run via GitHub actions. The test and deploy workflow runs all the checks described in the previous section and then deploys all of the AWS infrastructure using Terraform.

1. Add the credentials for your AWS admin privileges account (under the names AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY) to [GitHub secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions).

2. Run the CI/CD pipeline by pushing your code to any branch on the remote repo.

### Deploying the pipeline locally

Alternatively you can deploy the pipeline by executing commands on your local machine.

1. Add the credentials for your AWS admin privileges account (under the names AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY) to a plaintext file called credentials in a folder called .aws in your home directory.

If you already use Terraform on your machine, skip to 4.

2. Install the AWS command-line-interface tool (instructions [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html))

3. Install Terraform (instructions [here](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli))

4. Initialise Terraform in the tf directory.

```bash
cd terraform
terraform init
```

5. See Terraform's plan for the cloud infrastructure it will build.

```bash
terraform plan
```

6. Build the infrastructure.

```bash
terraform apply
```

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
