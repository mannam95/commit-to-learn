# DynamoDB Terraform Module
dynamodb_table_name = "Your DynamoDB Table Name"
dynamodb_table_billing_mode = "Your DynamoDB Table Billing Mode, such as PROVISIONED or PAY_PER_REQUEST"
dynamodb_table_tags = {
  "Name" = "Your DynamoDB Table Name"
  Environment = "Your DynamoDB Table Environment"
}
dynamodb_table_read_capacity_minimum = 1
dynamodb_table_read_capacity_maximum = 5
dynamodb_table_read_capacity_target = 1
dynamodb_table_write_capacity_minimum = 1
dynamodb_table_write_capacity_maximum = 5
dynamodb_table_write_capacity_target = 1

# Lambda Module
lambda_execution_role_name = "Your Lambda Execution Role Name"
lambda_function_name = "Your Lambda Function Name"

# API Gateway Module
my_api_gateway_rest_api_name = "Your API Gateway Rest API Name"