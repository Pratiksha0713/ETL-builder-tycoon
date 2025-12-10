"""
Mock Kafka - Simulated Kafka streaming for pipeline simulation.
"""

from __future__ import annotations


class FakeKafka:
    """
    Simulated Kafka broker for pipeline testing and simulation.
    
    Provides basic produce/consume functionality without requiring
    an actual Kafka cluster.
    """
    
    def __init__(self, topic: str, partitions: int = 1) -> None:
        """
        Initialize a fake Kafka instance.
        
        Args:
            topic: The Kafka topic name.
            partitions: Number of partitions for the topic.
        """
        self.topic = topic
        self.partitions = partitions
    
    def produce(self, message: dict, key: str | None = None) -> None:
        """
        Produce a message to the topic.
        
        Args:
            message: The message payload to produce.
            key: Optional partition key.
        """
        pass
    
    def consume(self, timeout_ms: int = 1000) -> dict | None:
        """
        Consume a message from the topic.
        
        Args:
            timeout_ms: Maximum time to wait for a message.
            
        Returns:
            The consumed message, or None if no message available.
        """
        pass
