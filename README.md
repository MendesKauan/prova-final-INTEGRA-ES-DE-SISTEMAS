# Prova final da Materia de Integrações de Sistemas

### Positivo Osorio - 30/05/2025 
### Kauan Alexandre Mendes da Silva - RGM 28952782

##

Nesse projeto possuimos 3 APIs que consomem do **Redis** como cacheamento e do **RabbitMQ** para menssageria.

Mas antes de subir as aplicações, execute o docker-compose que contém essas duas ferramentas.
Basta executar `docker-compose up -d` no diretorio que contém o arquvio do docker

##

### 1º API - Modulo de Sensores (Node.js e Express)
- Com os arquivos da aplicação em sua maquina, o Redis e o RabbitMQ rodando. Para subir o **Modulo de Sensores** basta rodar no terminal dentro do diretorio da aplicação `(\pasta_repositorio\Modulo de Sensores)` o seguinte comando: `npm install` para baixar as dependencias e depois, para subir o servidor: `npm run start`.

- Temos a rota **GET - `http://localhost:3000/sensor-data`**, que ao ser acionado ele envia dados simulados de temperatura e pressão:

    ``` 
    Exemplo de retorno:
    {
        "temperature": "38.50",
        "pressure": "709.40",
        "timestamp": "2025-05-31T00:26:07.586Z"
    }
    ```
    Após o envio desses dados ao solicitante, armazenamos a resposta no Redis. Caso o endpoint seja acionado logo em seguida, ele vai primeiro no Redis, antes de acionar a função novamente, tornando o retorno mais rapido! 

- Temos uma segunda rota **POST - `http://localhost:3000/alert`**. Utilizamos da biblioteca **AXIOS** para enviar alertas a API **Modulo de Eventos Criticos** por meio da função `axios.post(rota, dados)`

    É necessario passar, via **body** da requisição o JSON com a mensagem do alerta:
    `{ "alert" : "menssagem de alerta" }` 

    ##

### 2º API - Modulo de Eventos Criticos (Python e Flask)
    
- Para subir esse serviço, precisamos utilizar de um ambiente virtual do Python. Para isso, na pasta da aplicação `(\pasta_repositorio\Modulo de Eventos Criticos)` via terminal executamos: `python -m venv venv`. E depois entramos nesse ambiente: `.\venv\Scripts\Activate.ps1`.

- Já no ambiente virtual, instalamos as dependencias: `pip install -r requirements.txt`, e subimos a aplicação: `python app.py`

- Na primeira parte do código, é configurado os acessos ao Redis e ao RabbitMQ. Logo em seguida definimos funções para se conectar e consumir as menssagens vindas do Rabbitmq. 

    Quando a API de Modulo de Logistica realiza envios de menssagens, a função `logistics_callback()` consome essas menssagens e as armazena no Redis

- Abaixo, temos o endpoint **POST - `http://localhost:5000/event`** que recebe as menssagens enviadas pela API **Modulo de Sensores** e armazena essas menssagens num array e no Redis  

    Para testar sem a utilização da API em Node, passe via Body: `{ "alert" : "menssagem de alerta" }` . Resposta esperada: `{ "message": "Evento recebido" }` 

- Por fim, temos o endpoint **GET - `http://localhost:5000/events`** que ao ser acionada retorna todas as informações salvas, tanto as menssagens vindas da API em Node, quanto da fila do RabbitMQ.

    ##

### 3º API - Modulo de Logistica (PHP e Composer)

- Para o servidor em PHP subir, no diretorio da aplicação `(\pasta_repositorio\Modulo de Logistica)` rodamos o comando **`php -S 0.0.0.0:8000 -t .\src`**

- O primeiro endpoint **GET - `http://localhost:8000/equipments`** ao ser acionado, ele envia dados simulados de equipamentos e seus status. **Retorno esperado:**

``` 
    {   
        "id": "EQ001",
        "name": "Bomba X",
        "status": "Disponível"
    },
    {
        "id": "EQ002",
        "name": "Válvula Y",
        "status": "Em Manutenção"
    }
```
- O segundo endpoint **POST - `http://localhost:8000/dispatch`**, serve para publicar as menssagens na fila do RabbitMQ **logistics_queue**.

    Com o RabbitMQ rodando localmente, conseguimos acessar o portal gerado pelo link http://localhost:15672 e colocar em Username e Password a palavra **guest**, conforme declarado na função `$connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');`

    Nesse portal conseguimos vizualizar as filas, os canais e as conexões.




