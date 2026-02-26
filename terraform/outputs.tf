output "public_ip" {
  description = "The public IP of the Airlines application server"
  value       = aws_instance.app_server.public_ip
}

output "website_url" {
  description = "The URL to access the Airlines application"
  value       = "http://${aws_instance.app_server.public_dns}"
}
