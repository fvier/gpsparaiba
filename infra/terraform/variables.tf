variable "vps_plan" {
  description = "Plano retornado pelo import da VPS existente."
  type        = string
}

variable "data_center_id" {
  description = "ID do datacenter retornado pelo import."
  type        = number
}

variable "template_id" {
  description = "ID do template de sistema operacional retornado pelo import."
  type        = number
}

variable "hostname" {
  description = "Hostname da VPS existente."
  type        = string
}

variable "expected_ipv4" {
  description = "Proteção para confirmar que o import aponta para a VPS correta."
  type        = string
  default     = "147.79.110.132"
}

variable "dns_zone" {
  description = "Zona DNS hospedada na Hostinger; vazio não cria registro."
  type        = string
  default     = ""
}

variable "dns_name" {
  description = "Nome relativo do registro A, como app ou @."
  type        = string
  default     = "app"
}
