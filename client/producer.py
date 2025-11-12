from kafka import KafkaProducer
import json
from constants import *

producer = KafkaProducer(bootstrap_servers='localhost:9092')


def produce_message(username: str, message: str):
    payload = {
        "username": username,
        "message": message  # in the future, add message in everyones pubkey
    }

    producer.send(MESSAGES_TOPIC, json.dumps(payload).encode('utf-8'))
    producer.flush()
