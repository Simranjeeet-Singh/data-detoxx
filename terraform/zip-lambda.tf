resource "null_resource" "install_dependencies" {
  provisioner "local-exec" {
    command = "pip install -r ${path.module}/../src/lambda_code/requirements.txt -t ${path.module}/../tmp/dependencies/python"
  }
  triggers = {
  always_run = timestamp()
  }
}

data "archive_file" "lambda_dependencies_zip" {
  depends_on = [null_resource.install_dependencies]
  excludes   = [
    "__pycache__",
    "venv",
  ]
  type             = "zip"
  source_dir      = "${path.module}/../tmp/dependencies"
  output_path      = "${path.module}/../tmp/lambda_dependencies.zip"
}

data "archive_file" "lambda_one_zip" {
  depends_on = [data.archive_file.lambda_dependencies_zip]
  type             = "zip"
  output_path      = "${path.module}/../tmp/lambda_one.zip"
  source_dir       = "${path.module}/../src/lambda_code"
}