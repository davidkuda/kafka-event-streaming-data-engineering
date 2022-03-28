# Kafka Commands

```sh
# cd into dir where Kafka binaries were downloaded:
cd $HOME/dev/kafka/kafka_2.13-3.1.0

# start zookeeper:
bin/zookeeper-server-start.sh config/zookeeper.properties

# start the Kafka broker service:
bin/kafka-server-start.sh config/server.properties

# or alternatively:
docker run -it --rm \
  --entrypoint kafka/bin/zookeeper-server-start.sh \
  kafka-arm \
    kafka/config/zookeeper.properties

docker run -it --rm \
  --entrypoint bin/kafka-server-start.sh \
  kafka-arm \
    config/server.properties

# set shortcut for cmd:
alias k=$(pwd)/bin/kafka-topics.sh

# Print help:
bin/kafka-topics.sh

# List existing topics:
bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# Create a new topic:
bin/kafka-topics.sh \
  --create --topic quickstart-events \
  --bootstrap-server localhost:9092

# Write event to topic:
bin/kafka-console-producer.sh \
  --topic quickstart-events \
  --bootstrap-server localhost:9092

# Read events from a topic:
bin/kafka-console-consumer.sh \
  --topic quickstart-events \
  --from-beginning \
  --bootstrap-server localhost:9092
```


## From confluent python guide

src: https://developer.confluent.io/get-started/python/#create-topic

```
bin/kafka-topics.sh --create \
  --topic purchases \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 1
```
