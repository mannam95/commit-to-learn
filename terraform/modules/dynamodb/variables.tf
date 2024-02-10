variable "dynamodb_table_name" {
  description = "Required. Name of the DynamoDB table."
  type        = string
}

variable "dynamodb_table_billing_mode" {
  description = "Required. Billing mode for the DynamoDB table."
  type        = string
}

variable "dynamodb_table_tags" {
  description = "Optional. Tags for the DynamoDB table."
  type        = map(any)
}

variable "dynamodb_table_read_capacity_minimum" {
  description = "Required. Minimum allowed autoscale range."
  type        = number
}

variable "dynamodb_table_read_capacity_maximum" {
  description = "Required. Maximum allowed autoscale range."
  type        = number
}

variable "dynamodb_table_read_capacity_target" {
  description = "Required. Target within autoscale range."
  type        = number
}

variable "dynamodb_table_write_capacity_minimum" {
  description = "Required. Minimum allowed autoscale range."
  type        = string
}

variable "dynamodb_table_write_capacity_maximum" {
  description = "Required. Maximum allowed autoscale range."
  type        = number
}

variable "dynamodb_table_write_capacity_target" {
  description = "Required. Target within autoscale range."
  type        = number
}