"""
Mock Kafka - Simulated Kafka streaming for pipeline simulation.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field


@dataclass
class SimulationMetrics:
    """Standard metrics returned by all simulation classes."""
    latency_ms: float = 0.0
    cost_units: float = 0.0
    throughput: float = 0.0
    warnings: list[str] = field(default_factory=list)


@dataclass
class IngestionMetrics(SimulationMetrics):
    """Metrics from a Kafka ingestion simulation."""
    total_events: int = 0
    events_per_partition: dict[int, int] = field(default_factory=dict)
    duration_seconds: float = 0.0


@dataclass
class LagMetrics(SimulationMetrics):
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
    
    # Cost simulation constants
    COST_PER_1K_MESSAGES = 0.01  # Cost units per 1000 messages
    BASE_LATENCY_MS = 5.0  # Base produce/consume latency
    LATENCY_PER_PARTITION_MS = 0.5  # Additional latency per partition
    
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
    
    def _calculate_latency(self) -> float:
        """Calculate simulated latency based on partition count."""
        return self.BASE_LATENCY_MS + (self.partitions * self.LATENCY_PER_PARTITION_MS)
    
    def _calculate_cost(self, num_messages: int) -> float:
        """Calculate cost units for a number of messages."""
        return (num_messages / 1000.0) * self.COST_PER_1K_MESSAGES
    
    def produce(self, message: dict, key: str | None = None) -> SimulationMetrics:
        """
        Produce a message to the topic.
        
        Args:
            message: The message payload to produce.
            key: Optional partition key.
            
        Returns:
            SimulationMetrics with latency, cost, throughput, and warnings.
        """
        warnings: list[str] = []
        
        # Determine partition
        if key:
            partition = hash(key) % self.partitions
        else:
            partition = random.randint(0, self.partitions - 1)
        
        self._partition_queues[partition].append(message)
        self._produced_offsets[partition] += 1
        
        latency_ms = self._calculate_latency()
        cost_units = self._calculate_cost(1)
        
        return SimulationMetrics(
            latency_ms=latency_ms,
            cost_units=cost_units,
            throughput=1.0 / (latency_ms / 1000.0) if latency_ms > 0 else 0.0,
            warnings=warnings
        )
    
    def consume(self, timeout_ms: int = 1000) -> tuple[dict | None, SimulationMetrics]:
        """
        Consume a message from the topic.
        
        Args:
            timeout_ms: Maximum time to wait for a message.
            
        Returns:
            Tuple of (message or None, SimulationMetrics).
        """
        warnings: list[str] = []
        message = None
        
        # Try to consume from any partition with messages
        for partition in range(self.partitions):
            queue = self._partition_queues[partition]
            if queue:
                message = queue.pop(0)
                self._consumed_offsets[partition] += 1
                break
        
        if message is None:
            warnings.append(f"No messages available within {timeout_ms}ms timeout")
        
        latency_ms = self._calculate_latency()
        cost_units = self._calculate_cost(1 if message else 0)
        
        metrics = SimulationMetrics(
            latency_ms=latency_ms,
            cost_units=cost_units,
            throughput=1.0 / (latency_ms / 1000.0) if latency_ms > 0 else 0.0,
            warnings=warnings
        )
        
        return message, metrics
    
    def simulate_ingestion(self, n_seconds: float) -> IngestionMetrics:
        """
        Simulate ingesting events over a period of time.
        
        Distributes events across partitions using a round-robin
        strategy with some randomization to simulate real-world behavior.
        
        Args:
            n_seconds: Duration of the simulation in seconds.
            
        Returns:
            IngestionMetrics with total_events, events_per_partition, and standard metrics.
        """
        warnings: list[str] = []
        total_events = int(self.records_per_second * n_seconds)
        
        # Initialize partition counts
        events_per_partition: dict[int, int] = {
            i: 0 for i in range(self.partitions)
        }
        
        # Distribute events across partitions
        for _ in range(total_events):
            partition = random.randint(0, self.partitions - 1)
            events_per_partition[partition] += 1
            self._produced_offsets[partition] += 1
        
        # Simulate consumer processing during the same period
        consumed_total = int(self.consumer_speed * n_seconds)
        consumed_per_partition = consumed_total // self.partitions
        
        for partition in range(self.partitions):
            max_consumable = self._produced_offsets[partition] - self._consumed_offsets[partition]
            actual_consumed = min(consumed_per_partition, max_consumable)
            self._consumed_offsets[partition] += actual_consumed
        
        # Check for imbalanced partitions
        if events_per_partition:
            max_events = max(events_per_partition.values())
            min_events = min(events_per_partition.values())
            if max_events > min_events * 1.5:
                warnings.append("Partition imbalance detected: some partitions have 50%+ more events")
        
        # Check if consumer is falling behind
        if self.consumer_speed < self.records_per_second:
            warnings.append(f"Consumer speed ({self.consumer_speed}/s) slower than producer ({self.records_per_second}/s)")
        
        latency_ms = self._calculate_latency() * n_seconds
        cost_units = self._calculate_cost(total_events)
        throughput = total_events / n_seconds if n_seconds > 0 else 0.0
        
        return IngestionMetrics(
            latency_ms=latency_ms,
            cost_units=cost_units,
            throughput=throughput,
            warnings=warnings,
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
            LagMetrics with total_lag, lag_per_partition, and standard metrics.
        """
        warnings: list[str] = []
        lag_per_partition: dict[int, int] = {}
        total_lag = 0
        
        for partition in range(self.partitions):
            partition_lag = (
                self._produced_offsets[partition] - 
                self._consumed_offsets[partition]
            )
            lag_per_partition[partition] = max(0, partition_lag)
            total_lag += lag_per_partition[partition]
        
        # Calculate time to catch up
        is_falling_behind = self.consumer_speed <= self.records_per_second
        
        if is_falling_behind:
            time_to_catch_up = float('inf')
            warnings.append("Consumer will never catch up - speed <= producer rate")
        elif total_lag == 0:
            time_to_catch_up = 0.0
        else:
            net_rate = self.consumer_speed - self.records_per_second
            time_to_catch_up = total_lag / net_rate
        
        # Lag warnings
        if total_lag > 10000:
            warnings.append(f"High lag detected: {total_lag} messages behind")
        elif total_lag > 1000:
            warnings.append(f"Moderate lag: {total_lag} messages behind")
        
        latency_ms = self._calculate_latency()
        cost_units = 0.0  # Lag computation is free
        throughput = self.consumer_speed
        
        return LagMetrics(
            latency_ms=latency_ms,
            cost_units=cost_units,
            throughput=throughput,
            warnings=warnings,
            total_lag=total_lag,
            lag_per_partition=lag_per_partition,
            time_to_catch_up_seconds=time_to_catch_up,
            is_falling_behind=is_falling_behind
        )
    
    def reset_offsets(self) -> None:
        """Reset all produced and consumed offsets to zero."""
        self._produced_offsets = {i: 0 for i in range(self.partitions)}
        self._consumed_offsets = {i: 0 for i in range(self.partitions)}
        self._partition_queues = {i: [] for i in range(self.partitions)}
