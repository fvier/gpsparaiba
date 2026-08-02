# Terraform da VPS Hostinger

Esta receita adota a VPS já existente no estado Terraform e, opcionalmente,
gerencia seu registro DNS. Ela não cria outra VPS e contém duas proteções:
`prevent_destroy` e a validação do IPv4 `147.79.110.132`.

O provider Hostinger identifica a máquina pelo ID interno, não pelo IP. Obtenha
um token no hPanel (Conta > API) e nunca o grave no repositório:

```bash
export HOSTINGER_API_TOKEN='seu-token-temporario'
curl --fail --silent --show-error \
  -H "Authorization: Bearer $HOSTINGER_API_TOKEN" \
  -H 'Content-Type: application/json' \
  https://developers.hostinger.com/api/vps/v1/virtual-machines
```

Na resposta, localize a máquina com IP `147.79.110.132` e copie seu ID. Depois:

```bash
cd infra/terraform
terraform init
cp terraform.tfvars.example terraform.tfvars
terraform import hostinger_vps.rastrek ID_INTERNO_DA_VPS
terraform state show hostinger_vps.rastrek
```

Copie `plan`, `data_center_id`, `template_id` e `hostname` mostrados no estado
para `terraform.tfvars`. Só então revise o plano:

```bash
terraform fmt -check
terraform validate
terraform plan
```

O primeiro plano aceitável deve indicar **zero alterações** na VPS. Se mostrar
substituição, cancelamento ou mudança de template, não aplique: corrija os
valores para coincidirem exatamente com o estado importado.

Para criar também um registro A, preencha `dns_zone` e `dns_name`. Isso só se
aplica quando os nameservers do domínio usam o DNS da Hostinger. O domínio
`gpsparaiba.com.br` usa `e.sec.dns.br` e `f.sec.dns.br`; portanto seus registros
continuam sendo gerenciados no Registro.br/NickBR e `dns_zone` deve ficar vazio.

## Limite desta receita

Terraform controla os recursos da conta Hostinger. Como essa VPS usa o sistema
Coolify, o deploy da aplicação segue `docs/deploy_coolify.md` e o arquivo
`docker-compose.coolify.yml`. O Coolify, e não o Terraform, controla containers,
proxy e certificados. Como a VPS já existe, associar um post-install script pode
reinstalar o sistema; por isso esse mecanismo não é usado aqui.

O estado Terraform contém metadados da infraestrutura. Guarde-o de forma
segura, não o versione e faça backup antes de qualquer alteração.
