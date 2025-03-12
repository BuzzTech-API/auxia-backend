# auxia-backend

## Como inicializar a aplicação

Se você tiver [poetry](https://python-poetry.org/) instalado:

```bash
poetry shell
poetry install
make run
```

Caso não tenha instalado:

```bash
python3 -m venv venv
source venv/bin/activate # se você usa linux
source venv/Scripts/activate # se você usa windows
pip install -r requirements.txt
fastapi dev ./auxia/main.py
```

## Diagrama de rotas

### Rotas de generate e Criação de usuário

<image src="./doc/img/Diagrama de rotas.png" alt="Rota de post generate e post user" />

## Diagrama de Banco de dados

<image src="./doc/img/Diagrama BD API V2.drawio.png" alt="Rota de post generate e post user" />

## Estrutura das pastas

- auxia/
  - controllers/
  - core/
  - db/
  - models/
  - schemas/
  - usecases/
  - main.py
  - routers.py
- doc/
  - img/
- tests/
  - schemas/
  - usecases/
  - controllers/
  - conftest.py
  - factories.py

### auxia/

É a pasta principal onde está todo o programa, sendo os arquivos main.py o servidor e routers onde são adicionado todas rotas dos controllers

#### auxia/controllers/

É a pasta onde fica as configurações das rotas separada por suas categorias

#### auxia/core/

É a pasta onde fica configurações importantes e classes que são importante para toda aplicação como exceçõestá

#### auxia/db/

É a pasta onde fica a classe de gerenciamento da conexão com o banco

#### auxia/models/

É a pasta onde fica os modelos que tem lógicas importantes de négocio

#### auxia/schemas/

É a pasta onde fica os esquemas de dados que irão entrar e sair da aplicação

#### auxia/usecases/

É a pasta onde fica funções de caso de uso, como criar um usuário no banco, buscar usuário no banco e etc.

### doc/

É a pasta onde está todos arquivos de documentação do backend

#### doc/img/

É a pasta onde fica as imagens da documentação

### tests/

É a pasta onde está todos os testes do programa, sendo os arquivos conftest.py um arquivos onde ficam as funções de configuração e que são reutilizadas por varios testes, além do factories.py que fica todas as funções de dados pre-configurado para os testes

#### test/controllers/

É a pasta onde fica os testes das rotas

#### auxia/schemas/

É a pasta onde fica os testes de validação dos esquemas de dados

#### auxia/usecases/

É a pasta onde fica os teste das funções de caso de uso, como criar um usuário no banco, buscar usuário no banco e etc, que testa se as funções estão tendo seu comportamento devido
