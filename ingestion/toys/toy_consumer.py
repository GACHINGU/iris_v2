from kafka import KafkaConsumer

#  the reciever standing at the post office should know which pigeon hole to put to collect the mail
#  "localhost:9092"since these data transfer is happening within my local machine which is outside Kafka
consumer = KafkaConsumer(
    "cbr-events", bootstrap_servers="localhost:9092", auto_offset_reset="earliest"
)

# the reciever
for message in consumer:
    print(message.value)
