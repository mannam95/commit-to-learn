module "dynamodb" {
  source = "./dynamodb"
}

module "lambda" {
  source = "./lambda"
  basic_dynamodb_table_arn = module.dynamodb.basic_dynamodb_table_arn
}

module "api-gateway" {
  source = "./api-gateway"
  my_lambda_function_name = module.lambda.my_lambda_function_name
  my_lambda_function_arn = module.lambda.my_lambda_function_arn
}