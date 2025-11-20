from kafka import KafkaProducer
import json
from constants import *
import encryption
import keys

producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_ADDRESS)


def produce_message(username: str, message: str, maxlen: int):
    pubkeys = keys.get_pubkeys()

    if len(message) > maxlen:
        message = message[:maxlen]  # truncate message if its too large for RSA

    # encrypt the message for each recipient with their public key
    payload = {
        "username": username,
        "messages": {user: encryption.encrypt(message, encryption.Pubkey(pubkey["n"], pubkey["e"])) for user, pubkey in pubkeys.items()}
    }

    producer.send(MESSAGES_TOPIC, json.dumps(payload).encode('utf-8'))
    producer.flush()
