resource "aws_lambda_layer_version" "lambda_one_dependencies" {
  depends_on = [data.archive_file.lambda_dependencies_zip]
  layer_name          = "lambda-one-dependencies"
  filename            = "${path.module}/../tmp/lambda_dependencies.zip"
}