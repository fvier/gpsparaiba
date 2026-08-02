resource "hostinger_vps" "rastrek" {
  # Esta configuração representa a VPS existente. Importe antes de aplicar.
  plan           = var.vps_plan
  data_center_id = var.data_center_id
  template_id    = var.template_id
  hostname       = var.hostname

  lifecycle {
    prevent_destroy = true

    postcondition {
      condition     = self.ipv4_address == var.expected_ipv4
      error_message = "A VPS importada não possui o IPv4 esperado. Não aplique alterações."
    }
  }
}

resource "hostinger_dns_record" "app" {
  count = var.dns_zone == "" ? 0 : 1

  zone  = var.dns_zone
  name  = var.dns_name
  type  = "A"
  value = var.expected_ipv4
  ttl   = 300
}
