provider "aws" {
  region = "eu-north-1"
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  version = "~> 2.0"
}

resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "DynamoDB-Terraform"
  billing_mode   = "PROVISIONED"
  read_capacity  = 12
  write_capacity = 12
  hash_key       = "RecordId"

  attribute {
    name = "RecordId"
    type = "S"
  }

  tags = {
    Name        = "dynamodb-table-dev"
    Environment = "Dev"
  }
}