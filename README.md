# Pipeline ETL — Integracao entre Sistemas com IA
### Projeto Integrador | Integração entre Sistemas

Sistema de integração de dados entre dois sistemas distintos, implementando o pipeline **ETL** (Extract → Transform → Load).

---

## Os dois sistemas

| | Sistema 1 (Origem) | Sistema 2 (Destino) |
|---|---|---|
| **Tecnologia** | Banco de dados SQLite | Arquivo JSON |
| **Arquivo** | `dados/sistema1.db` | `dados/sistema2_depois_etl.json` |
| **Função** | Fonte dos dados brutos | Destino dos dados validados |
| **Validação** | `dados/sistema1_antes_etl.json` | `dados/sistema2_depois_etl.json` |

### Como validar a migração

Após rodar `python demo.py`, compare os dois arquivos:

- **`dados/sistema1_antes_etl.json`** — dados brutos do Sistema 1, incluindo registros inválidos
- **`dados/sistema2_depois_etl.json`** — dados migrados para o Sistema 2, somente registros válidos

Diferenças esperadas entre os dois arquivos:

| Registro | Sistema 1 | Sistema 2 | Motivo |
|----------|-----------|-----------|--------|
| prod-001 | ✅ presente | ✅ migrado | válido |
| prod-002 | ✅ presente | ✅ migrado (nome normalizado) | válido |
| prod-003 | ✅ presente | ✅ migrado | válido |
| prod-004 | ⚠️ presente | ❌ rejeitado | nome vazio |
| prod-005 | ⚠️ presente | ❌ rejeitado | preço negativo |
| ord-001  | ✅ presente | ✅ migrado | válido |
| ord-002  | ✅ presente | ✅ migrado | válido |
| ord-003  | ⚠️ presente | ❌ rejeitado | total zero e sem itens |

---

## Como rodar (sem nenhuma configuração)

Requisitos: **Python 3.10+** instalado.

```bash
# 1. Clone o repositório
git clone https://github.com/RaphaelSilvaS/integracao-firebase.git
cd integracao-firebase

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o pipeline ETL no modo demo
python demo.py
```

Ao final da execução, os arquivos de validação estarão em `dados/`:

```
dados/
├── sistema1.db                 ← Sistema 1: banco SQLite (origem)
├── sistema1_antes_etl.json     ← Sistema 1 exportado para leitura (ANTES)
├── sistema2_depois_etl.json    ← Sistema 2: resultado da migração (DEPOIS)
└── migracao_resumo.json        ← resumo da execução com métricas
```

---

## Etapas do pipeline ETL

```
┌─────────────┐     ┌───────────┐     ┌─────────────┐     ┌─────────────┐
│  SISTEMA 1  │     │  EXTRACT  │     │  TRANSFORM  │     │  SISTEMA 2  │
│  SQLite .db │ ──► │  Leitura  │ ──► │  Validação  │ ──► │  JSON file  │
│  (origem)   │     │  das      │     │  Limpeza    │     │  (destino)  │
│             │     │  tabelas  │     │  Metadados  │     │             │
└─────────────┘     └───────────┘     └─────────────┘     └─────────────┘
```

### O que cada etapa faz

| Etapa | Classe | Descrição |
|-------|--------|-----------|
| Extract | `src/extractor.py` | Lê todas as tabelas do Sistema 1 |
| Transform | `src/transformer.py` | Valida campos obrigatórios, normaliza strings, rejeita inválidos |
| Load | `src/loader.py` | Grava os registros válidos no Sistema 2 |

### Regras de validação (Transform)

**Produtos:**
- `name` não pode ser vazio
- `description` não pode ser vazia
- `imageURL` não pode ser vazia
- `price` deve ser numérico e maior que zero

**Pedidos:**
- `total` deve ser numérico e maior que zero
- `products` deve ser uma lista não vazia
- `date` deve ser uma data válida no formato ISO

---

## Estrutura do projeto

```
integracao-firebase/
├── dados/                          ← gerado ao rodar demo.py
│   ├── sistema1.db                 ← Sistema 1 (SQLite)
│   ├── sistema1_antes_etl.json     ← Sistema 1 legível (ANTES)
│   ├── sistema2_depois_etl.json    ← Sistema 2 (DEPOIS)
│   └── migracao_resumo.json        ← métricas da execução
├── src/
│   ├── extractor.py                ← extrai dados do Sistema 1
│   ├── transformer.py              ← valida e normaliza os dados
│   ├── loader.py                   ← carrega dados no Sistema 2
│   ├── logger.py                   ← logs coloridos + arquivo
│   └── integrator.py               ← orquestra o pipeline ETL
├── config/
│   └── settings.py                 ← configurações Firebase (modo produção)
├── tests/
│   └── test_integration.py         ← testes das regras de validação
├── demo.py                         ← modo demo (roda sem Firebase)
├── main.py                         ← modo produção (requer Firebase)
└── requirements.txt
```

---

## Testes automatizados

```bash
python tests/test_integration.py
```

Valida as regras de transformação sem precisar de banco ou internet.

---

## Uso de Inteligência Artificial

Este projeto foi desenvolvido com apoio de IA (Claude — Anthropic) para:
- Geração e sugestão de código
- Modelagem da arquitetura ETL
- Identificação de erros e melhorias
- Otimização do pipeline de dados

---

## Tecnologias utilizadas

- **Python 3.10+**
- **sqlite3** — banco de dados do Sistema 1 (origem)
- **json** — formato do Sistema 2 (destino)
- **requests** — chamadas HTTP para a API REST do Firebase (modo produção)
- **colorama** — logs coloridos no terminal

---

## Projeto Integrador — Integração entre Sistemas
Curso de Tecnologia da Informação
