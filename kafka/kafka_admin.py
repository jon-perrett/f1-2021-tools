import os
from confluent_kafka.admin import AdminClient, NewTopic
import time


class KafkaAdmin:
    """A wrapper class for confluent_kafka.admin.AdminClient for doing common admin tasks"""

    def __init__(self, config):
        self.admin_client = AdminClient(config)

    def check_topic(
        self, topic_name: str, n_timeouts: int = 3, timeout_interval: int = 3
    ) -> bool:
        """Method to check if a topic exists within the kafka instance

        Args:
            topic_name (str): name of topic to check
            n_timeouts (int, optional): Number of timed out attempts to allow. Defaults to 3.
            timeout_interval (int, optional): Lengfth of timeout in seconds. Defaults to 3.

        Returns:
            bool: [description]
        """
        attempts = 0
        while attempts < n_timeouts:
            if topic_name in self.admin_client.list_topics().topics:
                print(f"Topic {topic_name} exists")
                return True
            time.sleep(timeout_interval)
            print(
                f"Topic {topic_name} doesn't exist. Checking again in {timeout_interval}"
            )
            attempts += 1
        print(f"Failed to find topic {topic_name} after {n_timeouts} attempts.")
        return False

    def add_topic(self, topic_name: str) -> bool:
        """Adds a topic to the Kafka instance, checking whether or not the topic was created.

        Args:
            topic_name (str): the name of the topic to add

        Returns:
            bool: whether or not the topic was successfully added
        """
        topic_list = []
        topic_list.append(NewTopic(topic_name, 1, 1))
        self.admin_client.create_topics(topic_list)
        return self.check_topic(topic_name)

    def check_add_topic(self, topic_name: str) -> bool:
        if self.check_topic(topic_name, 0, 0):
            print(f"Topic {topic_name} already exists")
            return True
        if self.add_topic(topic_name):
            print(f"{topic_name} created successfully")
            return True
        return False


if __name__ == "__main__":
    config = {"bootstrap.servers": os.getenv('BOOTSTRAP_SERVERS')}
    kafka = KafkaAdmin(config)
    kafka.check_add_topic("hello_world")
