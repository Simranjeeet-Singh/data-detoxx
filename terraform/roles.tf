#Creation of different roles 

#Create role for Lambda Function
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}
#lambda_2
data "aws_iam_policy_document" "assume_role_2" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}
#Attaching the Role for Lambda-one-Function
resource "aws_iam_role" "lambda_one_role" {
  name               = "lambda-one-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}
#Attaching the Role for Lambda-two-Function
resource "aws_iam_role" "lambda_two_role" {
  name               = "lambda-two-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role_2.json
}
#Policy attached to lambda-one role
resource "aws_iam_role_policy_attachment" "lambda-policy-attach" {
  role       = aws_iam_role.lambda_one_role.name
  policy_arn = aws_iam_policy.s3_rw_policy.arn
}
#Policy attached to lambda-two role
resource "aws_iam_role_policy_attachment" "lambda2-policy-attach" {
  role       = aws_iam_role.lambda_two_role.name
  policy_arn = aws_iam_policy.s3_rw_policy_processed.arn
}



