resource "tls_private_key" "mongo_key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "aws_key_pair" "mongo_key" {
  key_name   = "mongo-key"
  public_key = tls_private_key.mongo_key.public_key_openssh
}
