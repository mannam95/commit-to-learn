variable "my_api_gateway_rest_api_name" {
  description = "Name of the API Gateway"
}

variable "my_lambda_function_name" {
  description = "Name of the Lambda function"
  default     = ""
}

variable "my_lambda_function_invoke_arn" {
  description = "ARN of the Lambda function"
  default     = ""
}

variable "my_api_gateway_stage_name" {
  description = "Name of the API Gateway stage"
  default     = ""
}