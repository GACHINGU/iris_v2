from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers="localhost:9092")

# Creating a pigeon-hole for Kafka as the postoffice, and also the content inside the mail letter
# the b in these line of code makes the content the sender of the mail is sending ro be in raw bytes cause thats the only thing the Kafka understands
producer.send("cbr-events", b"Hello Zookeeper, Kafka is alive")

#  making sure that the message is actually sent and not sitting in the mail box
producer.flush()
