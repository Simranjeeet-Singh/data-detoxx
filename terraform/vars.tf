variable "ingestion_storage" {
    type = string
    default = "data-detox-ingestion-bucket"
}

variable "processed_storage" {
    type = string
    default = "data-detox-processed-bucket"
}

variable "aws_pandas_layer_arn" {
    type = string
    default = "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python311:8"
}