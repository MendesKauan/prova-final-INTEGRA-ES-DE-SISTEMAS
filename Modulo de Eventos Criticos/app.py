from flask import Flask, request, jsonify
import redis
import json
import threading
import pika
import time

app = Flask(__name__)

# Configurações de serviços
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'guest'
RABBITMQ_PASS = 'guest'

# Redis Client
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
CACHE_KEY = 'events_cache' # Chave para o cache no Redis

# Lista local para armazenar eventos (como um backup/cache em memória)
message_node = []

# Funções de Conexão e Consumo RabbitMQ
def connect_rabbitmq():
    print("[*] Tentando conectar ao RabbitMQ...")
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        virtual_host='/',
        credentials=credentials,
        heartbeat=60
    )
    retries = 5
    while retries > 0:
        try:
            connection = pika.BlockingConnection(parameters)
            print("[x] Conectado ao RabbitMQ.")
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            print(f"[-] Erro ao conectar ao RabbitMQ: {e}. Tentando novamente em 5 segundos...")
            retries -= 1
            time.sleep(5)
    raise Exception("Não foi possível conectar ao RabbitMQ após várias tentativas.")

def logistics_callback(ch, method, properties, body):
    try:
        message = json.loads(body.decode('utf-8'))
        urgent_content = message.get('message_urgent', 'Conteúdo da mensagem urgente não disponível.')

        event_data = {
            "type": "Logistics_Update",
            "message": f"Logística: {urgent_content}",
            "details": message,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z")
        }
        print(f"[+] Mensagem de logística recebida: {message}")
        message_node.append(event_data)
        redis_client.lpush(CACHE_KEY, json.dumps(event_data))
        redis_client.expire(CACHE_KEY, 300) 

        ch.basic_ack(method.delivery_tag)
    except Exception as e:
        print(f"[-] Erro no callback de logística: {e}. Mensagem: {body.decode()}")
        ch.basic_nack(method.delivery_tag, requeue=False)

def alert_callback(ch, method, properties, body):
    try:
        alert_data = json.loads(body.decode('utf-8'))
        event_data = {
            "type": "Alert",
            "message": f"Alerta Crítico: {alert_data.get('alert_message', 'Mensagem de alerta não disponível.')}",
            "details": alert_data,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z")
        }
        print(f"[!] Alerta recebido: {alert_data}")
        message_node.append(event_data)
        redis_client.lpush(CACHE_KEY, json.dumps(event_data))
        redis_client.expire(CACHE_KEY, 300)
        ch.basic_ack(method.delivery_tag)
    except Exception as e:
        print(f"[-] Erro no callback de alerta: {e}. Mensagem: {body.decode()}")
        ch.basic_nack(method.delivery_tag, requeue=False)

def rabbitmq_consumer_thread():
    try:
        connection = connect_rabbitmq()
        channel = connection.channel()

        channel.queue_declare(queue='logistics_queue', durable=True)
        channel.queue_declare(queue='alert_queue', durable=True)

        channel.basic_consume(queue='logistics_queue', on_message_callback=logistics_callback)
        channel.basic_consume(queue='alert_queue', on_message_callback=alert_callback)

        channel.start_consuming()
 
    finally:
        if 'connection' in locals() and connection.is_open:
            print("[*] Fechando conexão com RabbitMQ.")
            connection.close()

consumer_thread = threading.Thread(target=rabbitmq_consumer_thread)
consumer_thread.daemon = True
consumer_thread.start()



@app.route('/event', methods=['POST'])
def receive_event():
    event = request.get_json()
    message_node.append(event)
    redis_client.lpush(CACHE_KEY, json.dumps(event))
    redis_client.expire(CACHE_KEY, 300)
    return jsonify({"message": "Evento recebido"}), 200


@app.route('/events', methods=['GET'])
def get_events():
    cached_events_json = redis_client.lrange(CACHE_KEY, 0, -1)
    if cached_events_json:
        events = [json.loads(e) for e in cached_events_json]
        return jsonify(events), 200
    return jsonify(message_node), 200 



if __name__ == '__main__':
    app.run(debug=True, port=5000)


