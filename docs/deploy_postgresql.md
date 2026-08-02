# Publicação em VPS com Docker, PostgreSQL e HTTPS

> Para a VPS Hostinger instalada com Coolify, use `deploy_coolify.md`. Este
> documento permanece como alternativa para servidores Docker autogerenciados.

Esta é a referência operacional do ambiente de produção. O Compose sobe três
serviços: Caddy nas portas públicas 80/443, a aplicação Flask na rede interna e
PostgreSQL sem porta pública. O certificado TLS é emitido e renovado pelo Caddy.

## Pré-requisitos

- VPS Ubuntu/Debian com pelo menos 2 GB de RAM;
- Docker Engine com o plugin `docker compose`;
- portas TCP 22, 80 e 443 liberadas (e UDP 443, recomendado);
- registro DNS `A` do domínio apontando para o IPv4 da VPS;
- acesso SSH por chave e usuário com `sudo`.

Não publique a porta 5432 e não reutilize senhas do sistema no PostgreSQL.

## 1. Preparar o servidor

Instale Docker conforme a documentação oficial da distribuição. Depois clone o
repositório, entre na pasta e crie o arquivo de ambiente:

```bash
cp .env.vps.example .env.vps
chmod 600 .env.vps
openssl rand -hex 32
openssl rand -base64 36
```

Use as duas saídas, respectivamente, em `SECRET_KEY` e `POSTGRES_PASSWORD`.
Defina `DOMAIN` com o hostname já configurado no DNS. O arquivo `.env.vps` não
deve ser commitado.

## 2. Preservar os dados de origem

Antes da transferência, pare gravações na aplicação antiga e copie para uma
área segura:

- `apps/db.sqlite3`;
- `apps/static/images/`, incluindo avatares e imagens do carrossel;
- uma cópia externa desses arquivos para permitir rollback.

Transfira o repositório e esses dados com `rsync` ou `scp`. Não sobrescreva a
pasta de imagens da VPS depois que a nova aplicação começar a receber uploads.

## 3. Primeira publicação

Todos os comandos Compose deste documento usam explicitamente o arquivo da VPS:

```bash
docker compose --env-file .env.vps build app
docker compose --env-file .env.vps up -d postgres
docker compose --env-file .env.vps run --rm app flask db upgrade
```

Se existem dados no SQLite antigo, importe-os antes de liberar o site:

```bash
docker compose --env-file .env.vps run --rm \
  -v /caminho/absoluto/db.sqlite3:/tmp/origem.sqlite3:ro \
  app python scripts/migrate_sqlite_to_postgres.py --source /tmp/origem.sqlite3
```

O importador recusa executar se as tabelas de destino já contiverem registros.
Ele não apaga nem atualiza registros existentes.

Por fim, suba todos os serviços:

```bash
docker compose --env-file .env.vps up -d
docker compose --env-file .env.vps ps
docker compose --env-file .env.vps logs --tail=100 app caddy
curl --fail https://SEU_DOMINIO/health
```

Valide também login, troca de senha, permissões, carrossel e upload de avatar.

## 4. Atualizar uma versão

Antes de cada atualização, faça o backup descrito abaixo. Depois de baixar a
versão aprovada:

```bash
docker compose --env-file .env.vps build app
docker compose --env-file .env.vps run --rm app flask db upgrade
docker compose --env-file .env.vps up -d --no-deps app
docker compose --env-file .env.vps ps
curl --fail https://SEU_DOMINIO/health
```

As migrações rodam como tarefa única, nunca simultaneamente em várias réplicas.

## 5. Backup e restauração

Crie uma pasta fora do repositório e restrinja seu acesso. Exemplo de backup:

```bash
mkdir -p "$HOME/rastrek-backups"
docker compose --env-file .env.vps exec -T postgres \
  pg_dump -U gps_paraiba -d gps_paraiba -Fc \
  > "$HOME/rastrek-backups/postgres-$(date +%F-%H%M).dump"
tar -C apps/static -czf \
  "$HOME/rastrek-backups/images-$(date +%F-%H%M).tar.gz" images
```

Se `POSTGRES_USER` ou `POSTGRES_DB` foram alterados, ajuste o comando. Copie os
backups periodicamente para outro provedor/servidor e teste uma restauração. O
arquivo `.env.vps` deve ter cópia segura separada.

Restauração do banco em uma janela de manutenção:

```bash
docker compose --env-file .env.vps stop app
docker compose --env-file .env.vps exec -T postgres \
  pg_restore -U gps_paraiba -d gps_paraiba --clean --if-exists \
  < /caminho/backup.dump
docker compose --env-file .env.vps start app
```

## 6. Rollback

Para código sem migração destrutiva, volte ao commit/tag anterior, reconstrua a
imagem e suba somente `app`. Se a versão alterou o esquema de maneira
incompatível, restaure primeiro o dump correspondente e só então a versão
anterior. Nunca suponha que `flask db downgrade` substitui um backup validado.

## Checklist de corte

- DNS já aponta para a VPS e portas 80/443 respondem;
- `.env.vps` tem permissão 600, segredos únicos e `DEBUG=False`;
- dump do banco e arquivo das imagens foram copiados para fora da VPS;
- `flask db upgrade` e, se necessário, importação do SQLite concluíram;
- `/health`, login e uploads foram testados por HTTPS;
- rotina automatizada de backup e monitoramento de espaço em disco foi criada;
- aplicação antiga permanece disponível para rollback até a homologação final.
