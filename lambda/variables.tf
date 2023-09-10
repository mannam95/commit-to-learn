variable "lambda_execution_role_name" {
  description = "Name of the IAM role for the Lambda function"
}

variable "iam_policy_name" {
  description = "Name of the IAM policy for the Lambda function"
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
}

variable "basic_dynamodb_table_arn" {
  description = "ARN of the DynamoDB table to write to"
}