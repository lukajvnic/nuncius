from kafka import KafkaConsumer
import json
from constants import *
from datetime import datetime
from zoneinfo import ZoneInfo


def consume_messages(cli):
    consumer = KafkaConsumer(
        MESSAGES_TOPIC,
        bootstrap_servers="localhost:9092",
    )

    try:
        while True:
            if getattr(cli, "SESSION", None) and cli.SESSION.killed:
                break

            records = consumer.poll(timeout_ms=500)  # returns a dict of partitions -> records
            if not records:
                continue

            for tp, msgs in records.items():
                for record in msgs:
                    raw = record.value
                    payload = json.loads(raw.decode("utf-8")) if isinstance(raw, (bytes, bytearray)) else json.loads(raw)
                    cli.provide_message(payload["username"],
                                        datetime.now(ZoneInfo("America/New_York")).strftime("%H:%M:%S"),
                                        payload["message"])

    except KeyboardInterrupt:
        print("[consumer] interrupted by user, exiting")
    finally:
        consumer.close()