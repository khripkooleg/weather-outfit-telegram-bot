resource "aws_key_pair" "tg_key" {
  key_name   = "tg_key_pair"
  public_key = file(var.ssh_public_key)
}

resource "aws_instance" "tg_ec2" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.tg_sub_public.id
  vpc_security_group_ids = [aws_security_group.tg_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2_ecr_profile.name
  key_name               = aws_key_pair.tg_key.key_name

  root_block_device {
    volume_size           = 40
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }
}
