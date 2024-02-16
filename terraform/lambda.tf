resource "aws_lambda_function" "s3_file_reader" {
  depends_on = [data.archive_file.lambda_one_zip,aws_lambda_layer_version.lambda_one_dependencies]
  filename = "${path.module}/../tmp/lambda_one.zip"
  function_name = "lambda_handler"
  role          = aws_iam_role.lambda_one_role.arn
  handler       = "lambda_one.lambda_handler"
  runtime = "python3.9"
  timeout = 600
  layers = [aws_lambda_layer_version.lambda_one_dependencies.arn]
}

