# Deploy na Hostinger com Coolify

Neste ambiente, o Coolify gerencia proxy reverso, domínio, TLS, builds e logs.
Não suba o serviço Caddy de `docker-compose.yml`; use exclusivamente
`docker-compose.coolify.yml` como arquivo da aplicação no painel.

## Criar o recurso

1. No Coolify, crie um projeto e um ambiente `production`.
2. Adicione `Public Repository` com `https://github.com/fvier/gpsparaiba`.
3. Selecione a branch aprovada para produção.
4. Escolha o build pack `Docker Compose`.
5. Use `/` como diretório base.
6. Informe `/docker-compose.coolify.yml` como localização do Compose.
7. Associe `https://gpsparaiba.com.br:5000` ao serviço `app`. O sufixo `:5000`
   informa ao Coolify a porta interna; externamente o acesso permanece em 443.

Não publique portas no serviço `postgres`. Ele deve permanecer acessível apenas
na rede privada criada para esse stack.

## DNS oficial

O domínio principal é `gpsparaiba.com.br`. Em 2 de agosto de 2026, o registro A
público já resolvia para `147.79.110.132`. Os nameservers são
`e.sec.dns.br` e `f.sec.dns.br`, então o DNS não será gerenciado pelo provider
Terraform da Hostinger.

O host `www.gpsparaiba.com.br` ainda não possui registro. Se ele também for
usado, crie no painel DNS um CNAME `www` apontando para `gpsparaiba.com.br` e
adicione `https://www.gpsparaiba.com.br:5000` ao mesmo serviço no Coolify. Uma
alternativa é manter somente o domínio sem `www` e configurar redirecionamento.

Antes de associar a aplicação, o Traefik pode responder 404 e apresentar seu
certificado padrão. Depois de salvar o domínio e publicar o serviço, o Coolify
deve emitir o certificado válido automaticamente.

## Variáveis

O Compose usa as variáveis mágicas do Coolify para gerar e preservar dois
segredos:

- `SERVICE_HEX_64_RASTREK`: chave de sessão Flask;
- `SERVICE_PASSWORD_64_POSTGRES`: senha do PostgreSQL.

O painel também mostrará `POSTGRES_DB` e `POSTGRES_USER`, ambos opcionais e com
o padrão `gps_paraiba`. Marque segredos como runtime-only quando a versão do
Coolify oferecer essa opção. Não copie essas chaves para o Git.

No primeiro deploy de um banco vazio, defina também `INITIAL_ADMIN_EMAIL` e
`INITIAL_ADMIN_PASSWORD`. A aplicação cria o administrador exigindo troca de
senha no primeiro login. Depois de confirmar o acesso, remova as duas variáveis;
a aplicação nunca recria ou substitui um usuário existente.

## Banco e primeira publicação

O container da aplicação espera o PostgreSQL ficar saudável, executa
`flask db upgrade` uma vez a cada inicialização e só então inicia o Gunicorn.
Isso mantém o primeiro deploy reproduzível. Mantenha uma única instância do
serviço `app` enquanto as migrações forem executadas dessa forma.

Para importar o SQLite existente, primeiro publique o stack vazio. Depois abra
o terminal do serviço `app`, disponibilize temporariamente uma cópia do arquivo
e execute:

```bash
python scripts/migrate_sqlite_to_postgres.py --source /tmp/origem.sqlite3
```

O arquivo precisa estar dentro do container. Remova-o logo após a importação e
nunca o adicione ao repositório ou a uma imagem Docker.

## Persistência e backup

Os volumes `postgres_data` e `app_images` são persistentes e gerenciados pelo
stack. O segundo preserva imagens do carrossel, avatares e demais arquivos dessa
pasta entre builds.

Configure no Coolify backups externos do PostgreSQL. A pasta de imagens também
precisa de cópia externa periódica; backup apenas do banco não cobre uploads.
Antes de qualquer mudança de volume ou restauração, faça snapshot da VPS e
confirme o nome físico dos volumes no servidor.

## Validação depois do deploy

- serviço `postgres` saudável e sem porta pública;
- serviço `app` saudável;
- `https://gpsparaiba.com.br/health` retorna HTTP 200;
- login, permissões, upload de avatar e carrossel funcionam;
- certificado HTTPS está válido;
- redeploy preserva banco e imagens.

## Responsabilidades

- Terraform: adoção/proteção da VPS e DNS Hostinger;
- Coolify: aplicação, proxy, HTTPS, variáveis, logs e deploy;
- Docker Compose: topologia Flask/PostgreSQL e volumes;
- rotina operacional: backups externos e teste de restauração.
