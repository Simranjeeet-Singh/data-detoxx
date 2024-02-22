resource "aws_lambda_function" "s3_file_reader" {
  depends_on = [data.archive_file.lambda_one_zip,aws_lambda_layer_version.lambda_one_dependencies]
  filename = "${path.module}/../tmp/lambda_one.zip"
  function_name = "lambda_handler"
  role          = aws_iam_role.lambda_one_role.arn
  handler       = "lambda_one.lambda_handler"
  runtime = "python3.9"
  timeout = 600
  layers = [aws_lambda_layer_version.lambda_one_dependencies.arn, "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python39:16"]
}

#lambda
resource "aws_lambda_function" "s3_processor" {
  depends_on = [data.archive_file.lambda_two_zip]
  #aws_lambda_layer_version.lambda_oneß_dependencies
  filename = "${path.module}/../tmp/lambda_two.zip"
  function_name = "lambda_handler2"
  role          = aws_iam_role.lambda_two_role.arn
  handler       = "lambda_two.lambda_handler2"
  runtime = "python3.9"
  timeout = 600
  # layers = [aws_lambda_layer_version.lambda_two_dependencies.arn, "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python39:16"]
}

resource "aws_lambda_permission" "allow_s3" {
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.s3_processor.function_name
  principal = "s3.amazonaws.com"
  source_arn = aws_s3_bucket.ingestion_bucket.arn
  source_account = data.aws_caller_identity.current.account_id
}