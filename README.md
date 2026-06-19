# Virtual Store — Loja Virtual com Flutter e Firebase

Aplicativo mobile de loja virtual desenvolvido em **Flutter (Dart)**, integrado com **Firebase** (Realtime Database + Authentication). Sem APIs pagas — Firebase possui plano gratuito.

---

## Funcionalidades

- Cadastro e login de usuários (Firebase Authentication)
- Listagem de produtos com imagem, nome e preço
- Favoritar produtos por usuário
- Carrinho de compras
- Histórico de pedidos
- Gerenciamento de produtos (adicionar, editar, remover)

---

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Flutter / Dart | App mobile (Android e iOS) |
| Firebase Authentication | Login e cadastro de usuários |
| Firebase Realtime Database | Armazenamento de produtos, pedidos e favoritos |
| Provider | Gerenciamento de estado |
| http | Comunicação REST com Firebase |
| shared_preferences | Persistência local do token de autenticação |

---

## Como Rodar

### Pré-requisitos

- [Flutter SDK](https://docs.flutter.dev/get-started/install) instalado
- Emulador Android/iOS ou dispositivo físico conectado
- Conta Google (para criar o Firebase — gratuito)

### 1. Clone o repositório

```bash
git clone https://github.com/RaphaelSilvaS/integracao-sistemas.git
cd integracao-sistemas
```

### 2. Configure o Firebase (GRATUITO — 15 minutos)

> Se o professor quiser rodar com os dados do projeto original, pule para o passo 3.

**2.1 — Crie um projeto Firebase**

1. Acesse [console.firebase.google.com](https://console.firebase.google.com)
2. Clique em **Adicionar projeto** > dê um nome > continue
3. Desative Google Analytics (opcional) > **Criar projeto**

**2.2 — Ative o Realtime Database**

1. No menu lateral: **Compilar > Realtime Database**
2. Clique em **Criar banco de dados**
3. Escolha a região (ex: `us-central1`) > **Próximo**
4. Selecione **Iniciar no modo de teste** > **Ativar**
5. Copie a URL do banco (ex: `https://SEU-PROJETO-default-rtdb.firebaseio.com`)

**2.3 — Ative a Autenticação**

1. No menu lateral: **Compilar > Authentication**
2. Clique em **Primeiros passos**
3. Na aba **Método de login**, ative **E-mail/senha** > Salvar

**2.4 — Copie a Web API Key**

1. No menu lateral: **Configurações do projeto** (ícone de engrenagem)
2. Na aba **Geral**, copie o campo **Chave da API da Web**

**2.5 — Cole no código**

Edite o arquivo [`lib/utils/constants.dart`](lib/utils/constants.dart):

```dart
static const FIREBASE_API_KEY = 'SUA_CHAVE_AQUI';
static const FIREBASE_DB_URL = 'https://SEU-PROJETO-default-rtdb.firebaseio.com';
```

### 3. Instale as dependências e rode

```bash
flutter pub get
flutter run
```

---

## Estrutura do Projeto

```
lib/
├── components/
│   ├── auth_form.dart          # Formulário de login/cadastro
│   ├── badge.dart              # Badge do carrinho
│   ├── cart_items.dart         # Item do carrinho
│   ├── main_drawer.dart        # Menu lateral
│   ├── order_item.dart         # Item de pedido
│   ├── product_grid_item.dart  # Card de produto
│   └── product_gridview.dart   # Grade de produtos
├── models/
│   ├── auth.dart               # Autenticação Firebase
│   ├── cart_item.dart          # Modelo de item do carrinho
│   ├── order_list.dart         # Lista de pedidos (Firebase)
│   ├── order_model.dart        # Modelo de pedido
│   └── product_model.dart      # Modelo de produto
├── providers/
│   ├── cart.dart               # Carrinho de compras
│   ├── counter.dart            # Contador simples
│   └── product_list.dart       # Lista de produtos (Firebase)
├── screens/
│   ├── auth_screen.dart        # Tela de login/cadastro
│   ├── cart_screen.dart        # Tela do carrinho
│   ├── orders_screen.dart      # Histórico de pedidos
│   ├── product_details_screen.dart  # Detalhe do produto
│   ├── product_form_screen.dart     # Formulário de produto
│   ├── products_overview_screen.dart # Home — grade de produtos
│   └── products_screen.dart    # Gerenciar produtos
├── utils/
│   ├── constants.dart          # CONFIGURAÇÃO FIREBASE (edite aqui)
│   └── routes/app_routes.dart  # Rotas da aplicação
└── main.dart                   # Ponto de entrada
```

---

## Integração com Firebase

O app se comunica com o Firebase via **REST API** — sem SDK adicional. Todas as chamadas usam o pacote `http`:

- **Autenticação:** `identitytoolkit.googleapis.com` (login e cadastro)
- **Produtos/Pedidos/Favoritos:** `firebaseio.com` (leitura e escrita via JSON)

O token de autenticação do Firebase é passado em cada requisição como parâmetro `?auth=TOKEN`, garantindo segurança dos dados por usuário.

---

## Plano Gratuito Firebase (Spark)

| Recurso | Limite gratuito |
|---|---|
| Usuários autenticados | Ilimitado |
| Realtime Database | 1 GB armazenamento / 10 GB/mês transferência |
| Requests | Ilimitado |

Suficiente para desenvolvimento e demonstração acadêmica.
