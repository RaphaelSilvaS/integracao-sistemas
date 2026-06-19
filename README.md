# Integração de Sistemas — Loja Virtual com Firebase

Projeto de integração entre dois sistemas distintos via **Firebase Realtime Database**,
utilizando **Python** (Sistema A) e **Flutter/Dart** (Sistema B).

---

## Arquitetura de Integração

```
┌──────────────────────────────────────────────────────────────┐
│                    SISTEMA A — Python                        │
│  seed_firebase.py                                            │
│  - Gera dados brutos dos produtos                            │
│  - Valida campos obrigatórios e preços                       │
│  - Transforma e normaliza os dados                           │
│  - Carrega no Firebase via REST API                          │
└─────────────────────────┬────────────────────────────────────┘
                          │  HTTP REST (JSON)
                          ▼
          ┌───────────────────────────────┐
          │   Firebase Realtime Database  │
          │   (projeto-integrador-303c5)  │
          │   /products   /orders         │
          └───────────────┬───────────────┘
                          │  HTTP REST (JSON)
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                    SISTEMA B — Flutter/Dart                  │
│  App Mobile (Android/iOS/Web)                                │
│  - Autentica usuário via Firebase Auth                       │
│  - Lê produtos do Firebase em tempo real                     │
│  - Exibe loja com carrinho e pedidos                         │
│  - Grava pedidos de volta no Firebase                        │
└──────────────────────────────────────────────────────────────┘
```

**Interoperabilidade:** Python escreve → Firebase centraliza → Flutter lê.
Dois sistemas em linguagens diferentes comunicando via mesma API REST.

---

## Tecnologias

| Sistema | Linguagem | Tecnologia | Função |
|---|---|---|---|
| Sistema A | Python | requests | Popula o Firebase com produtos validados |
| Banco Central | — | Firebase Realtime Database | Armazena e sincroniza dados entre sistemas |
| Sistema B | Dart/Flutter | http, Provider | App mobile que consome os dados do Firebase |
| Autenticação | — | Firebase Authentication | Login/cadastro de usuários (e-mail e senha) |

---

## Como Rodar

### Pré-requisitos

- Python 3.10+ instalado
- Flutter SDK instalado
- Conta Firebase configurada (veja configuração abaixo)

---

### Pré-requisito — Chave Groq (gratuita, 2 minutos)

A IA de validação usa o **Groq** (gratuito, sem cartão de crédito):

1. Acesse [console.groq.com](https://console.groq.com)
2. Entre com conta Google
3. Clique em **"API Keys"** → **"Create API Key"**
4. Copie a chave gerada

---

### Passo 1 — Clone o repositório

```bash
git clone https://github.com/RaphaelSilvaS/integracao-sistemas.git
cd integracao-sistemas
```

---

### Passo 2 — Configure a chave Groq

Crie um arquivo `.env` na raiz do projeto:

```
GROQ_API_KEY=sua_chave_groq_aqui
```

Ou exporte no terminal:
```bash
# Windows
set GROQ_API_KEY=sua_chave_aqui

# Linux/Mac
export GROQ_API_KEY=sua_chave_aqui
```

---

### Passo 3 — Execute o Pipeline de Agentes (Sistema A)

O Sistema A popula o Firebase com produtos validados:

```bash
python seed_firebase.py
```

Saída esperada:
```
Validando e carregando produtos no Firebase...
  [OK] Camiseta Básica Branca
  [OK] Calça Jeans Slim
  [OK] Tênis Casual Branco
  ...
Concluido! 8 produtos carregados no Firebase.
```

---

### Passo 3 — Execute o Sistema B (Flutter)

O Sistema B lê os dados que o Sistema A carregou:

```bash
flutter pub get
flutter run -d chrome
```

O app abre no navegador. Crie uma conta com e-mail e senha para ver os produtos.

---

## Configuração do Firebase

As credenciais já estão configuradas em `lib/utils/constants.dart`:

```dart
static const FIREBASE_API_KEY = 'AIzaSyCKNk9uRu0Xwk9oYdjpioHyXUOkv1NRrNY';
static const FIREBASE_DB_URL = 'https://projeto-integrador-303c5-default-rtdb.firebaseio.com';
```

Para usar seu próprio Firebase:
1. Acesse [console.firebase.google.com](https://console.firebase.google.com)
2. Crie um projeto → ative Realtime Database (modo teste) → ative Authentication (E-mail/senha)
3. Substitua os valores acima com suas credenciais

---

## Estrutura do Projeto

```
integracao-sistemas/
│
├── seed_firebase.py            # SISTEMA A — Python: valida e carrega produtos
│
├── lib/                        # SISTEMA B — Flutter/Dart
│   ├── main.dart               # Ponto de entrada do app
│   ├── models/
│   │   ├── auth.dart           # Autenticação Firebase (login/cadastro)
│   │   ├── product_model.dart  # Modelo de produto
│   │   ├── order_list.dart     # Pedidos (leitura e escrita no Firebase)
│   │   └── order_model.dart    # Modelo de pedido
│   ├── providers/
│   │   ├── product_list.dart   # CRUD de produtos via Firebase REST
│   │   └── cart.dart           # Carrinho de compras (estado local)
│   ├── screens/
│   │   ├── auth_screen.dart           # Tela de login/cadastro
│   │   ├── products_overview_screen.dart  # Home — grade de produtos
│   │   ├── product_details_screen.dart    # Detalhes do produto
│   │   ├── product_form_screen.dart       # Formulário (admin)
│   │   ├── cart_screen.dart              # Carrinho
│   │   └── orders_screen.dart            # Histórico de pedidos
│   └── utils/
│       └── constants.dart      # Credenciais Firebase (edite aqui)
│
├── android/                    # Configuração Android
├── ios/                        # Configuração iOS
├── assets/                     # Fontes e imagens
└── pubspec.yaml                # Dependências Flutter
```

---

## Fluxo de Dados (Interoperabilidade)

```
1. seed_firebase.py (Python)
   └─ gera 8 produtos de roupas/calçados
   └─ valida: nome ≥ 3 chars, preço > 0, descrição ≥ 10 chars
   └─ POST /products.json → Firebase

2. Firebase Realtime Database
   └─ armazena os dados em formato JSON
   └─ URL pública REST: .../products.json

3. Flutter App (Dart)
   └─ ProductsList.loadProducts() → GET /products.json?auth=TOKEN
   └─ exibe produtos em grade com nome e preço
   └─ usuário pode favoritar, adicionar ao carrinho, fazer pedido
   └─ pedido → POST /orders/{userId}.json → Firebase
```

---

## Git — Histórico de Commits

```
2a91d9e  Remove campo de imagem obrigatorio e adiciona script de seed
a9ce697  Configura credenciais do Firebase do projeto integrador
538deff  Migra projeto para loja virtual Flutter com Firebase
98bbb29  fix: alinha dados do demo_agentes.py com demo.py
de2eee8  docs: separa modo demo do modo producao no README
892c336  feat: adiciona modo demo dos agentes (SQLite -> JSON)
47891b2  feat: adiciona arquitetura multi-agente com validacao por IA
6fc85d9  fix: README e terminologia alinhados com os dois sistemas
5194661  chore: adiciona dados gerados pelo demo
84a55e3  refactor: ETL com dois sistemas distintos (SQLite e JSON)
7418ae5  feat: pipeline ETL Firebase-to-Firebase - Projeto Integrador
```

---

## Plano Gratuito Firebase (Spark)

| Recurso | Limite gratuito |
|---|---|
| Usuários autenticados | Ilimitado |
| Realtime Database | 1 GB armazenamento / 10 GB/mês |
| Requests | Ilimitado |

**Nenhuma API paga é utilizada neste projeto.**
