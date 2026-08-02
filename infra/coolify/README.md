# Inventário Terraform do Coolify

Esta configuração consulta a API do Coolify em modo somente leitura. Ela não
cria, altera ou remove recursos porque contém apenas `data` sources.

No painel do Coolify, habilite a API em `Settings` e gere um token em
`Security > API Tokens`. Guarde as credenciais localmente em `.env.coolify`, na
raiz do repositório:

```bash
export COOLIFY_ENDPOINT='http://147.79.110.132:8000'
export COOLIFY_TOKEN='token-gerado-no-coolify'
```

Proteja o arquivo com permissão 600 e nunca o versione. Para coletar o
inventário:

```bash
set -a
source .env.coolify
set +a
terraform -chdir=infra/coolify init
terraform -chdir=infra/coolify plan -refresh-only
terraform -chdir=infra/coolify output
```

O resultado inclui saúde e versão do Coolify, servidores registrados, projetos,
aplicações, status/domínios/repositórios e deployments. Variáveis de ambiente e
segredos das aplicações não são exportados por este inventário.
