
# Create a security group
resource "aws_security_group" "ssh_ec2" {
  name        = var.aws_security_group_ssh_ec2_name
  description = "SSH Security group for EC2"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "http_ec2" {
  name        = var.aws_security_group_http_ec2_name
  description = "Http Security group for EC2"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "example" {
  ami = var.aws_instance_ami

  instance_type = var.aws_instance_type

  key_name = var.aws_instance_key_name

  vpc_security_group_ids = [aws_security_group.ssh_ec2.id, aws_security_group.http_ec2.id]

  tags = var.aws_instance_tags
}
