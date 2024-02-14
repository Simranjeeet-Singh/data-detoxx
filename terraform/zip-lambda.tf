resource "null_resource" "install_dependencies" {
  provisioner "local-exec" {
    command = "pip install -r ${path.module}/../src/requirements.txt -t ${path.module}/../src/"
  }
}

data "archive_file" "lambda_zip" {
  depends_on = [null_resource.install_dependencies]
  excludes   = [
    "__pycache__",
    "venv",
  ]
  type             = "zip"
  source_dir       = "${path.module}/../src"
  output_path      = "${path.module}/../lambda_one.zip"
}