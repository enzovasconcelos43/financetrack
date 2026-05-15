# 💰 FinanceTrack CLI

> Aplicação de linha de comando para **gestão financeira pessoal** com **cotações de moedas em tempo real** via [AwesomeAPI](https://docs.awesomeapi.com.br/).

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![CI](https://img.shields.io/github/actions/workflow/status/SEU_USUARIO/financetrack/ci.yml?label=CI)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-1.0.0-orange)

---

## 📋 Índice

- [Funcionalidades](#funcionalidades)
- [Demonstração](#demonstração)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Testes](#testes)
- [Deploy](#deploy)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Versionamento](#versionamento)

---

## ✨ Funcionalidades

| Módulo | Recursos |
|---|---|
| 📊 **Cotações** | Dólar, Euro, Bitcoin, Libra, Peso, Iene em tempo real |
| 🔄 **Conversão** | Converta valores de BRL para qualquer moeda |
| 💼 **Finanças** | Registre receitas e despesas com extrato completo |
| 💾 **Persistência** | Dados salvos localmente em `financas.json` |
| 🤖 **CI/CD** | Pipeline automático de lint e testes no GitHub Actions |

---

## 🖥️ Demonstração

```
══════════════════════════════════════════════════
  💰  FinanceTrack CLI  v1.0.0
  Gestão Financeira + Cotações em Tempo Real
══════════════════════════════════════════════════

  [1] 📊 Cotações de Moedas
  [2] 💼 Gestão Financeira
  [0] 🚪 Sair

  Digite sua opção: 1

📊  COTAÇÕES DE MOEDAS
──────────────────────────────
  [1] Dólar Americano → Real
  [2] Euro → Real
  ...
```

---

## 🛠️ Tecnologias

- **Python 3.11+** — Linguagem principal
- **Requests** — Consumo da API REST
- **Pytest** — Testes unitários e de integração
- **Ruff** — Linter e formatador de código
- **GitHub Actions** — Pipeline CI/CD automatizado
- **AwesomeAPI** — API pública de cotações de moedas

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.11 ou superior instalado
- Git instalado
- Conexão com a internet (para cotações em tempo real)

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/financetrack.git

# 2. Acesse a pasta do projeto
cd financetrack

# 3. Crie um ambiente virtual (isola as dependências)
python -m venv .venv

# 4. Ative o ambiente virtual
# No Windows:
.venv\Scripts\activate
# No Linux/Mac:
source .venv/bin/activate

# 5. Instale as dependências
pip install -r requirements.txt

# 6. Execute a aplicação
python main.py
```

---

## 📖 Como Usar

### Cotações de Moedas

1. No menu principal, escolha `[1] Cotações de Moedas`
2. Selecione a moeda desejada (ex: `[1]` para Dólar)
3. A cotação atual será exibida com variação percentual
4. Opcionalmente, informe um valor em R$ para conversão

### Gestão Financeira

1. No menu principal, escolha `[2] Gestão Financeira`
2. Defina seu saldo inicial com a opção `[4]`
3. Adicione receitas (`[1]`) e despesas (`[2]`)
4. Consulte o extrato completo com `[3]`

---

## 🧪 Testes

```bash
# Rodar todos os testes com detalhes
pytest test_main.py -v

# Rodar com relatório de cobertura
pytest test_main.py --cov=main --cov-report=term-missing

# Verificar qualidade do código (lint)
ruff check .
```

### Cobertura dos Testes

| Função | Tipo | Cobertura |
|---|---|---|
| `calcular_saldo` | Unitário | 6 casos |
| `adicionar_transacao` | Unitário | 5 casos |
| `converter_valor` | Unitário | 5 casos |
| `carregar_dados` / `salvar_dados` | Unitário | 3 casos |
| `buscar_cotacao` | Integração (mock) | 5 casos |

---

## ☁️ Deploy

### Opção 1 — Render (recomendado para iniciantes)

1. Acesse [render.com](https://render.com) e crie uma conta gratuita
2. Clique em **New → Web Service**
3. Conecte seu repositório GitHub
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
5. Clique em **Deploy**

> ⚠️ **Nota:** Aplicações CLI interativas funcionam melhor localmente. No Render/Railway, o deploy é útil para demonstrar o projeto e executar tarefas agendadas (cron jobs).

### Opção 2 — Railway

1. Acesse [railway.app](https://railway.app) e conecte com GitHub
2. Clique em **New Project → Deploy from GitHub repo**
3. Selecione o repositório `financetrack`
4. O Railway detecta automaticamente o Python e instala o `requirements.txt`

---

## 📁 Estrutura do Projeto

```
financetrack/
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline CI (GitHub Actions)
├── main.py                 # Código principal da aplicação
├── test_main.py            # Testes unitários e de integração
├── requirements.txt        # Dependências do projeto
├── pyproject.toml          # Configuração do Ruff (linter)
├── .gitignore              # Arquivos ignorados pelo Git
└── README.md               # Esta documentação
```

---

## 📌 Versionamento Semântico

Este projeto segue o padrão [SemVer](https://semver.org/lang/pt-BR/): `MAJOR.MINOR.PATCH`

| Versão | Mudança |
|---|---|
| `1.0.0` | Lançamento inicial com cotações e gestão financeira |

---

## 🌿 Branches

| Branch | Propósito |
|---|---|
| `main` | Código estável, pronto para produção |
| `entrega-intermediaria` | Branch de desenvolvimento do bootcamp |

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

---

## 👤 Autor

Feito com ❤️ durante o Bootcamp de Ciência da Computação.

> Substitua `SEU_USUARIO` nos badges e links pelo seu usuário real do GitHub.
