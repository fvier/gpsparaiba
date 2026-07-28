# 🏗️ Ajuda & Infraestrutura (Rastrek)

Visão geral da infraestrutura, arquitetura de diretórios e comandos rápidos para manutenção da plataforma **Rastrek**.

---

## 1. Arquitetura de Servidores

- **Servidor Web (WSGI)**: Gunicorn (`gunicorn-cfg.py`) executando a aplicação Flask.
- **Banco de Dados**: SQLite (Desenvolvimento) / PostgreSQL (Produção).
- **Frontend**: Bootstrap 5 + ApexCharts para dashboards + Iconify.

---

## 2. Comandos Rápidos de Infraestrutura

```bash
# Executar em modo desenvolvimento:
python3 run.py

# Executar com Gunicorn (Produção):
gunicorn --config gunicorn-cfg.py run:app

# Verificar compilação de código:
python3 -m py_compile run.py apps/__init__.py
```
