resource "aws_lambda_layer_version" "lambda_one_dependencies" {
  depends_on = [data.archive_file.lambda_one_dependencies_zip]
  layer_name          = "lambda-one-dependencies"
  filename            = "${path.module}/../tmp/lambda_one_dependencies.zip"
  source_code_hash = data.archive_file.lambda_one_dependencies_zip.output_base64sha256
}

resource "aws_lambda_layer_version" "lambda_two_dependencies" {
  depends_on = [data.archive_file.lambda_two_dependencies_zip]
  layer_name          = "lambda-two-dependencies"
  filename            = "${path.module}/../tmp/lambda_two_dependencies.zip"
  source_code_hash = data.archive_file.lambda_two_dependencies_zip.output_base64sha256
}

resource "aws_lambda_layer_version" "lambda_three_dependencies" {
  depends_on = [data.archive_file.lambda_three_dependencies_zip]
  layer_name          = "lambda-three-dependencies"
  filename            = "${path.module}/../tmp/lambda_three_dependencies.zip"
  source_code_hash = data.archive_file.lambda_three_dependencies_zip.output_base64sha256
}

resource "aws_lambda_layer_version" "lambda_utils" {
  depends_on = [data.archive_file.lambda_utils_zip]
  layer_name          = "lambda-utils"
  filename            = "${path.module}/../tmp/lambda_utils.zip"
  source_code_hash = data.archive_file.lambda_utils_zip.output_base64sha256
}