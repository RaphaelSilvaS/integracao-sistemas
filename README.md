# 🔄 Integração Firebase → Firebase
### Projeto Integrador — Integração entre Sistemas com apoio de IA

Este projeto demonstra a integração entre dois sistemas distintos utilizando
Firebase Realtime Database como origem e destino, com transformação e validação
de dados durante o processo de migração/sincronização.

---

## 📋 Descrição

A aplicação realiza as seguintes operações:
- **Extração** de dados do Firebase (Sistema X / Origem)
- **Transformação** e validação dos dados extraídos
- **Carregamento** dos dados no Firebase (Sistema Y / Destino)
- **Log** completo de todas as operações realizadas
- **Relatório** final com métricas da integração

---

## 🗂️ Estrutura do Projeto

```
integracao-firebase/
├── src/
│   ├── extractor.py       # Extrai dados do Firebase origem
│   ├── transformer.py     # Transforma e valida os dados
│   ├── loader.py          # Carrega dados no Firebase destino
│   ├── logger.py          # Sistema de logs
│   └── integrator.py      # Orquestra todo o processo (pipeline)
├── config/
│   └── settings.py        # Configurações dos dois Firebases
├── tests/
│   └── test_integration.py # Testes automatizados
├── logs/                  # Logs gerados automaticamente
├── main.py                # Ponto de entrada da aplicação
├── requirements.txt       # Dependências do projeto
└── README.md
```

---

## ⚙️ Como configurar

### 1. Instale as dependências
```bash
pip install -r requirements.txt
```

### 2. Configure os Firebases em `config/settings.py`
Insira as URLs e chaves dos seus dois projetos Firebase.

### 3. Execute
```bash
python main.py
```

---

## 🛠️ Tecnologias utilizadas
- **Python 3.10+**
- **requests** — chamadas HTTP para a API REST do Firebase
- **python-dotenv** — variáveis de ambiente
- **colorama** — logs coloridos no terminal

---

## 🤖 Uso de Inteligência Artificial
Este projeto foi desenvolvido com apoio de IA (Claude - Anthropic) para:
- Geração e sugestão de código
- Modelagem da arquitetura de integração
- Identificação de erros e melhorias
- Otimização do pipeline de dados

---

## 👨‍💻 Projeto Integrador — Integração entre Sistemas
Curso de Tecnologia da Informação
