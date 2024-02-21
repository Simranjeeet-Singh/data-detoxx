resource "aws_s3_bucket" "ingestion_bucket" {
  bucket = "${var.ingestion_storage}"
}

resource "aws_s3_bucket" "processed_bucket" {
  bucket = "${var.processed_storage}"
}