resource "aws_lambda_function" "s3_file_reader" {
  depends_on = [data.archive_file.lambda_one_zip,aws_lambda_layer_version.lambda_one_dependencies]
  filename = "${path.module}/../tmp/lambda_one.zip"
  function_name = "lambda_handler"
  role          = aws_iam_role.lambda_one_role.arn
  handler       = "lambda_one.lambda_handler"
  source_code_hash = data.archive_file.lambda_one_zip.output_base64sha256
  runtime = "python3.11"
  timeout = 600
  layers = [aws_lambda_layer_version.lambda_one_dependencies.arn, aws_lambda_layer_version.lambda_utils.arn, var.aws_pandas_layer_arn]
}

resource "aws_lambda_function" "s3_processor" {
  depends_on = [data.archive_file.lambda_two_zip, aws_lambda_layer_version.lambda_two_dependencies]
  filename = "${path.module}/../tmp/lambda_two.zip"
  function_name = "lambda_handler2"
  role          = aws_iam_role.lambda_two_role.arn
  handler       = "lambda_two.lambda_handler2"
  source_code_hash = data.archive_file.lambda_two_zip.output_base64sha256
  runtime = "python3.11"
  timeout = 600
  layers = [aws_lambda_layer_version.lambda_two_dependencies.arn, aws_lambda_layer_version.lambda_utils.arn, var.aws_pandas_layer_arn]
}

resource "aws_lambda_function" "s3_uploader" {
  depends_on = [data.archive_file.lambda_three_zip] #, aws_lambda_layer_version.lambda_three_dependencies
  filename = "${path.module}/../tmp/lambda_three.zip"
  function_name = "lambda_handler3"
  role          = aws_iam_role.lambda_three_role.arn
  handler       = "lambda_three.lambda_handler3"
  source_code_hash = data.archive_file.lambda_three_zip.output_base64sha256
  runtime = "python3.11"
  timeout = 600
  # layers = [aws_lambda_layer_version.lambda_three_dependencies.arn, aws_lambda_layer_version.lambda_utils.arn, var.aws_pandas_layer_arn]
}

resource "aws_lambda_permission" "allow_s3" {
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.s3_processor.function_name
  principal = "s3.amazonaws.com"
  source_arn = aws_s3_bucket.ingestion_bucket.arn
  source_account = data.aws_caller_identity.current.account_id
}

resource "aws_lambda_permission" "allow_s32" {
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.s3_uploader.function_name
  principal = "s3.amazonaws.com"
  source_arn = aws_s3_bucket.processed_bucket.arn
  source_account = data.aws_caller_identity.current.account_id
}