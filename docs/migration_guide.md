# 🚚 Guia de Migração & Onboarding (Rastrek)

Instruções para clonar, configurar e executar a aplicação **Rastrek** em novos servidores ou estações de desenvolvimento de colaboradores.

---

## 1. Pré-requisitos
- Python 3.10 ou superior
- Git e chave SSH cadastrada no GitHub
- Pip e venv

---

## 2. Passo a Passo de Setup

```bash
# 1. Clonar repositório
git clone git@github.com:fvier/rastreck.git
cd rastreck

# 2. Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Copiar variáveis de ambiente
cp env.sample .env

# 5. Executar em ambiente local
python3 run.py
```
