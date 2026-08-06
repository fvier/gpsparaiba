# 📘 ESTUDO TÉCNICO E DOCUMENTAÇÃO DE DESENVOLVIMENTO — GPS PARAÍBA ERP

**Projeto:** Sistema ERP Comercial, Financeiro e Gestão de Vendas  
**Autor / Engenharia:** Fernando Vier  
**Organização:** GPS Paraíba  
**Carga Horária Total Dedicada:** 220 Horas de Engenharia de Software  
**Data da Documentação:** Agosto de 2026  

---

## 1. INTRODUÇÃO E VISÃO GERAL DO SISTEMA

Este documento apresenta o **estudo técnico detalhado** das horas, arquitetura, módulos e tecnologias utilizadas no desenvolvimento sob medida do **GPS Paraíba ERP**.

Diferente de softwares genéricos de prateleira, o sistema foi construído especificamente para atender à operação de rastreamento veicular da GPS Paraíba. Ele unifica em uma única plataforma web a gestão financeira multiempresa, a operação comercial de vendas e comissionamento, o gerenciamento de conteúdo da marca (*Linktree* e Landing Page), a exportação avançada de relatórios institucionais (XLSX, CSV, PDF), o módulo de integrações e APIs REST, e a auditoria em tempo real das ações dos usuários.

---

## 2. DICIONÁRIO DE TECNOLOGIAS (EXPLICADO EM LINGUAGEM ACESSÍVEL)

Para que qualquer pessoa — mesmo sem conhecimento prévio em programação ou TI — compreenda a estrutura do sistema, apresentamos abaixo uma analogia simples para cada tecnologia utilizada:

### 🐍 Python & Flask (O Maestro / Motor do Sistema)
* **O que é em linguagem simples:** É a linguagem de programação e a estrutura interna que dita as regras do sistema.
* **Analogia:** Pense no Python com Flask como o **maestro de uma orquestra** ou o **gerente de um restaurante**. Quando um usuário clica em um botão na tela, o Flask recebe a mensagem, calcula o que deve ser feito (ex: somar comissões, salvar uma venda, verificar senhas) e entrega a resposta pronta.

### 🐘 PostgreSQL (O Cofre de Dados Digital)
* **O que é em linguagem simples:** É o banco de dados relacional onde todas as informações são salvas permanentemente.
* **Analogia:** Funciona como um **arquivo de aço à prova de fogo ultra organizado**. Cada pasta do arquivo (tabela) guarda informações específicas (como vendas, empresas, clientes, categorias financeiras e logs) de forma relacional, garantindo que nenhum dado se perca ou se corrompa.

### 🐳 Docker & Containers (As Caixas Organizadoras do Servidor)
* **O que é em linguagem simples:** É a tecnologia que empacota o sistema e suas dependências dentro de compartimentos isolados chamados "containers".
* **Analogia:** Imagine um **navio cargueiro cheio de contêineres de transporte**. Cada contêiner carrega tudo o que precisa para funcionar sem interferir nos outros. Se um programa precisar ser atualizado, ele é alterado dentro da sua própria caixa sem quebrar o restante do servidor.

### 🦄 Gunicorn (O Atendente de Alta Velocidade)
* **O que é em linguagem simples:** É o servidor de aplicação que atende aos pedidos dos navegadores e repassa para o Python.
* **Analogia:** É como um **balcão com vários atendentes rápidos num banco**. Quando muitos funcionários tentam acessar o sistema ao mesmo tempo, o Gunicorn distribui as requisições entre vários trabalhadores virtuais (*workers*) para que ninguém enfrente lentidão.

### 🚦 Traefik & SSL/HTTPS (O Segurança da Porta e o Cadeado de Proteção)
* **O que é em linguagem simples:** É o roteador de tráfego e o sistema de criptografia que protege a conexão entre o computador do usuário e o servidor na nuvem.
* **Analogia:** É o **segurança da portaria que verifica o crachá** e o **envelopamento blindado das cartas**. O certificado SSL (o cadeado verde na barra de navegação `https://`) garante que nenhuma senha ou dado financeiro possa ser lido por terceiros durante o trajeto pela internet.

### 🏥 Healthcheck & Auto-heal (O Médico Robô 24/7)
* **O que é em linguagem simples:** Um script de automação que realiza exames de saúde no sistema a cada 1 minuto.
* **Analogia:** É um **médico residente particular que mede o pulso e a respiração do servidor 24 horas por dia**. Se o sistema por algum motivo oscilar ou parar de responder, o robô percebe em segundos e faz o reinício automático (*Auto-heal*), restaurando o ar sem precisar de intervenção humana.

### 🎨 HTML5, CSS3, JavaScript & Bootstrap (A Fachada e o Painel Interativo)
* **O que é em linguagem simples:** As linguagens que constroem o visual, as cores, os botões e os efeitos interativos da tela.
* **Analogia:** Se o sistema fosse um carro, o HTML5 seria a **estrutura de metal/chassi**, o CSS3 seria a **pintura, estofamento e acabamento**, e o JavaScript seria o **painel digital com botões interativos**. O Bootstrap é um kit de ferramentas de design moderno que faz o carro ficar bonito em qualquer tamanho de tela (computador, tablet ou celular).

### 🔄 Git & GitHub (A Máquina do Tempo do Código)
* **O que é em linguagem simples:** O sistema de controle de versão que registra cada mudança feita no código-fonte.
* **Analogia:** Funciona como um **livro de registro com opção de desfazer e refazer**. Se uma alteração for feita hoje, fica registrado exatamente quem alterou, que horas alterou e o que mudou, permitindo voltar no tempo caso necessário.

---

## 3. TABELA DE TEMPO DEDICADO E MÓDULOS DO PROJETO

O desenvolvimento do sistema foi dividido em **8 módulos principais**, totalizando **220 horas** de trabalho especializado:

| Módulo do Sistema | Carga Horária | Percentual | Descrição Sintética |
| :--- | :---: | :---: | :--- |
| **1. Gestão Financeira Multiempresa & Categorização** | 40 h | 18,2% | Estrutura de lançamentos, empresas (*GPS Paraíba*, *Casa*), categorias/subcategorias com contadores e filtros dinâmicos de período, mês e ano. |
| **2. Gestão de Vendas, Comissões, Instalações & Validação** | 30 h | 13,6% | Registro de vendas, checkbox de instalação, transferência de vendedor, cálculo de comissões, ranking e módulo de validação/bloqueio. |
| **3. Módulo Comercial, Linktree & Integração Landing Page** | 25 h | 11,4% | Gestão de planos da landing page, motor e página pública do Linktree (`/links`), prévia ao vivo em *iframe* e gerenciador de carrossel. |
| **4. Arquitetura, Segurança & Logs de Auditoria** | 20 h | 9,1% | Autenticação, controle de permissões por perfil, histórico completo de auditoria (`/admin-logs`), alternador visual de senha e segurança. |
| **5. Infraestrutura VPS, Docker & Healthcheck 24/7** | 20 h | 9,1% | Servidor na nuvem, banco PostgreSQL, containers Docker isolados, Gunicorn otimizado, SSL, monitoramento e robô Auto-heal. |
| **6. Exportação Avançada (XLSX, CSV & PDF Institucional)** | 30 h | 13,6% | Gerador de documentos Excel, CSV numéricos puros e relatórios PDF institucionais com cabeçalho/rodapé dinâmicos e carimbo de auditoria. |
| **7. Módulo de API REST, Integrações & Guia para Devs** | 25 h | 11,4% | Painel de integrações com Tema Escuro, endpoints RESTful seguros, autenticação por Bearer Token, guia interativo e suporte ao Postman. |
| **8. Personalização Sob Medida, Ajustes & Retrabalho** | 30 h | 13,6% | Readequação de layout ao fluxo da empresa, criação de regras exclusivas, melhorias de usabilidade baseadas em feedback real da equipe. |
| **TOTAL DEDICADO** | **220 h** | **100%** | **Engenharia de Software Completa (Full-Stack + DevOps)** |

---

## 4. DETALHAMENTO TÉCNICO DE CADA MÓDULO

### 🔹 Módulo 1: Gestão Financeira Multiempresa & Categorização (40 Horas)
* **Controle Multiempreisa:** Implementação da entidade `FinancialCompany` permitindo categorizar lançamentos entre unidades (*GPS Paraíba*, *Casa*).
* **Lançamentos Dinâmicos:** Cálculo de status em tempo real (*Pendente, Pago, Cancelado, Vencido, Perto de Vencer*) com base na data de vencimento e data atual.
* **Árvore de Categorias:** Suporte a categorias pai e subcategorias filhas. Exibição de *badges* contadores mostrando quantos lançamentos pertencem a cada categoria.
* **Proteção contra Exclusão:** Bloqueio de exclusão para categorias que possuem lançamentos vinculados, sugerindo a desativação para manter a integridade fiscal.
* **Sistema de Filtros Complexos:**
  - Filtro por período em dias corridos (7, 15, 30, 60, 90, 180, 365 dias);
  - Seleção por Mês e Ano dinâmico (calculado direto do banco de dados, sem exibir anos futuros sem lançamentos);
  - Seleção personalizada de intervalo de datas (`start_date` / `end_date`);
  - Preservação da URL de origem (`request.referrer`) para impedir que a página perca os filtros selecionados ao realizar alterações inline.

### 🔹 Módulo 2: Gestão de Vendas, Comissões, Instalações & Validação (30 Horas)
* **Fluxo de Contratos:** Cadastro de novas vendas vinculando cliente, contato, dados do veículo, placa e plano contratado.
* **Recurso de Instalação (`Com Instalação`):** Adição de campo tipo *checkbox* presente na tela de cadastro, no modal de edição e na área expandida de detalhes da tabela.
* **Transferência de Vendedor:** Opção de atribuir a comissão de uma venda para outro colaborador da equipe.
* **Módulo de Validação (`/validacao-vendas`):** Sistema de conferência em duas etapas. Vendas validadas são travadas permanentemente contra edição ou alteração de status por segurança operacional.
* **Mapeamento de Ranking:** Motor de cálculo e ranking dos vendedores de acordo com o volume de contratos ativados.

### 🔹 Módulo 3: Módulo Comercial, Linktree & Integração (25 Horas)
* **Gestão de Planos:** Controle de planos comerciais exibidos na página inicial pública da GPS Paraíba.
* **Página do Linktree Público (`/links`):** Interface otimizada para dispositivos móveis com links para redes sociais, atendimento e serviços.
* **Painel de Administração do Linktree (`/planos`):**
  - Edição de títulos, descrições, ícones da biblioteca Remix Icon, URLs e cores em formato HEX/HSL;
  - Prévia interativa em tempo real (*iframe*) dentro do painel administrativo;
  - Reordenação dinâmica de links.
* **Destaques de Interface:** Inclusão de botão destacado de acesso ao Linktree no topo da barra de navegação (*topbar*) do ERP.

### 🔹 Módulo 4: Arquitetura, Segurança & Logs de Auditoria (20 Horas)
* **Sistema de Permissões:** Níveis de acesso diferenciados (*Administrador, Gerente e Colaborador*).
* **Módulo de Auditoria (`/admin-logs`):** Registro automático de ações no sistema (criação de empresa, alteração de lançamento, login, reset de senha).
  - Exibição em tabela com limite de visualização por usuário e cards com totais de atividades.
* **Segurança de Acesso:**
  - Botão com ícone de olho (`ri-eye-line` / `ri-eye-off-line`) para alternar a exibição da senha digitada nas telas de login e alteração de senha;
  - Redirecionamento obrigatório de troca de senha no primeiro acesso para senhas temporárias.

### 🔹 Módulo 5: Infraestrutura VPS, Docker, Resiliência & Healthcheck 24/7 (20 Horas)
* **Containerização na Nuvem:** Construção de ambiente isolado na plataforma VPS utilizando Docker Compose.
* **Banco PostgreSQL:** Instalação e manutenção do banco de dados relacional com execução de comandos `ALTER TABLE` seguros para evolução de esquema.
* **Gunicorn & Performance:** Ajuste fino e dimensionamento de workers e threads para concorrência de requisições.
* **Automação Healthcheck & Auto-heal:** Script rodando em plano de fundo a cada 60 segundos na VPS com blindagem de proxy contra quedas para alta disponibilidade.

### 🔹 Módulo 6: Exportação Avançada de Relatórios & Documentos (XLSX, CSV, PDF) (30 Horas)
* **Exportador Excel / CSV:** Geração de relatórios em XLSX e CSV com suporte a vírgula brasileira e números puros para cálculos no Excel.
* **PDF Institucional jsPDF / autoTable:** Gerador de relatórios PDF com cabeçalho institucional, logo oficial da GPS Paraíba e dados de contato em 100% das páginas.
* **Rodapé com Auditoria:** Numeração automática de páginas e carimbo de segurança (data, hora, min, seg e usuário solicitante).
* **Controle de Layout:** Quebra de página sem corte de linhas de tabelas e totalizadores destacados.

### 🔹 Módulo 7: Módulo de API REST, Integrações & Guia para Devs (25 Horas)
* **Painel de Integrações (/admin-integracoes):** Interface em abas com suporte a Tema Escuro (Dark Mode).
* **Endpoints RESTful & Token:** APIs REST para Vendas e Lançamentos com autenticação via Bearer Token (RFC 6750) e gerador de token.
* **Documentação & Postman:** Guia interativo com parâmetros GET, atalhos de data e coleção estruturada para testes no Postman.

### 🔹 Módulo 8: Personalização Sob Medida, Ajustes & Retrabalho (30 Horas)
* **Desenvolvimento Orientado a Feedback:** Tempo dedicado a ajustar o comportamento do sistema após testes práticos da equipe.
* **Ajustes Realizados:**
  - Reformatação de seletores de tabela para evitar recarregamento bruto da tela;
  - Adequação visual das tabelas para evitar ocultação acidental de colunas essenciais (como a coluna Empresa);
  - Refinamento de usabilidade, formulários e modos visuais do ERP.

---

## 5. CONCLUSÃO E ESTADO ATUAL DO PROJETO

O projeto encontra-se **100% desenvolvido, homologado e implantado em ambiente de produção** na VPS dedicada da empresa sob o domínio oficial **`https://gpsparaiba.com.br`**.

A arquitetura implantada garante escalabilidade para adição de novos módulos futuros, segurança no armazenamento dos registros financeiros e operacionais, e autonomia completa para a equipe da GPS Paraíba gerenciar suas operações comerciais diárias.
