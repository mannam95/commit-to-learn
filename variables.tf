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

# Description: Variables for the EC2 module.
variable "aws_security_group_ssh_ec2_name" {
  description = "Name of the security group for SSH access to EC2"
  type        = string
}

variable "aws_security_group_http_ec2_name" {
  description = "Name of the security group for HTTP access to EC2"
  type        = string
}

variable "aws_instance_ami" {
  description = "AMI ID for the EC2 instance"
  type        = string
}

variable "aws_instance_type" {
  description = "Instance type for the EC2 instance"
  type        = string
}

variable "aws_instance_key_name" {
  description = "Key pair name for the EC2 instance"
  type        = string
}

variable "aws_instance_tags" {
  description = "Tags for the EC2 instance"
  type        = map(any)
}