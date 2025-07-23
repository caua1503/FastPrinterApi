# Guia de Uso do Backend

Este guia fornece instruções essenciais sobre como utilizar o backend do sistema de gerenciamento de impressoras.

## Acessando a Documentação Interativa (Swagger UI)

Toda a API é autodocumentada (graças ao FastAPi) seguindo o padrão OpenAPI. 
Você pode acessar a interface do Swagger UI para ver todos os endpoints do projeto, seus parâmetros e modelos de dados.

- **URL de acesso:** `http://<seu-servidor>:<porta>/docs`
- **URL de acesso (localhost):** `http://localhost:8000/docs`

Através da interface, você pode:
- Visualizar todos os endpoints disponíveis.
- Entender quais parâmetros cada endpoint espera.
- Testar a API em tempo real, enviando requisições e vendo as respostas.

## Primeiro Acesso e Autenticação

Para o primeiro uso, um usuário administrador padrão é criado para que você possa configurar o sistema.

- **Login:** `fastprinter_admin`
- **Senha:** `123456`

**Importante:** Por razões de segurança, é recomendável que você **altere a senha** deste usuário no primeiro acesso. O sistema pode solicitar a troca de senha automaticamente.

Para se autenticar, utilize o endpoint `/api/v1/auth/login` e envie as credenciais. A API retornará um token de acesso que deverá ser usado para autorizar as requisições subsequentes.

## Principais Funcionalidades da API

A API está organizada em rotas que representam os principais recursos do sistema:

- `/users`: Gerenciamento de usuários (criar, ler, atualizar, deletar).
- `/printers`: Gerenciamento de impressoras.
- `/supplies`: Controle de suprimentos (toners, cartuchos, etc.).
- `/departments`: Gerenciamento de departamentos da organização.
- `/history`: Registro de históricos de manutenções, recargas e outros eventos.
- `/permissions`: Controle de permissões de acesso dos usuários e suas chaves de API.

Recomendo explorar cada uma dessas rotas na documentação do Swagger para ajudar a entender o funcionamento.