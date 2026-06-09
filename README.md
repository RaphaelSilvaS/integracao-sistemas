# Integracao Firebase — Sistema ETL
### Projeto Integrador — Integracao entre Sistemas com apoio de IA

Sistema de integração de dados entre dois sistemas distintos.  
Arquitetura **ETL** (Extract → Transform → Load) com Firebase Realtime Database como origem e destino.

---

## Execucao rapida (sem configuracao) — MODO DEMO

Nao precisa de conta Firebase nem de nenhuma configuracao.  
Funciona em qualquer maquina com Python instalado.

```bash
# 1. Instale as dependencias
pip install -r requirements.txt

# 2. Rode o modo demo
python demo.py
```

O demo usa os arquivos da pasta `demo/` como origem e destino:
- **Entrada**: `demo/origem.json` — 5 produtos e 3 pedidos de exemplo
- **Saida**: `demo/destino.json` — dados validados e migrados
- **Relatorio**: `demo/metadados.json` — resumo da execucao

---

## O que o modo demo demonstra

O pipeline roda as **4 etapas completas** do sistema:

| Etapa | O que faz |
|-------|-----------|
| 1. Autenticacao | Conecta nos dois sistemas (origem e destino) |
| 2. Extracao | Le os dados do Sistema X |
| 3. Transformacao | Valida e normaliza cada registro |
| 4. Carga | Grava os dados no Sistema Y |

**Registros validos** sao migrados e recebem metadados (`_migrado_em`, `_origem_id`, `_sistema`).  
**Registros invalidos** sao detectados e ignorados com log de aviso:
- `prod-004` — ignorado por ter nome vazio
- `prod-005` — ignorado por ter preco negativo
- `ord-003`  — ignorado por ter total zero e lista de produtos vazia

---

## Descricao do projeto

A aplicacao realiza as seguintes operacoes:
- **Extracao** de dados do Firebase (Sistema X / Origem)
- **Transformacao** e validacao dos dados extraidos
- **Carregamento** dos dados no Firebase (Sistema Y / Destino)
- **Log** completo de todas as operacoes realizadas
- **Relatorio** final com metricas da integracao

---

## Estrutura do projeto

```
integracao-firebase/
├── demo/
│   ├── origem.json        # Dados de exemplo (Sistema X)
│   ├── destino.json       # Gerado ao rodar demo.py
│   └── metadados.json     # Gerado ao rodar demo.py
├── src/
│   ├── extractor.py       # Extrai dados do Firebase origem
│   ├── transformer.py     # Transforma e valida os dados
│   ├── loader.py          # Carrega dados no Firebase destino
│   ├── logger.py          # Sistema de logs coloridos
│   └── integrator.py      # Orquestra todo o processo (pipeline)
├── config/
│   └── settings.py        # Configuracoes dos dois Firebases
├── tests/
│   └── test_integration.py # Testes automatizados
├── demo.py                # Modo demo — roda sem Firebase
├── main.py                # Modo producao — requer Firebase
├── requirements.txt       # Dependencias do projeto
└── README.md
```

---

## Execucao com Firebase real (modo producao)

### 1. Instale as dependencias
```bash
pip install -r requirements.txt
```

### 2. Configure os Firebases em `config/settings.py`
Insira as URLs, chaves de API e credenciais dos seus dois projetos Firebase.

### 3. Execute
```bash
python main.py
```

---

## Testes automatizados

```bash
python tests/test_integration.py
```

Os testes validam as regras de transformacao sem precisar de Firebase ou internet.

---

## Tecnologias utilizadas
- **Python 3.10+**
- **requests** — chamadas HTTP para a API REST do Firebase
- **python-dotenv** — variaveis de ambiente
- **colorama** — logs coloridos no terminal

---

## Uso de Inteligencia Artificial

Este projeto foi desenvolvido com apoio de IA (Claude - Anthropic) para:
- Geracao e sugestao de codigo
- Modelagem da arquitetura de integracao ETL
- Identificacao de erros e melhorias
- Otimizacao do pipeline de dados

---

## Projeto Integrador — Integracao entre Sistemas
Curso de Tecnologia da Informacao
