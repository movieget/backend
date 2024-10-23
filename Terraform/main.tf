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

# 사용 가능한 가용 영역 조회
data "aws_availability_zones" "available" {
  state = "available"
}

# Create a Subnet
resource "aws_subnet" "FastAPI" {
  vpc_id                  = aws_vpc.MovieVPC.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = data.aws_availability_zones.available.names[0]
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

  ingress {
    description = "HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
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

# Generate SSH Key Pair for Gateway_Server
resource "tls_private_key" "Gateway_Server" {
  algorithm   = "RSA"
  rsa_bits    = 4096
}

resource "aws_key_pair" "Gateway_Server_pair" {
  key_name   = "Gateway_Server_pair"
  public_key = tls_private_key.Gateway_Server.public_key_openssh
}

# Generate SSH Key Pair for Backend_Server
resource "tls_private_key" "Backend_Server_key" {
  algorithm   = "RSA"
  rsa_bits    = 4096
}

resource "aws_key_pair" "Backend_Server_key_pair" {
  key_name   = "Backend_Server_key_pair"
  public_key = tls_private_key.Backend_Server_key.public_key_openssh
}

# ${path.module}는 프로젝트의 루트 디렉토리
resource "local_file" "Gateway_Server_private_key" {
  content  = tls_private_key.Gateway_Server.private_key_pem
  filename = "${path.module}/Gateway_Server_private_key.pem"
  file_permission = "0600"
}

resource "local_file" "Backend_Server_private_key" {
  content  = tls_private_key.Backend_Server_key.private_key_pem
  filename = "${path.module}/Backend_Server_private_key.pem"
  file_permission = "0600"
}

# Create two EC2 Instances
resource "aws_instance" "Gateway_Server" {
  ami                         = "ami-096099377d8850a97"
  instance_type               = "t4g.small"
  vpc_security_group_ids      = [aws_security_group.FastAPISG.id]
  subnet_id                   = aws_subnet.FastAPI.id
  associate_public_ip_address = true
  key_name                    = aws_key_pair.Gateway_Server_pair.key_name

  tags = {
    Name = "Gateway_Server"
  }
}

resource "aws_instance" "Backend_Server" {
  ami                         = "ami-096099377d8850a97"
  instance_type               = "t4g.small"
  vpc_security_group_ids      = [aws_security_group.FastAPISG.id]
  subnet_id                   = aws_subnet.FastAPI.id
  associate_public_ip_address = true
  key_name                    = aws_key_pair.Backend_Server_key_pair.key_name

  tags = {
    Name = "Backend_Server"
  }
}

output "Gateway_Server_id" {
  value = aws_instance.Gateway_Server.id
}

output "Gateway_Server_public_ip" {
  value = aws_instance.Gateway_Server.public_ip
}

output "Backend_Server_id" {
  value = aws_instance.Backend_Server.id
}

output "Backend_Server_public_ip" {
  value = aws_instance.Backend_Server.public_ip
}

output "Gateway_Server_public_key" {
  value     = tls_private_key.Gateway_Server.public_key_openssh
  sensitive = true
}

output "Backend_Server_public_key" {
  value     = tls_private_key.Backend_Server_key.public_key_openssh
  sensitive = true
}

output "Gateway_Server_private_key_path" {
  value = local_file.Gateway_Server_private_key.filename
}

output "Backend_Server_private_key_path" {
  value = local_file.Backend_Server_private_key.filename
}
