# 🛠️ Estratégia de Execução & Fluxo Git (Rastrek)

Este documento define o fluxo de trabalho com o Git, padrões de commit, ramificação (branching) e critérios para contribuição e deploy no repositório **Rastrek**.

---

## 1. Padrão de Branches

| Branch | Finalidade | Regra de Merge |
| :--- | :--- | :--- |
| `main` | Código de produção estável e pronto para deploy | Exige Pull Request (PR) revisado |
| `feature/*` | Desenvolvimento de novas funcionalidades ou módulos de rastreamento | Merge na `main` via PR |
| `fix/*` | Correção de bugs ou falhas identificadas em homologação | Merge na `main` via PR |
| `docs/*` | Atualizações de governança, manuais e documentação | Merge direto ou via PR rápido |

---

## 2. Convenção de Commits (Conventional Commits)

Os commits devem seguir o padrão:
`<tipo>(<escopo>): <descrição curta em minúsculas>`

### Tipos Permitidos:
- `feat`: Nova funcionalidade (ex: `feat(telemetria): adiciona gráfico de velocidade em tempo real`)
- `fix`: Correção de bug (ex: `fix(auth): corrige validação do token JWT`)
- `docs`: Alterações na documentação (ex: `docs(readme): atualiza instruções de onboarding`)
- `ci`: Alterações nos workflows do GitHub Actions ou scripts de CI/CD
- `refactor`: Refatoração de código sem alterar regra de negócio
- `style`: Ajustes de formatação, CSS ou layout

---

## 3. Visualização do Git Graph no Terminal

Para visualizar a árvore de commits e branches no terminal:

```bash
git log --graph --oneline --all --decorate
```

Ou configure o alias permanente:
```bash
git config --global alias.graph "log --graph --oneline --all --decorate"
git graph
```
