resource "aws_dynamodb_table" "basic_dynamodb_table" {
  name         = var.dynamodb_table_name
  billing_mode = var.dynamodb_table_billing_mode
  # read_capacity  = var.dynamodb_table_read_capacity_target
  # write_capacity = var.dynamodb_table_write_capacity_target
  hash_key = "RecordId"

  attribute {
    name = "RecordId"
    type = "S"
  }

  tags = var.dynamodb_table_tags
}

output "basic_dynamodb_table_arn" {
  value = aws_dynamodb_table.basic_dynamodb_table.arn
}