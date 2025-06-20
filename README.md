# FastPrinterAPI

Uma API assíncrona desenvolvida em FastAPI para o gerenciamento centralizado de múltiplas impressoras, com foco em estatísticas, previsões e histórico detalhado de manutenção.

Embora o núcleo do projeto seja a API RESTful, ele também inclui uma interface gráfica intuitiva para facilitar a interação e o gerenciamento.

## Objetivo

Facilitar o controle, monitoramento e manutenção de parques de impressoras, fornecendo:
- Estatísticas em tempo real de uso e status
- Previsão de próximas recargas e limpezas
- Histórico completo de manutenções, recargas e eventos
- Gestão de departamentos, suprimentos e usuários

## Principais Funcionalidades

- **Gestão de Impressoras:** Cadastro, atualização, consulta e remoção de impressoras.
- **Histórico de Manutenção:** Registro e consulta de manutenções, recargas e limpezas.
- **Previsão Inteligente:** Cálculo da próxima recarga/limpeza com base no uso e histórico.
- **Gestão de Suprimentos:** Controle de suprimentos.
- **Departamentos e Usuários:** Organização por setores e permissões de acesso.
- **Autenticação Segura:** Endpoints protegidos para operações sensíveis.

## Tecnologias Utilizadas

- Python 3.12+
- FastAPI (assíncrono)
- Pydantic (validação de dados)
- SQLAlchemy (ORM)
- Alembic (migrações)
- Docker (opcional)
- Testes automatizados (pytest)

## Estrutura do Projeto

```
impressoras/
  app/
    routers/api/      # Endpoints organizados por domínio
    schemas/          # Schemas Pydantic para validação
    models/           # Modelos ORM
    services/         # Lógica de negócio
    helpers/          # Utilitários e integrações
    static/           # Arquivos estáticos (css, js, img)
    templates/        # Templates HTML
  migrations/         # Migrações do banco de dados
  test/               # Testes automatizados
  Dockerfile          # Containerização
  README.md           # Este arquivo
```
