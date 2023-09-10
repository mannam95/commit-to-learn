# Description: Variables for the DynamoDB table module.
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

# Description: Variables for the Lambda module.
variable "lambda_execution_role_name" {
  description = "Required. Name of the Lambda execution role."
  type        = string
}

variable "iam_policy_name" {
  description = "Required. Name of the IAM policy."
  type        = string
}

variable "lambda_function_name" {
  description = "Required. Name of the Lambda function."
  type        = string
}

# Description: Variables for the API Gateway module.
variable "my_api_gateway_rest_api_name" {
  description = "Required. Name of the API Gateway."
  type        = string
}

variable "my_api_gateway_stage_name" {
  description = "Name of the API Gateway stage"
  type        = string
}