resource "aws_lambda_function" "s3_file_reader" {
  filename = "${path.module}/../lambda_one.zip"
  function_name = "lambda_handler"
  role          = aws_iam_role.lambda_one_role.arn
  handler       = "lambda_one.lambda_handler"
  runtime = "python3.9"
}

