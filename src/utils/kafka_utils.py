from confluent_kafka import Producer
import socket

def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Delivery failed: {err}")
    else:
        print(
            f"✅ Delivered to {msg.topic()} "
            f"[partition={msg.partition()}] "
            f"offset={msg.offset()}"
        )

def get_kafka_producer(bootstrap_servers="kafka:9092"):
    conf = {
        "bootstrap.servers": bootstrap_servers,
        "client.id": socket.gethostname(),
        "acks": "all",
        "enable.idempotence": True,
        "retries": 5,
        "linger.ms": 10,
        "delivery.timeout.ms": 120000
    }
    return Producer(conf), delivery_report
