"""
Mock Spark - Simulated Spark processing for pipeline simulation.
"""

from __future__ import annotations

import statistics
from typing import Any


class FakeSparkJob:
    """
    Simulated Spark job for pipeline testing and simulation.
    
    Provides basic Spark job simulation without requiring an actual Spark cluster.
    """
    
    BASE_COMPUTE_TIME_MS = 100.0  # Base compute time in milliseconds
    
    def __init__(
        self,
        partitions: int = 200,
        records_per_partition: list[int] | None = None
    ) -> None:
        """
        Initialize a fake Spark job.
        
        Args:
            partitions: Number of partitions.
            records_per_partition: List of record counts per partition.
                                  If None, creates uniform distribution.
        """
        self.partitions = partitions
        
        if records_per_partition is None:
            # Default: uniform distribution (1000 records per partition)
            self.records_per_partition = [1000] * partitions
        else:
            if len(records_per_partition) != partitions:
                raise ValueError(
                    f"records_per_partition length ({len(records_per_partition)}) "
                    f"must match partitions ({partitions})"
                )
            self.records_per_partition = records_per_partition
    
    def run(self) -> dict[str, Any]:
        """
        Run the Spark job simulation.
        
        Calculates:
        - skew = stddev(records_per_partition)
        - shuffle_cost = partitions * 2
        - compute_time = base + skew*5 + shuffle_cost
        
        Returns:
            Dictionary with simulation metrics:
            {
                "latency_ms": compute_time,
                "cost_units": calculated cost,
                "throughput": calculated throughput,
                "warnings": [...]
            }
        """
        warnings: list[str] = []
        
        # Calculate skew as standard deviation of records per partition
        if len(self.records_per_partition) > 1:
            skew = statistics.stdev(self.records_per_partition)
        else:
            skew = 0.0
        
        # Calculate shuffle cost
        shuffle_cost = self.partitions * 2
        
        # Calculate compute time: base + skew*5 + shuffle_cost
        compute_time = self.BASE_COMPUTE_TIME_MS + (skew * 5.0) + shuffle_cost
        
        # Calculate total records
        total_records = sum(self.records_per_partition)
        
        # Calculate cost based on compute time and partitions
        # Cost increases with compute time and number of partitions
        cost_units = (compute_time / 1000.0) * (self.partitions / 100.0)
        
        # Calculate throughput (records per second)
        throughput = (total_records / (compute_time / 1000.0)) if compute_time > 0 else 0.0
        
        # Generate warnings
        if skew > 1000:
            warnings.append(
                f"High data skew detected (stddev={skew:.2f}) - "
                f"consider repartitioning for better performance"
            )
        
        if self.partitions < 10:
            warnings.append(
                f"Low partition count ({self.partitions}) - "
                f"may not utilize cluster efficiently"
            )
        
        if self.partitions > 1000:
            warnings.append(
                f"Very high partition count ({self.partitions}) - "
                f"may cause overhead"
            )
        
        # Check for empty partitions
        empty_partitions = sum(1 for r in self.records_per_partition if r == 0)
        if empty_partitions > 0:
            warnings.append(
                f"{empty_partitions} empty partition(s) detected - "
                f"consider coalescing"
            )
        
        # Check for very uneven distribution
        if len(self.records_per_partition) > 1:
            max_records = max(self.records_per_partition)
            min_records = min(self.records_per_partition)
            if min_records > 0 and max_records / min_records > 10:
                warnings.append(
                    f"Uneven partition distribution: "
                    f"max={max_records}, min={min_records} - "
                    f"consider repartitioning"
                )
        
        return {
            "latency_ms": compute_time,
            "cost_units": cost_units,
            "throughput": throughput,
            "warnings": warnings,
            "skew": skew,
            "shuffle_cost": shuffle_cost,
            "total_records": total_records,
        }
