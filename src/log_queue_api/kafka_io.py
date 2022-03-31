import json
from typing import List, Callable
from pprint import pprint
from datetime import datetime

from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer, Consumer

from .config_utils import get_config, get_consumer_config


def create_topics(topics: List[str]):
    """Create kafka topics.

    Link to documentation:
    - https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#confluent_kafka.admin.NewTopic
    - https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/adminapi.py
    """
    topic_objects = [NewTopic(topic, 1) for topic in topics]

    admin = AdminClient(get_config())

    fs = admin.create_topics(topic_objects)

    for topic, f in fs.items():
        try:
            f.result()
            print(f"Create topic {topic}")
        except Exception as e:
            print(f"Failed to create topic {topic}: {e}")


def list_topics():
    """List all topics.
    
    https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#confluent_kafka.admin.AdminClient.list_topics
    """
    admin = AdminClient(get_config())
    topics = admin.list_topics().topics
    if topics is None:
        print("There are no topics yet in Kafka!")
    else:
        pprint(topics)


def push(topic: str, key, value):
    """Publish new content to a topic."""
    # Create Producer instance
    producer = Producer(get_config())

    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    def delivery_callback(err, msg):
        if err:
            print(f"ERROR: Message failed delivery: {err}")
        else:
            print(
                f"Produced event to topic {msg.topic()}:\n",
                f"\tkey = {msg.key().decode('utf-8')}\n",
                f"\tvalue = {msg.value().decode('utf-8')}",
            )

    # producer.produce(topic, value, key, callback=delivery_callback)
    producer.produce(topic, value, key)

    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()


def subscribe(topic: str, function: Callable = None, *args, **kwargs):
    consumer: Consumer = Consumer(get_consumer_config())
    consumer.subscribe([topic])

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = consumer.poll(2.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting...")
            elif msg.error():
                print("ERROR: %s".format(msg.error()))
            else:
                # Extract the (optional) key and value, and print.
                print(f"Consumed event from topic {msg.topic()}: key={msg.key().decode('utf-8')}, value:")
                v = msg.value().decode("utf-8")
                pprint(json.loads(v))
                print("")
                if function:
                    function(v)
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()


def subscribe_count_unique_visitors():
    consumer: Consumer = Consumer(get_consumer_config())
    consumer.subscribe(["website_visits"])
    
    # ? How could you pass these outter scope values as args in order to make function generic?
    window = {}
    window_count = 0
    previous_ts: int = 1

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                pass

            elif msg.error():
                print("ERROR: %s".format(msg.error()))

            else:
                v = msg.value().decode("utf-8")
                d = json.loads(v)
                ts = d["ts"]
                uid = d["uid"]

                # utc_ts = datetime.utcfromtimestamp(ts)
                # print(utc_ts, "Consuming new message")
    
                if ts % 60 != 0:
                    if window.get(uid):
                        continue
                    window[uid] = 1
                    window_count += 1

                if ts % 60 == 0 and ts - previous_ts != 0:
                    print("A minute finished:")
                    utc_ts = datetime.utcfromtimestamp(ts)
                    print("date: ", utc_ts)
                    print("count: ", window_count)
                    print("")
                    data = json.dumps({
                        "datetime": ts, 
                        "count": window_count
                    })
                    window = {}
                    window_count = 0
                    previous_ts = ts
                    push("visits_per_minute", str(utc_ts), data)

    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()


def delete_topics(topics: List[str]):
    """Delete kafka topics.

    Compare to:
    - https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/adminapi.py#L51
    """
    admin = AdminClient(get_config())

    # Call delete_topics to asynchronously delete topics, a future is returned.
    # By default this operation on the broker returns immediately while
    # topics are deleted in the background. But here we give it some time (30s)
    # to propagate in the cluster before returning.
    #
    # Returns a dict of <topic,future>.
    fs = admin.delete_topics(topics, operation_timeout=30)

    # Wait for operation to finish.
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print(f"Topic {topic} deleted")
        except Exception as e:
            print(f"Failed to delete topic {topic}: {e}")
