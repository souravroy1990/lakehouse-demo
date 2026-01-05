from confluent_kafka import Producer
import socket

def get_kafka_producer(bootstrap_servers="localhost:9092"):
    conf = {
        'bootstrap.servers': bootstrap_servers,
        'client.id': socket.gethostname()
    }
    return Producer(conf)
