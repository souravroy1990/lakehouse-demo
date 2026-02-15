import os
import json, time, random
from datetime import datetime
from faker import Faker
from utils.kafka_utils import get_kafka_producer

fake = Faker()
producer = get_kafka_producer("kafka:9092")

TOPIC = os.getenv("KAFKA_TOPIC", "fake-data-topic")

def generate_trade():
    return {
        "trade_id": fake.uuid4(),
        "symbol": random.choice(["INFY", "TCS", "RELIANCE", "HDFCBANK"]),
        "price": round(random.uniform(1000, 2500), 2),
        "volume": random.randint(10, 1000),
        "trade_time": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    print("Starting fake trade data generator...")
    while True:
        trade = generate_trade()
        producer.produce(TOPIC, json.dumps(trade).encode("utf-8"))
        producer.poll(0)
        print(f"Produced: {trade}")
        time.sleep(5) # Sleep for 5 seconds before generating the next trade
