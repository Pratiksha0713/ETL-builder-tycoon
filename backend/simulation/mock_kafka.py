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


@dataclass
class LagMetrics:
    """Metrics for consumer lag simulation."""
    total_lag: int = 0
    lag_per_partition: dict[int, int] = field(default_factory=dict)
    time_to_catch_up_seconds: float = 0.0
    is_falling_behind: bool = False


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
        records_per_second: float = 1000.0,
        consumer_speed: float = 1200.0
    ) -> None:
        """
        Initialize a fake Kafka instance.
        
        Args:
            topic: The Kafka topic name.
            partitions: Number of partitions for the topic.
            records_per_second: Simulated producer ingestion rate.
            consumer_speed: Consumer processing rate (records per second).
        """
        self.topic = topic
        self.partitions = partitions
        self.records_per_second = records_per_second
        self.consumer_speed = consumer_speed
        
        # Internal storage for messages per partition
        self._partition_queues: dict[int, list[dict]] = {
            i: [] for i in range(partitions)
        }
        
        # Track produced and consumed offsets per partition
        self._produced_offsets: dict[int, int] = {
            i: 0 for i in range(partitions)
        }
        self._consumed_offsets: dict[int, int] = {
            i: 0 for i in range(partitions)
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
            self._produced_offsets[partition] += 1
        
        # Simulate consumer processing during the same period
        consumed_total = int(self.consumer_speed * n_seconds)
        consumed_per_partition = consumed_total // self.partitions
        
        for partition in range(self.partitions):
            # Consumer can't consume more than what's been produced
            max_consumable = self._produced_offsets[partition] - self._consumed_offsets[partition]
            actual_consumed = min(consumed_per_partition, max_consumable)
            self._consumed_offsets[partition] += actual_consumed
        
        return IngestionMetrics(
            total_events=total_events,
            events_per_partition=events_per_partition,
            duration_seconds=n_seconds
        )
    
    def compute_lag(self) -> LagMetrics:
        """
        Compute the current consumer lag across all partitions.
        
        Lag is the difference between produced records and consumed records.
        A positive lag means the consumer is behind the producer.
        
        Returns:
            LagMetrics with total_lag and lag_per_partition in records.
        """
        lag_per_partition: dict[int, int] = {}
        total_lag = 0
        
        for partition in range(self.partitions):
            partition_lag = (
                self._produced_offsets[partition] - 
                self._consumed_offsets[partition]
            )
            lag_per_partition[partition] = max(0, partition_lag)
            total_lag += lag_per_partition[partition]
        
        # Calculate time to catch up (if consumer is faster than producer)
        is_falling_behind = self.consumer_speed <= self.records_per_second
        
        if is_falling_behind:
            # Consumer will never catch up
            time_to_catch_up = float('inf')
        elif total_lag == 0:
            time_to_catch_up = 0.0
        else:
            # Net processing rate (how fast we're catching up)
            net_rate = self.consumer_speed - self.records_per_second
            time_to_catch_up = total_lag / net_rate
        
        return LagMetrics(
            total_lag=total_lag,
            lag_per_partition=lag_per_partition,
            time_to_catch_up_seconds=time_to_catch_up,
            is_falling_behind=is_falling_behind
        )
    
    def reset_offsets(self) -> None:
        """Reset all produced and consumed offsets to zero."""
        self._produced_offsets = {i: 0 for i in range(self.partitions)}
        self._consumed_offsets = {i: 0 for i in range(self.partitions)}
