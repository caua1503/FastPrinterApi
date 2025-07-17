# Guia de Desenvolvimento do Projeto

Este guia foi criado para ajudar quem deseja contribuir com o projeto ou entende-lo, explicando desde a configuração do ambiente até as decisões de arquitetura que tomei.

## 1. Configuração do Ambiente de Desenvolvimento

Este projeto utiliza `uv` para gerenciamento de dependências e ambientes virtuais. `uv` é uma ferramenta de alta performance, similar ao poetry, que agiliza a instalação e o gerenciamento de pacotes.

1.  **Instale o `uv`**: Recomendo seguir a [documentação oficial de instalação do uv](https://docs.astral.sh/uv/getting-started/installation/) para ter a ferramenta disponível em seu sistema ou instalar via pip.
2.  **Sincronize as dependências**: Após instalar o `uv`, navegue até a raiz do projeto e execute o seguinte comando para instalar todas as dependências:
    ```bash
    uv sync
    ```

## 2. Comandos Úteis (Taskipy)

Para facilitar o desenvolvimento, configurei alguns atalhos com `taskipy`. Abaixo estão os comandos disponíveis:

### Ambiente e Execução
- `task dev`: Inicia o ambiente de desenvolvimento usando o script `development.sh`.
- `task windev`: Cria um ambiente, constrói a imagem Docker e sobe os contêineres (otimizado para Windows).
- `task build`: Constrói a imagem Docker da aplicação.
- `task rundocker`: Inicia os serviços definidos no `docker-compose.yaml` em modo detached.
- `task docker`: Executa as tarefas `build` e `rundocker` em sequência.

### Qualidade e Testes de Código
- `task lint`: Formata o código com `ruff` e aplica correções automáticas.
- `task check`: Apenas verifica a formatação e a qualidade do código com `ruff`.
- `task test`: Formata, verifica e executa a suíte de testes com `pytest`.

### Migrations (Banco de Dados Principal)
- `task migrations`: Cria a estrutura inicial de migrations com Alembic (usar apenas uma vez).
- `task update`: Gera um novo arquivo de migração baseado nas alterações dos `models`.
- `task upgrade`: Aplica as migrações pendentes no banco de dados.

### Migrations (Banco de Dados de Logs)
- `task migrations_logs`: Cria a estrutura inicial de migrations para os logs.
- `task updatelogs`: Gera uma nova migração para a base de logs.
- `task upgradelogs`: Aplica as migrações de logs pendentes.


## 3. Decisões de Arquitetura e Padrões

### Arquitetura em Camadas
Busquei organizar o projeto seguindo uma **Arquitetura em Camadas (Layered Architecture)**. A ideia é separar o código com base em suas responsabilidades para facilitar a manutenção e a evolução do projeto.

- `app/routers`: Define os endpoints da API. Recebe as requisições HTTP, valida os dados com os `schemas` e chama a camada de serviço correspondente.
- `app/services`: Contém a lógica de negócio da aplicação. Orquestra as operações e interage com a camada de acesso a dados.
- `app/models`: Define os modelos de dados (tabelas) utilizando SQLAlchemy ORM.
- `app/schemas`: Define os "contratos" de dados com Pydantic, garantindo a validação e o formato dos dados de entrada e saída.
- `app/core`: Armazena funcionalidades que são usadas em vários lugares, como segurança, tarefas em background (Celery) e logging.
- `app/helpers`: Contém funções utilitárias para auxiliar em tarefas específicas, como sessões de banco de dados, manipulação de Redis, e formatação de dados.
- `app/config`: Centraliza as configurações da aplicação, carregadas a partir de variáveis de ambiente.

### Testes com Pytest
Para garantir a qualidade e estabilidade, o projeto conta com uma suíte de testes com `pytest`. A cobertura de testes busca abranger grande parte do código, ajudando a prevenir regressões e erros inesperados. A estrutura dos testes foi pensada com foco na separação de responsabilidades, utilizando fixtures para isolar e configurar os cenários de teste.

### Tipagem Estática
Apesar da tipagem dinâmica do Python, optei por adotar a **tipagem estática (static typing)** em todo o projeto. Ferramentas como Pydantic e SQLAlchemy, que já são a base para os schemas e modelos, incentivam essa prática.

**Por que adotei a tipagem estática:**
- **Clareza**: Torna o código mais legível e fácil de entender.
- **Produtividade**: Ajuda no autocompletar inteligente e na navegação pela IDE.
- **Segurança**: Permite refatorações mais seguras e ajuda a encontrar erros antes mesmo de executar o código.
- **Documentação**: Funciona como uma documentação viva e sempre atualizada.
- **Manutenção**: Simplifica a manutenção, especialmente conforme o projeto cresce.

