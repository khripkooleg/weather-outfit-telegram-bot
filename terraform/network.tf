resource "aws_vpc" "tg_vpc" {
  cidr_block           = var.vpc_cidr
  instance_tenancy     = "default"
  enable_dns_support   = true
  enable_dns_hostnames = true
}

resource "aws_internet_gateway" "tg_igw" {
  vpc_id = aws_vpc.tg_vpc.id
}

resource "aws_subnet" "tg_sub_public" {
  vpc_id                  = aws_vpc.tg_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "tg_sub_private" {
  vpc_id            = aws_vpc.tg_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "${var.aws_region}a"
}

resource "aws_route_table" "tg_rt" {
  vpc_id = aws_vpc.tg_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.tg_igw.id
  }
}

resource "aws_route_table_association" "tg_rt_assoc" {
  subnet_id      = aws_subnet.tg_sub_public.id
  route_table_id = aws_route_table.tg_rt.id
}

resource "aws_security_group" "tg_sg" {
  name        = "Telegram Bot Security Group Ports"
  description = "List of Rules for Telegram Bot"
  vpc_id      = aws_vpc.tg_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.trusted_ip]
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
