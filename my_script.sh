# Ip @ 192.168.137.181

# Kafka Setup
# Navigate to the Kafka directory
cd kafka_2.13-3.6.0

# Start the Zookeeper server
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start the Kafka server
bin/kafka-server-start.sh config/server.properties

# Create the "gazData" topic with 1 partition and a replication factor of 1
bin/kafka-topics.sh --create --topic gazData --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

# Using a Virtual Environment
# Activate your virtual environment
source /home/fahym/myenv/bin/activate

# Run the program that sends gas sensor values to Kafka
(myenv) fahym@raspberrypi:~ $ python3 gaz_sensor_to_kafka.py

# Verify that Kafka has successfully received the gas sensor data
cd kafka_2.13-3.6.0/bin
fahym@raspberrypi:~/kafka_2.13-3.6.0/bin $
./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic gazData --from-beginning

# Run the program that initiates a 0.01 Ethereum transaction from the company's account to the association's account
# Activate your virtual environment again
source /home/fahym/myenv/bin/activate

# Run the Ethereum transaction program
(myenv) fahym@raspberrypi:~ $ python3 web3_a_to_b.py


python3 gaz_sensor_to_kafka.py
python3 web3_a_to_b.py