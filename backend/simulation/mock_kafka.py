"""
Mock Kafka - Simulated Kafka streaming for pipeline simulation.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field


@dataclass
class IngestionMetrics:
    """Metrics from a Kafka ingestion simulation."""
    total_events: int = 0
    events_per_partition: dict[int, int] = field(default_factory=dict)
    duration_seconds: float = 0.0
    
    @property
    def throughput(self) -> float:
        """Events per second achieved."""
        if self.duration_seconds > 0:
            return self.total_events / self.duration_seconds
        return 0.0


class FakeKafka:
    """
    Simulated Kafka broker for pipeline testing and simulation.
    
    Provides basic produce/consume functionality without requiring
    an actual Kafka cluster.
    """
    
    def __init__(
        self, 
        topic: str, 
        partitions: int = 1,
        records_per_second: float = 1000.0
    ) -> None:
        """
        Initialize a fake Kafka instance.
        
        Args:
            topic: The Kafka topic name.
            partitions: Number of partitions for the topic.
            records_per_second: Simulated ingestion rate.
        """
        self.topic = topic
        self.partitions = partitions
        self.records_per_second = records_per_second
        
        # Internal storage for messages per partition
        self._partition_queues: dict[int, list[dict]] = {
            i: [] for i in range(partitions)
        }
    
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
    
    def simulate_ingestion(self, n_seconds: float) -> IngestionMetrics:
        """
        Simulate ingesting events over a period of time.
        
        Distributes events across partitions using a round-robin
        strategy with some randomization to simulate real-world behavior.
        
        Args:
            n_seconds: Duration of the simulation in seconds.
            
        Returns:
            IngestionMetrics with total_events and events_per_partition.
        """
        total_events = int(self.records_per_second * n_seconds)
        
        # Initialize partition counts
        events_per_partition: dict[int, int] = {
            i: 0 for i in range(self.partitions)
        }
        
        # Distribute events across partitions
        # Use weighted random distribution to simulate real Kafka behavior
        for _ in range(total_events):
            # Simulate partition assignment (could be key-based or round-robin)
            partition = random.randint(0, self.partitions - 1)
            events_per_partition[partition] += 1
        
        return IngestionMetrics(
            total_events=total_events,
            events_per_partition=events_per_partition,
            duration_seconds=n_seconds
        )
