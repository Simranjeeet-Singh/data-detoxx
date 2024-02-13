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

    actions   = [
      "s3:ListBucket"
    ]
    resources = [
      "arn:aws:s3:::${var.ingestion_storage}"
    ]
  }

  statement {
    sid    = "AllObjectActions"
    effect = "Allow"

    actions   = [
      "s3:*Object"
    ]
    resources = [
      "arn:aws:s3:::${var.ingestion_storage}/*"
    ]
  }
}