provider "aws" {
  region = "ap-northeast-2"
}

# Create a VPC
resource "aws_vpc" "MovieVPC" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "MovieVPC"
  }
}

# Create an Internet Gateway
resource "aws_internet_gateway" "movieIG" {
  vpc_id = aws_vpc.MovieVPC.id

  tags = {
    Name = "MovieInternetGateway"
  }
}

# Create a Subnet
resource "aws_subnet" "FastAPI" {
  vpc_id                  = aws_vpc.MovieVPC.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "FastAPISubnet"
  }
}

# 라우팅 테이블 생성
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.MovieVPC.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.movieIG.id
  }

  tags = {
    Name = "MoviePublicRouteTable"
  }
}

# 라우팅 테이블과 서브넷 연결
resource "aws_route_table_association" "public_rt_association" {
  subnet_id      = aws_subnet.FastAPI.id
  route_table_id = aws_route_table.public_rt.id
}

# Create a Security Group
resource "aws_security_group" "FastAPISG" {
  name        = "FastAPISecurityGroup"
  description = "Allow SSH and FastAPI"
  vpc_id      = aws_vpc.MovieVPC.id

  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "FastAPI from anywhere"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "FastAPISecurityGroup"
  }
}

# Create two EC2 Instances
resource "aws_instance" "FastAPI_1" {
  ami                         = "ami-096099377d8850a97"
  instance_type               = "t4g.small"
  vpc_security_group_ids      = [aws_security_group.FastAPISG.id]
  subnet_id                   = aws_subnet.FastAPI.id
  associate_public_ip_address = true

  tags = {
    Name = "FastAPI-Server-1"
  }
}

resource "aws_instance" "FastAPI_2" {
  ami                         = "ami-096099377d8850a97"
  instance_type               = "t4g.small"
  vpc_security_group_ids      = [aws_security_group.FastAPISG.id]
  subnet_id                   = aws_subnet.FastAPI.id
  associate_public_ip_address = true

  tags = {
    Name = "FastAPI-Server-2"
  }
}

output "instance_1_id" {
  value = aws_instance.FastAPI_1.id
}

output "instance_1_public_ip" {
  value = aws_instance.FastAPI_1.public_ip
}

output "instance_2_id" {
  value = aws_instance.FastAPI_2.id
}

output "instance_2_public_ip" {
  value = aws_instance.FastAPI_2.public_ip
}