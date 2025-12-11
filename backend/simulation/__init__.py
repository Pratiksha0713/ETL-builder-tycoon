"""
Simulation module - Mock services for ETL Builder Tycoon.

Contains simulated versions of:
- Kafka (streaming)
- S3 (object storage)
- Spark (distributed processing)
- SQL (relational databases)

All simulation classes return metrics with standard keys:
- latency_ms: Operation latency in milliseconds
- cost_units: Simulated cost units for the operation
- throughput: Operations/rows/bytes per second
- warnings: List of warning messages
"""

from backend.simulation.mock_kafka import (
    FakeKafka,
    IngestionMetrics,
    LagMetrics,
    SimulationMetrics,
)
from backend.simulation.mock_s3 import (
    FakeS3,
    S3Metrics,
    S3Object,
)
from backend.simulation.mock_spark import (
    FakeSpark,
    SparkJob,
    SparkMetrics,
    SparkOperation,
)
from backend.simulation.mock_sql import (
    FakeSQL,
    QueryMetrics,
    QueryResult,
)

__all__ = [
    # Common
    "SimulationMetrics",
    # Kafka
    "FakeKafka",
    "IngestionMetrics",
    "LagMetrics",
    # S3
    "FakeS3",
    "S3Metrics",
    "S3Object",
    # Spark
    "FakeSpark",
    "SparkJob",
    "SparkMetrics",
    "SparkOperation",
    # SQL
    "FakeSQL",
    "QueryMetrics",
    "QueryResult",
]
