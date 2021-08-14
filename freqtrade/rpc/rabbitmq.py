import json
import ssl
from typing import Dict, Any

import pika

from freqtrade.rpc import RPC, RPCHandler


class RabbitMQ(RPCHandler):
    def __init__(self, rpc: 'RPC', config: Dict[str, Any]):
        super().__init__(rpc, config)

        self._host = self._config['rabbitmq']['host']
        self._username = self._config['rabbitmq']['username']
        self._password = self._config['rabbitmq']['password']

    def cleanup(self) -> None:
        pass

    def send_msg(self, msg: Dict[str, str]) -> None:
        credential = pika.credentials.PlainCredentials(self._username, self._password)
        context = ssl.create_default_context()
        ssl_option = pika.SSLOptions(context)
        conn_params = pika.ConnectionParameters(self._host, credentials=credential, port=5671, ssl_options=ssl_option)
        connection = pika.BlockingConnection(conn_params)
        channel = connection.channel()

        channel.queue_declare('freqtrade')
        channel.basic_publish(exchange='', routing_key='freqtrade', body=json.dumps(msg).encode('utf-8'))

        connection.close()
