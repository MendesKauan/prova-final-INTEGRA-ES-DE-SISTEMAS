# Prova final da Materia de Integrações de Sistemas

### Positivo Osorio - 30/05/2025 
### Kauan Alexandre Mendes da Silva - RGM 28952782

##

Nesse projeto possuimos 3 APIs que consomem do **Redis** como cacheamento e do **RabbitMQ** para menssageria.

### 1º API - Modulo de Sensores (Node.js)
- Com os arquivos da aplicação em sua maquina, para subi-la basta rodar no terminal dentro do diretorio da aplicação: `npm run start`

- Temos a rota **GET `http://localhost:3000/sensor-data`**, que ao ser acionado ele envia dados simulados de temperatura e pressão

    ``` 
    Retorno:
    {
        "temperature": "38.50",
        "pressure": "709.40",
        "timestamp": "2025-05-31T00:26:07.586Z"
    }
- Temos uma segunda rota **`http://localhost:3000/alert`**. Utilizamos da biblioteca **AXIOS** para enviar alertas a API **Modulo de Eventos Criticos (Python)**

    É necessario passar, via **body** da requisição o JSON:
    `{ "alert" : "menssagem de alerta" }` 


