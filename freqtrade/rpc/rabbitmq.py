import json
from typing import Dict, Any

import pika

from freqtrade.rpc import RPC, RPCHandler


class RabbitMQ(RPCHandler):
    def __init__(self, rpc: 'RPC', config: Dict[str, Any]):
        super().__init__(rpc, config)

        self._host = self._config['rabbitmq']['host']

    def cleanup(self) -> None:
        pass

    def send_msg(self, msg: Dict[str, str]) -> None:
        conn_params = pika.ConnectionParameters(self._host)
        connection = pika.BlockingConnection(conn_params)
        channel = connection.channel()

        channel.queue_declare('freqtrade')
        channel.basic_publish(exchange='', routing_key='freqtrade', body=json.dumps(msg).encode('utf-8'))

        connection.close()
