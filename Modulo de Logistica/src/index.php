<?php
require_once __DIR__ . '/../vendor/autoload.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

header('Content-Type: application/json');

$requestUri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$method = $_SERVER['REQUEST_METHOD'];

$routes = [

    'GET' => [
        '/equipments' => function() {
            echo json_encode([
                ['id' => 'EQ001', 'name' => 'Bomba X', 'status' => 'Disponível'],
                ['id' => 'EQ002', 'name' => 'Válvula Y', 'status' => 'Em Manutenção']
            ]);
        }
    ],

    'POST' => [
        '/dispatch' => function() {
            $input = json_decode(file_get_contents('php://input'), true);
            $message = $input['message_urgent'];

            $connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
            $channel = $connection->channel();
            $channel->queue_declare('logistics_queue', false, true, false, false);

            $messageData = [
                'message_urgent' => $message
            ];
            
            $msg = new AMQPMessage(json_encode($messageData), array('delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT));

            $channel->basic_publish($msg, '', 'logistics_queue');
            echo json_encode(['message' => 'Mensagem de logística enviada.', 'data' => $messageData]);

            $channel->close();
            $connection->close();
        }
    ]
];


if (isset($routes[$method]) && isset($routes[$method][$requestUri])) {
    $routes[$method][$requestUri]();
}