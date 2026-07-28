# 🔍 Troubleshooting & Diagnóstico (Rastrek)

Guia rápido para resolução de problemas comuns na aplicação **Rastrek**.

> [!IMPORTANT]
> **Alimentação Incremental:** Nunca remova soluções antigas deste documento. Adicione novos problemas e soluções incrementalmente.

---

## 1. Problema: Error: Invalid `<config_mode>`

### Sintoma
A execução do `run.py` falha com mensagem `Error: Invalid <config_mode>`.

### Solução
Defina a variável `DEBUG` no arquivo `.env` ou no ambiente:
```bash
export DEBUG=True
python3 run.py
```

---

## 2. Problema: Módulos Não Encontrados (`ModuleNotFoundError`)

### Sintoma
`ModuleNotFoundError: No module named 'flask'` ou dependência ausente.

### Solução
Garantir que o ambiente virtual está ativado e as dependências instaladas:
```bash
source venv/bin/activate
pip install -r requirements.txt
```
