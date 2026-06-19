# Pipeline ETL Multi-Agente com IA

Sistema de integração de dados entre dois ambientes Firebase, utilizando arquitetura de agentes autônomos com validação inteligente via IA (Claude — Anthropic).

---

## Sistemas Envolvidos

| | Sistema A | Sistema B |
|---|---|---|
| **Tipo** | Firebase Realtime Database (Origem) | Firebase Realtime Database (Destino) |
| **Papel** | Fornece os dados brutos | Recebe os dados validados e normalizados |
| **Config** | `config/settings.py → FIREBASE_ORIGEM` | `config/settings.py → FIREBASE_DESTINO` |

---

## Arquitetura de Agentes

O pipeline é composto por **1 agente orquestrador** e **4 sub-agentes especializados**, cada um com responsabilidade única e autônoma.

```
┌─────────────────────────────────────────────┐
│           AGENTE ORQUESTRADOR               │
│   Coordena o fluxo e o contexto compartilhado│
└────────────────────┬────────────────────────┘
                     │
     ┌───────────────┼───────────────────┐
     ▼               ▼                   ▼
┌─────────┐   ┌────────────┐   ┌──────────────┐
│Sub-agente│   │ Sub-agente │   │  Sub-agente  │
│Extração  │──▶│Validação IA│──▶│Transformação │
│          │   │  (Claude)  │   │              │
└─────────┘   └────────────┘   └──────┬───────┘
                                       │
                          ┌────────────┴──────────┐
                          ▼                        ▼
                   ┌────────────┐         ┌──────────────┐
                   │ Sub-agente │         │  Sub-agente  │
                   │   Carga    │         │ Monitoramento│
                   │(Sistema B) │         │  (Relatório) │
                   └────────────┘         └──────────────┘
```

### Agente Orquestrador — `agents/orchestrator_agent.py`

Responsável por inicializar e coordenar todos os sub-agentes em sequência. Gerencia o contexto compartilhado entre eles e interrompe o pipeline em caso de falha crítica.

### Sub-agente de Extração — `agents/extraction_agent.py`

Conecta ao **Sistema A** (Firebase Origem), autentica via API REST e extrai todas as coleções configuradas (`products`, `orders`). Retorna os dados brutos para o contexto compartilhado.

### Sub-agente de Validação IA — `agents/validation_agent.py`

Envia uma amostra dos dados extraídos para o modelo **Claude (Anthropic)** e recebe:

- **Score de qualidade** dos dados (0 a 100)
- **Lista de anomalias** detectadas automaticamente (campos vazios, preços negativos, formatos inválidos)
- **Decisão autônoma**: `prosseguir` ou `interromper` o pipeline

Este agente resolve a **complexidade** do projeto — a IA analisa padrões que regras fixas não conseguem detectar.

### Sub-agente de Transformação — `agents/transformation_agent.py`

Valida campos obrigatórios, normaliza strings, arredonda valores numéricos e adiciona metadados de migração (timestamp, ID de origem). Apenas registros válidos seguem para a carga.

### Sub-agente de Carga — `agents/loading_agent.py`

Conecta ao **Sistema B** (Firebase Destino), autentica e carrega os dados transformados coleção a coleção via requisições PUT, preservando os IDs originais.

### Sub-agente de Monitoramento — `agents/monitoring_agent.py`

Consolida as métricas de todos os agentes e gera um relatório JSON em `dados/relatorios/`. Exibe no terminal um sumário com totais de registros extraídos, validados, transformados e carregados.

---

## Estrutura do Projeto

```
integracao-firebase/
├── agents/
│   ├── base_agent.py           # Classe abstrata base para todos os agentes
│   ├── orchestrator_agent.py   # Agente Orquestrador
│   ├── extraction_agent.py     # Sub-agente: extração do Sistema A
│   ├── validation_agent.py     # Sub-agente: validação por IA (Claude)
│   ├── transformation_agent.py # Sub-agente: transformação dos dados
│   ├── loading_agent.py        # Sub-agente: carga no Sistema B
│   └── monitoring_agent.py     # Sub-agente: métricas e relatório
├── src/
│   ├── extractor.py            # Comunicação com Firebase Origem
│   ├── transformer.py          # Regras de validação e normalização
│   ├── loader.py               # Comunicação com Firebase Destino
│   └── logger.py               # Logger colorido com contadores
├── config/
│   └── settings.py             # Credenciais dos dois sistemas Firebase
├── dados/
│   └── relatorios/             # Relatórios gerados automaticamente
├── main_agentes.py             # Ponto de entrada (modo agentes + IA)
├── main.py                     # Ponto de entrada (modo produção original)
├── demo.py                     # Modo demonstração local (sem Firebase)
└── requirements.txt
```

---

## Como Reproduzir o Ambiente

### Modo Demo — recomendado para validação (sem Firebase)

**Pré-requisito único:** Chave de API da [Anthropic (Claude)](https://console.anthropic.com/)

```bash
# 1. Clone o repositório
git clone https://github.com/RaphaelSilvaS/integracao-sistemas.git
cd integracao-sistemas

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Configure a chave da API (Windows)
set ANTHROPIC_API_KEY=sua_chave_aqui

# 4. Execute
python demo_agentes.py
```

O Sistema A (SQLite) e o Sistema B (JSON) são criados automaticamente na pasta `dados/`. Nenhuma conta Firebase é necessária.

---

### Modo Produção — Firebase real (opcional)

**Pré-requisitos:** Dois projetos Firebase + Chave Anthropic

Edite `config/settings.py` com as credenciais dos dois projetos Firebase:

```python
FIREBASE_ORIGEM = {
    "url": "https://seu-projeto-origem.firebaseio.com",
    "api_key": "SUA_API_KEY_ORIGEM",
    "email": "seu@email.com",
    "password": "sua_senha",
    "colecoes": ["products", "orders"]
}

FIREBASE_DESTINO = {
    "url": "https://seu-projeto-destino.firebaseio.com",
    "api_key": "SUA_API_KEY_DESTINO",
    "email": "seu@email.com",
    "password": "sua_senha"
}
```

```bash
set ANTHROPIC_API_KEY=sua_chave_aqui
python main_agentes.py
```

---

## Fluxo de Dados

```
Sistema A (Firebase Origem)
        │
        ▼
[Agente Extração] ──► dados brutos em memória
        │
        ▼
[Agente Validação IA] ──► Claude analisa qualidade e anomalias
        │
        ▼
[Agente Transformação] ──► dados normalizados e enriquecidos
        │
        ▼
[Agente Carga] ──► dados gravados no Sistema B
        │
        ▼
Sistema B (Firebase Destino)
        │
        ▼
[Agente Monitoramento] ──► relatório JSON em dados/relatorios/
```

---

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.10+ | Linguagem principal |
| Firebase Realtime Database | Sistema A (Origem) e Sistema B (Destino) |
| Claude — Anthropic | Validação inteligente de dados (IA) |
| requests | Comunicação HTTP com Firebase |
| colorama | Logs coloridos no terminal |
| python-dotenv | Variáveis de ambiente |

---

Projeto desenvolvido com suporte de IA (Claude — Anthropic) para arquitetura, implementação e validação inteligente dos dados.
