from typing import List

from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer

from .config_utils import get_config


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

    producer.produce(topic, value, key, callback=delivery_callback)

    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()


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
