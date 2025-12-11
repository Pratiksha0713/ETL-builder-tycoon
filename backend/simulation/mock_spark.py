"""
Mock Spark - Simulated Spark processing for pipeline simulation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class SparkOperation(Enum):
    """Types of Spark operations."""
    MAP = "map"
    FILTER = "filter"
    REDUCE = "reduce"
    JOIN = "join"
    GROUP_BY = "group_by"
    SORT = "sort"
    AGGREGATE = "aggregate"
    WINDOW = "window"


@dataclass
class SimulationMetrics:
    """Standard metrics returned by all simulation classes."""
    latency_ms: float = 0.0
    cost_units: float = 0.0
    throughput: float = 0.0
    warnings: list[str] = field(default_factory=list)


@dataclass
class SparkMetrics(SimulationMetrics):
    """Metrics from a Spark job execution."""
    rows_processed: int = 0
    partitions_used: int = 0
    shuffle_bytes: int = 0
    spill_bytes: int = 0
    stages_completed: int = 0
    tasks_completed: int = 0


@dataclass
class SparkJob:
    """Represents a Spark job configuration."""
    name: str
    operations: list[SparkOperation] = field(default_factory=list)
    input_rows: int = 0
    partitions: int = 200  # Default Spark partitions
    executor_memory_gb: float = 4.0
    executor_cores: int = 2
    num_executors: int = 2


class FakeSpark:
    """
    Simulated Spark cluster for pipeline testing and simulation.
    
    Provides basic Spark functionality simulation for testing
    pipelines without requiring an actual Spark cluster.
    """
    
    # Cost simulation constants
    COST_PER_EXECUTOR_HOUR = 0.10  # Cost units per executor per hour
    COST_PER_SHUFFLE_GB = 0.01  # Cost units per GB shuffled
    
    # Latency simulation constants (milliseconds)
    BASE_LATENCY_MS = 500.0  # Job startup overhead
    LATENCY_PER_STAGE_MS = 100.0  # Per-stage overhead
    LATENCY_PER_MILLION_ROWS_MS = 50.0  # Processing time per million rows
    
    # Operation complexity multipliers
    OPERATION_COMPLEXITY: dict[SparkOperation, float] = {
        SparkOperation.MAP: 1.0,
        SparkOperation.FILTER: 0.8,
        SparkOperation.REDUCE: 1.5,
        SparkOperation.JOIN: 3.0,
        SparkOperation.GROUP_BY: 2.0,
        SparkOperation.SORT: 2.5,
        SparkOperation.AGGREGATE: 1.8,
        SparkOperation.WINDOW: 2.5,
    }
    
    def __init__(
        self, 
        app_name: str = "FakeSparkApp",
        default_parallelism: int = 200
    ) -> None:
        """
        Initialize a fake Spark session.
        
        Args:
            app_name: The Spark application name.
            default_parallelism: Default number of partitions.
        """
        self.app_name = app_name
        self.default_parallelism = default_parallelism
        self._jobs_executed: list[SparkJob] = []
    
    def _calculate_complexity(self, operations: list[SparkOperation]) -> float:
        """Calculate total complexity multiplier for operations."""
        if not operations:
            return 1.0
        return sum(self.OPERATION_COMPLEXITY.get(op, 1.0) for op in operations)
    
    def _estimate_shuffle(self, job: SparkJob) -> int:
        """Estimate shuffle bytes based on operations."""
        shuffle_ops = {SparkOperation.JOIN, SparkOperation.GROUP_BY, 
                       SparkOperation.SORT, SparkOperation.REDUCE}
        
        shuffle_count = sum(1 for op in job.operations if op in shuffle_ops)
        
        # Estimate ~100 bytes per row per shuffle operation
        return job.input_rows * 100 * shuffle_count
    
    def _estimate_stages(self, operations: list[SparkOperation]) -> int:
        """Estimate number of stages based on operations."""
        # Shuffle operations create stage boundaries
        shuffle_ops = {SparkOperation.JOIN, SparkOperation.GROUP_BY, 
                       SparkOperation.SORT, SparkOperation.REDUCE}
        
        stages = 1  # At least one stage
        stages += sum(1 for op in operations if op in shuffle_ops)
        return stages
    
    def _generate_warnings(self, job: SparkJob, metrics: SparkMetrics) -> list[str]:
        """Generate warnings based on job characteristics."""
        warnings: list[str] = []
        
        # Check for potential issues
        if job.input_rows > 1_000_000_000:
            warnings.append("Very large dataset (>1B rows) - consider incremental processing")
        
        if metrics.shuffle_bytes > 10 * 1024 * 1024 * 1024:  # 10GB
            warnings.append("Large shuffle detected - consider broadcast joins or repartitioning")
        
        if metrics.spill_bytes > 0:
            warnings.append("Disk spill detected - consider increasing executor memory")
        
        if job.partitions < job.num_executors * job.executor_cores:
            warnings.append("Under-partitioned data - increase partitions for better parallelism")
        
        if job.partitions > job.input_rows / 1000:
            warnings.append("Over-partitioned data - consider coalescing")
        
        join_count = sum(1 for op in job.operations if op == SparkOperation.JOIN)
        if join_count > 3:
            warnings.append(f"Multiple JOINs ({join_count}) - consider restructuring query")
        
        return warnings
    
    def execute_job(self, job: SparkJob) -> SparkMetrics:
        """
        Execute a simulated Spark job.
        
        Args:
            job: The SparkJob configuration to execute.
            
        Returns:
            SparkMetrics with latency, cost, throughput, and warnings.
        """
        self._jobs_executed.append(job)
        
        # Calculate stages and tasks
        stages = self._estimate_stages(job.operations)
        tasks = stages * job.partitions
        
        # Calculate shuffle and potential spill
        shuffle_bytes = self._estimate_shuffle(job)
        
        # Estimate spill if shuffle exceeds available memory
        total_memory_bytes = job.num_executors * job.executor_memory_gb * 1024 * 1024 * 1024
        spill_bytes = max(0, shuffle_bytes - int(total_memory_bytes * 0.6))
        
        # Calculate latency
        complexity = self._calculate_complexity(job.operations)
        rows_millions = job.input_rows / 1_000_000
        
        latency_ms = (
            self.BASE_LATENCY_MS +
            (stages * self.LATENCY_PER_STAGE_MS) +
            (rows_millions * self.LATENCY_PER_MILLION_ROWS_MS * complexity)
        )
        
        # Add spill overhead
        if spill_bytes > 0:
            latency_ms *= 1.5
        
        # Calculate cost
        execution_hours = latency_ms / (1000 * 60 * 60)
        executor_cost = job.num_executors * execution_hours * self.COST_PER_EXECUTOR_HOUR
        shuffle_cost = (shuffle_bytes / (1024 * 1024 * 1024)) * self.COST_PER_SHUFFLE_GB
        cost_units = executor_cost + shuffle_cost
        
        # Calculate throughput (rows per second)
        throughput = (job.input_rows / latency_ms * 1000) if latency_ms > 0 else 0.0
        
        metrics = SparkMetrics(
            latency_ms=latency_ms,
            cost_units=cost_units,
            throughput=throughput,
            warnings=[],  # Will be filled below
            rows_processed=job.input_rows,
            partitions_used=job.partitions,
            shuffle_bytes=shuffle_bytes,
            spill_bytes=spill_bytes,
            stages_completed=stages,
            tasks_completed=tasks
        )
        
        # Generate and add warnings
        metrics.warnings = self._generate_warnings(job, metrics)
        
        return metrics
    
    def simulate_transformation(
        self,
        operation: SparkOperation,
        input_rows: int,
        partitions: int | None = None
    ) -> SparkMetrics:
        """
        Simulate a single Spark transformation.
        
        Args:
            operation: The type of operation to simulate.
            input_rows: Number of input rows.
            partitions: Number of partitions (uses default if not specified).
            
        Returns:
            SparkMetrics with operation details.
        """
        job = SparkJob(
            name=f"transform_{operation.value}",
            operations=[operation],
            input_rows=input_rows,
            partitions=partitions or self.default_parallelism
        )
        return self.execute_job(job)
    
    def simulate_etl_pipeline(
        self,
        operations: list[SparkOperation],
        input_rows: int,
        num_executors: int = 4,
        executor_memory_gb: float = 8.0
    ) -> SparkMetrics:
        """
        Simulate a complete ETL pipeline with multiple operations.
        
        Args:
            operations: List of operations in the pipeline.
            input_rows: Number of input rows.
            num_executors: Number of executors to use.
            executor_memory_gb: Memory per executor in GB.
            
        Returns:
            SparkMetrics with pipeline execution details.
        """
        job = SparkJob(
            name="etl_pipeline",
            operations=operations,
            input_rows=input_rows,
            partitions=self.default_parallelism,
            executor_memory_gb=executor_memory_gb,
            num_executors=num_executors
        )
        return self.execute_job(job)
    
    def get_job_history(self) -> list[SparkJob]:
        """Return list of all executed jobs."""
        return self._jobs_executed.copy()
    
    def clear_history(self) -> None:
        """Clear the job execution history."""
        self._jobs_executed.clear()
