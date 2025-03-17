# Gerir Clientes - API Documentation

Este projeto é uma API para gerenciamento de cobranças, pagamentos e clientes.

---

## Testar a Proteção das Rotas

Abaixo estão os passos para testar a proteção das rotas usando autenticação JWT.

### 1. Obter o Token de Acesso e Refresh

Faça uma requisição `POST` para o endpoint `/api/token/` com as credenciais do usuário.

#### Exemplo de Requisição:

```bash
curl -X POST -d "username=seu_usuario&password=sua_senha" http://127.0.0.1:8000/api/token/
```

```bash
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

- `access`: Token de acesso que será usado para autenticar as requisições.
- `refresh`: Token usado para obter um novo token de acesso quando o atual expirar.

### 2. Usar o Token

- Envie o token no cabeçalho Authorization para acessar as rotas protegidas:

> curl -H "Authorization: Bearer <seu_token_de_acesso>" http://127.0.0.1:8000/api/cobrancas/

### 3. Atualizar o Token

- Faça uma requisição `POST` para `/api/token/refresh/` com o token de refresh:

> curl -X POST -d "refresh=<seu_token_de_refresh>" http://127.0.0.1:8000/api/token/refresh/
