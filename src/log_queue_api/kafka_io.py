from typing import List

from confluent_kafka.admin import AdminClient, NewTopic

from config_utils import get_config


def main():
    # create_topics()
    delete_topics()


def create_topics(topics: List[str] = None):
    """Create kafka topics.
    
    Link to documentation:
    - https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#confluent_kafka.admin.NewTopic
    - https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/adminapi.py
    """

    if topics is None:
        topics = ["user_events", "org_events"]

    topic_objects = [NewTopic(topic, 1) for topic in topics]

    admin = AdminClient(get_config())

    fs = admin.create_topics(topic_objects)

    for topic, f in fs.items():
        try:
            f.result()
            print(f"Create topic {topic}")
        except Exception as e:
            print(f"Failed to create topic {topic}: {e}")


def delete_topics(topics: List[str] = None):
    """Delete kafka topics.
    
    Compare to:
    - https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/adminapi.py#L51
    """

    if topics is None:
        topics = ["user_events", "org_events"]

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


if __name__ == "__main__":
    main()
