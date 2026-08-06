# Mapeamento de Pendências & Issues de Desenvolvimento — GPS Paraíba

Este documento consolida as pendências técnicas mapeadas para futuras iterações do sistema GPS Paraíba.

---

## 📌 ISSUE-001: Ajuste Fino na Paginação e Repetição de Cabeçalho/Rodapé no PDF

- **Status**: `Mapeado / Agendado para Ajuste Futuro`
- **Módulos Afetados**:
  - `apps/templates/pages/financeiro-lancamentos.html`
  - `apps/templates/pages/vendas.html`

### 📋 Descrição do Problema
Ao exportar relatórios financeiros ou de vendas contendo múltiplos registros que se estendem por várias páginas em formato PDF:
1. Deseja-se a garantia matemática de que nenhuma linha de tabela seja fatiada horizontalmente na transição entre páginas A4.
2. Deseja-se a repetição obrigatória do cabeçalho institucional (Logo, Dados de Contato da Empresa, Solicitante e Carimbo de Data/Hora/Segundo) e dos títulos de colunas no topo de todas as páginas da exportação.

### 🧪 Abordagens Testadas & Próximos Passos Recomendados
1. **Engine Client-Side Atual**: Foi integrada a biblioteca `jsPDF-AutoTable`.
2. **Alternativa Recomendada para o Próximo Ajuste (Server-Side)**:
   - Implementar rota dedicada no Flask (`POST /financeiro/lancamentos/export-pdf`) utilizando **ReportLab** ou **WeasyPrint** no backend Python.
   - **Vantagem**: A geração no backend Python tem controle nativo milimétrico de páginas (`canvas.drawString`, `Platypus SimpleDocTemplate` e `Table` com `repeatRows=1`), garantindo 100% de precisão de layout e renderização ultra rápida.

---

*Documento mantido e sincronizado no controle de versão Git do projeto GPS Paraíba.*
