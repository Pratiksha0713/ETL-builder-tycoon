"""
Engine module - Core simulation engines for ETL Builder Tycoon.

Contains engines for:
- Pipeline construction and validation
- Latency calculation and simulation
- Data quality metrics
- Cost calculation and optimization
- Throughput analysis
"""

from backend.engine.pipeline_engine import (
    BlockType,
    BuildingBlock,
    Connection,
    ConnectionType,
    PipelineEngine,
    PipelineError,
    PipelineGraph,
    PipelineNode,
)
from backend.engine.latency_engine import LatencyEngine, LatencyResult
from backend.engine.quality_engine import (
    QualityEngine,
    QualityMetricType,
    QualityResult,
    QualityScore,
)
from backend.engine.cost_engine import (
    CostBreakdown,
    CostCategory,
    CostEngine,
    CostResult,
)
from backend.engine.throughput_engine import (
    ThroughputEngine,
    ThroughputMetrics,
    ThroughputResult,
)

__all__ = [
    # Pipeline Engine
    "BlockType",
    "BuildingBlock",
    "Connection",
    "ConnectionType",
    "PipelineEngine",
    "PipelineError",
    "PipelineGraph",
    "PipelineNode",
    # Latency Engine
    "LatencyEngine",
    "LatencyResult",
    # Quality Engine
    "QualityEngine",
    "QualityMetricType",
    "QualityResult",
    "QualityScore",
    # Cost Engine
    "CostBreakdown",
    "CostCategory",
    "CostEngine",
    "CostResult",
    # Throughput Engine
    "ThroughputEngine",
    "ThroughputMetrics",
    "ThroughputResult",
]





