# Generative AI HTTP Service🤖

## Objetivo🎯
Projeto desenvolvido com o intuito de facilitar e padronizar a utilização de chats de IA Generativa afim de processar grandes quantidades de dados.

# Documentação da API 📃

### Chats disponíveis:
- [Chat-GPT](https://chat.openai.com/) (gpt)

### Modelo de requisição

#### /{chat}/prompt 

Executa um prompt em um determinado chat e em seguida retorna o html do resultado.

##### Exemplo de Requisição:


````python
import requests

data = {
    'prompts': [
        { "prompt": 'Escreva um texto sobre cachorros'}
    ]
}

response = requests.post('https://api.domain/gpt/prompt', json=data)
````

##### Responses:

- 200
```json
{
    ...

    "response": {
        "content": "<p>Os cachorros são companheiros leais e amorosos. Com olhares ternos e caudas balançando, conquistam nossos corações. Seu instinto protetor e alegria contagiante fazem deles membros queridos da família. Cada latido é uma expressão de carinho, ensinando-nos sobre lealdade e gratidão.</p>",
        "tokens": 103
    }

    ...
}
```

- 503
```json
{
    "error": "Todos os nossos trabalhadores estão em repouso, tente novamente mais tarde. (- ｡ – ) zZz"
}
```

###### Template de resposta

````python
{
    'meta': { ... }
    'prompts': [
        {
            'content': str
            'tokens': int
        },
        ...
    ],
    'responses': [
        {
            'content': str
            'tokens': int
        },
        ...
    ]
}
````

#### /{chat}/scrapers

Retorna o estado dos scrapers que estão ativos em um determinado Chat.

##### Exemplo de requisição:

````python
import requests
response = requests.get('https://api.domain/gpt/scrapers')
````

##### Responses:

- 200
````json
[
    {
        "username": "scraper@email.com",
        "processing": true,
        "blocked": false
    },
    {
        "username": "scraper2@email.com",
        "processing": false,
        "blocked": true
    }
]
````

# Instalação ⚙
Para executar o projeto, siga os seguintes comandos:

* Instale o virtualenv
```sh
pip install virtualenv
```

* Crie um ambiente virtual
```sh
virtualenv venv 
```

* Ative o ambiente virtual
```sh
Scripts/Activate
```

* Instale as dependências
```sh
pip install requirements.txt
```

# Execução 👨‍💻

Na raiz do projeto execute o seguinte comando:

```sh
python app.py
```

# Entidades 🧱

**Trabalhador/Raspador**: `ChatScraper`. Entidade que manipula o front-end da IA Generativa afim de inserir dados para processamento e obtenção de dados processados pela IA. Podem existir 1 ou mais scrapers trabalhando simultaneamente.

**Configurador/Executador**: `ChatSetup`. Entidade que inicicializa todos os scrapers dos chats utilizando usuários do arquivo de `accounts`.

**Controlador**: `ChatController`. Entidade que recebe um `request` como entrega e retorna uma resposta para o usuário do serviço.

**Tokenizador**: `ChatTokenizer`. Entidade que converte um texto em [tokens](https://platform.openai.com/tokenizer) de processamento de IAs generativas.

# Estrutura de pastas 📁

**Chats**: Pasta onde ficam as instâncias de cada chat disponível no serviço.

**Controllers**: Pasta onde ficam todas as entidades `ChatController` de cada chat.

**Entities**: Pasta onde ficam todos os modelos de entidades disponíveis para implementação.

# Bibliotecas📚

#### ***Selenium*** 🚢
O Selenium em Python é uma biblioteca que permite a automação de ações em um navegador web. Ele é frequentemente utilizado para testes de software, scraping (extração de dados de websites) e automação de tarefas repetitivas que envolvem interações com páginas da web.

#### ***Undetected Chromedriver*** 🤐
O Undetected Chromedriver é uma extensão do Selenium para Python que oferece funcionalidades adicionais para tornar a automação web mais robusta e menos sujeita à detecção por parte dos websites.
