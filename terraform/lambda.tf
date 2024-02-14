resource "aws_lambda_function" "s3_file_reader" {
  depends_on = [data.archive_file.lambda_zip]
  filename = "${path.module}/../lambda_one.zip"
  function_name = "lambda_handler"
  role          = aws_iam_role.lambda_one_role.arn
  handler       = "lambda_one.lambda_handler"
  runtime = "python3.9"
  timeout=600
}

