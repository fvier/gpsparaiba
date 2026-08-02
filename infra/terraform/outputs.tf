output "vps_id" {
  description = "ID interno da VPS na Hostinger."
  value       = hostinger_vps.rastrek.id
}

output "vps_ipv4" {
  description = "IPv4 confirmado pelo provider."
  value       = hostinger_vps.rastrek.ipv4_address
}

output "ssh_command" {
  description = "Comando de acesso atual; depois deve ser trocado por usuário sem root."
  value       = "ssh root@${hostinger_vps.rastrek.ipv4_address}"
}
