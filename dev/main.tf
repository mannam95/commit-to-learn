module "dynamodb" {
  source = "../dynamodb"
  dynamodb_table_name = var.dynamodb_table_name
  dynamodb_table_billing_mode = var.dynamodb_table_billing_mode
  dynamodb_table_tags = var.dynamodb_table_tags
  dynamodb_table_read_capacity_minimum = var.dynamodb_table_read_capacity_minimum
  dynamodb_table_read_capacity_maximum = var.dynamodb_table_read_capacity_maximum
  dynamodb_table_read_capacity_target = var.dynamodb_table_read_capacity_target
  dynamodb_table_write_capacity_minimum = var.dynamodb_table_write_capacity_minimum
  dynamodb_table_write_capacity_maximum = var.dynamodb_table_write_capacity_maximum
  dynamodb_table_write_capacity_target = var.dynamodb_table_write_capacity_target
}

module "lambda" {
  source = "../lambda"
  lambda_execution_role_name = var.lambda_execution_role_name
  iam_policy_name = var.iam_policy_name
  lambda_function_name = var.lambda_function_name
  basic_dynamodb_table_arn = module.dynamodb.basic_dynamodb_table_arn
}

module "api-gateway" {
  source = "../api-gateway"
  my_api_gateway_rest_api_name = var.my_api_gateway_rest_api_name
  my_lambda_function_name = module.lambda.my_lambda_function_name
  my_lambda_function_invoke_arn = module.lambda.my_lambda_function_invoke_arn
}