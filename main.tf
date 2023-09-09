module "dynamodb" {
  source = "./dynamodb"
}

module "lambda" {
  source = "./lambda"
  basic_dynamodb_table_arn = module.dynamodb.basic_dynamodb_table_arn
}