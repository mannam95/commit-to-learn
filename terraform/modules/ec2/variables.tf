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