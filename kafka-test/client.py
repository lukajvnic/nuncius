from kafka import KafkaProducer, KafkaConsumer


def main():
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    while True:
        message = input("Enter message: ")
        producer.send('test-topic', message.encode('utf-8'))
        producer.flush()


main()
# consumer = KafkaConsumer('test-topic', bootstrap_servers='localhost:9092', auto_offset_reset='earliest')
# for msg in consumer:
#     print(msg.value)