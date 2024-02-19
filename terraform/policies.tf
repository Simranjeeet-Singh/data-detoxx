#Policies

#Read and Write Policy attached with permissions
resource "aws_iam_policy" "s3_rw_policy" {
  name        = "s3-rw-policy-${var.ingestion_storage}"
  description = "Read,Write premissions for lambda"
  policy      = data.aws_iam_policy_document.s3_rw_policy.json
}


#Read and Write permission statements for data-detox s3 bucket
data "aws_iam_policy_document" "s3_rw_policy" {
  version = "2012-10-17"

  statement {
    sid    = "ListObjectsInBucket"
    effect = "Allow"

    actions = [
      "s3:ListBucket"
    ]
    resources = [
      "arn:aws:s3:::${var.ingestion_storage}"
    ]
  }

  statement {
    sid    = "AllObjectActions"
    effect = "Allow"

    actions = [
      "s3:*Object"
    ]
    resources = [
      "arn:aws:s3:::${var.ingestion_storage}/*"
    ]
  }
}

# Create Cloudwatch log group
resource "aws_cloudwatch_log_group" "cw_log_group" {
  name = "/aws/lambda/${aws_lambda_function.s3_file_reader.function_name}"
  #   "/aws/lambda/${aws_lambda_function.demo_lambda.function_name}"
}

# Create Cloudwatch logging policy
resource "aws_iam_policy" "function_logging_policy" {
  name = "function-logging-policy"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        Action : [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Effect : "Allow",
        Resource : "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# Attach Cloudwatch logging policy to Lambda role
resource "aws_iam_role_policy_attachment" "function_logging_policy_attachment" {
  depends_on = [aws_lambda_function.s3_file_reader]
  role       = aws_iam_role.lambda_one_role.id
  policy_arn = aws_iam_policy.function_logging_policy.arn
}



# ----------------------------------------------------------------
resource "aws_iam_policy" "lambda_secrets_policy" {
  name        = "lambda_secrets_policy"
  description = "Policy for Lambda to access Secrets Manager"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        "Effect" : "Allow",
        "Principal" : {
          "AWS" : "arn:aws:iam::AccountId:role/LamdaRoleToAccessSecrets"
        },
        "Action" : "secretsmanager:GetSecretValue",
        "Resource" : "arn:aws:secretsmanager:Region:AccountId:secret:SecretName-123123"
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "lambda_secrets_policy_attachment" {
  name       = "lambda_secrets_policy_attachment"
  policy_arn = aws_iam_policy.lambda_secrets_policy.arn
  roles      = [aws_iam_role.lambda_one_role.id]
}
# resource "aws_iam_role_policy_attachment" "lambda-policy-attach" {
#   role       = aws_iam_role.lambda_one_role.name
#   policy_arn = [aws_iam_policy.s3_rw_policy.arn]
# }
