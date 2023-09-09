resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_dynamodb_policy" {
  name        = "DynamoDBWriteAccess"
  description = "Policy for Lambda to write to DynamoDB"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action   = "dynamodb:PutItem",
        Effect   = "Allow",
        Resource = var.basic_dynamodb_table_arn
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "lambda_dynamodb_policy_attachment" {
  name       = "lambda_dynamodb_policy_attachment"
  policy_arn = aws_iam_policy.lambda_dynamodb_policy.arn
  roles      = [aws_iam_role.lambda_execution_role.name]
}

resource "aws_lambda_function" "my_lambda_function" {
  function_name = "my-lambda-function"
  role         = aws_iam_role.lambda_execution_role.arn
  handler      = "index.handler"
  runtime      = "nodejs16.x"
  filename     = "dummy.zip"
  lifecycle {
    ignore_changes = [filename]
  }
}

output "my_lambda_function_name" {
  value = aws_lambda_function.my_lambda_function.function_name
}

output "my_lambda_function_arn" {
  value = aws_lambda_function.my_lambda_function.invoke_arn
}