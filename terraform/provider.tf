provider "aws" {
    region = "eu-west-2"
}

terraform {
    required_providers {
        aws= {
            source = "hashicorp/aws"
            version = "5.37.0"
        }
    }
    backend "s3" {
        bucket = "tfstate-ingestion-bucket"
        key = "tf-state"
        region = "eu-west-2"
    }
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}