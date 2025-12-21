"""
Mock Kafka - Simulated Kafka streaming for pipeline simulation.
"""

from __future__ import annotations


class FakeKafka:
    """
    Simulated Kafka broker for pipeline testing and simulation.
    
    Provides basic Kafka simulation functionality without requiring
    an actual Kafka cluster.
    """
    
    def __init__(
        self,
        partitions: int = 1,
        events_per_second: float = 1000.0,
        consumer_speed: float = 1200.0
    ) -> None:
        """
        Initialize a fake Kafka instance.
        
        Args:
            partitions: Number of partitions for the topic.
            events_per_second: Simulated producer ingestion rate (events per second).
            consumer_speed: Consumer processing rate (events per second).
        """
        self.partitions = partitions
        self.events_per_second = events_per_second
        self.consumer_speed = consumer_speed
    
    def simulate_ingestion(self, seconds: float) -> dict[str, float | list[str]]:
        """
        Simulate ingesting events over a period of time.
        
        Calculates:
        - events_generated = events_per_second * seconds
        - events_consumed = consumer_speed * seconds
        - lag = max(0, events_generated - events_consumed)
        
        Args:
            seconds: Duration of the simulation in seconds.
            
        Returns:
            Dictionary with simulation metrics:
            {
                "latency_ms": lag * 0.1,
                "throughput": events_consumed,
                "cost_units": partitions * 0.05,
                "warnings": [...]
            }
        """
        warnings: list[str] = []
        
        # Calculate events generated and consumed
        events_generated = self.events_per_second * seconds
        events_consumed = self.consumer_speed * seconds
        lag = max(0, events_generated - events_consumed)
        
        # Generate warnings
        if lag > 0:
            warnings.append(f"Consumer lag detected: {lag:.0f} events behind")
        
        if self.consumer_speed < self.events_per_second:
            warnings.append(
                f"Consumer speed ({self.consumer_speed}/s) slower than producer "
                f"({self.events_per_second}/s) - lag will accumulate"
            )
        
        if self.partitions < 3 and self.events_per_second > 5000:
            warnings.append(
                f"High event rate ({self.events_per_second}/s) with few partitions "
                f"({self.partitions}) - consider increasing partitions for better parallelism"
            )
        
        # Calculate metrics
        latency_ms = lag * 0.1
        throughput = events_consumed
        cost_units = self.partitions * 0.05
        
        return {
            "latency_ms": latency_ms,
            "throughput": throughput,
            "cost_units": cost_units,
            "warnings": warnings,
        }
