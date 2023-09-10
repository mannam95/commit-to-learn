resource "aws_dynamodb_table" "basic_dynamodb_table" {
  name           = var.dynamodb_table_name
  billing_mode   = var.dynamodb_table_billing_mode
  read_capacity  = var.dynamodb_table_read_capacity_target
  write_capacity = var.dynamodb_table_write_capacity_target
  hash_key       = "RecordId"

  attribute {
    name = "RecordId"
    type = "S"
  }

  tags = var.dynamodb_table_tags
}

# create a read policy for autoscaling
resource "aws_appautoscaling_target" "dynamodb_table_read_target" {
  max_capacity       = var.dynamodb_table_read_capacity_maximum
  min_capacity       = var.dynamodb_table_read_capacity_minimum
  resource_id        = "table/${aws_dynamodb_table.basic_dynamodb_table.name}"
  scalable_dimension = "dynamodb:table:ReadCapacityUnits"
  service_namespace  = "dynamodb"
}

# create a write policy for autoscaling
resource "aws_appautoscaling_target" "dynamodb_table_write_target" {
  max_capacity       = var.dynamodb_table_write_capacity_maximum
  min_capacity       = var.dynamodb_table_write_capacity_minimum
  resource_id        = "table/${aws_dynamodb_table.basic_dynamodb_table.name}"
  scalable_dimension = "dynamodb:table:WriteCapacityUnits"
  service_namespace  = "dynamodb"
}

# Apply the read policy
resource "aws_appautoscaling_policy" "dynamodb_table_read_policy" {
  name               = "DynamoDBReadCapacityUtilization:${aws_appautoscaling_target.dynamodb_table_read_target.resource_id}"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.dynamodb_table_read_target.resource_id
  scalable_dimension = aws_appautoscaling_target.dynamodb_table_read_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.dynamodb_table_read_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "DynamoDBReadCapacityUtilization"
    }

    target_value = 65.0
  }
}

# Apply the write policy
resource "aws_appautoscaling_policy" "dynamodb_table_write_policy" {
  name               = "DynamoDBWriteCapacityUtilization:${aws_appautoscaling_target.dynamodb_table_write_target.resource_id}"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.dynamodb_table_write_target.resource_id
  scalable_dimension = aws_appautoscaling_target.dynamodb_table_write_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.dynamodb_table_write_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "DynamoDBWriteCapacityUtilization"
    }

    target_value = 60.0
  }
}

output "basic_dynamodb_table_arn" {
  value = aws_dynamodb_table.basic_dynamodb_table.arn
}