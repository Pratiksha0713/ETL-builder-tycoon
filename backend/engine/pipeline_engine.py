"""
Pipeline Engine - Core pipeline graph representation and validation.

Handles pipeline construction, validation, and graph operations.
"""

from __future__ import annotations

from collections import deque, defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.engine.cost_engine import CostResult
    from backend.engine.quality_engine import QualityResult
    from backend.engine.throughput_engine import ThroughputResult


class BlockType(Enum):
    """Types of pipeline blocks."""
    INGESTION = "ingestion"
    STORAGE = "storage"
    TRANSFORM = "transform"
    ORCHESTRATION = "orchestration"


class ConnectionType(Enum):
    """Types of connections between blocks."""
    DATA_FLOW = "data_flow"
    CONTROL_FLOW = "control_flow"
    CONDITIONAL = "conditional"


@dataclass
class BuildingBlock:
    """Represents a building block in the pipeline."""
    name: str
    block_type: BlockType
    capabilities: list[str] = field(default_factory=list)
    cost_profile: dict[str, Any] = field(default_factory=dict)


@dataclass
class Connection:
    """Represents a connection between pipeline nodes."""
    source_id: str
    target_id: str
    connection_type: ConnectionType = ConnectionType.DATA_FLOW
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineNode:
    """Represents a node in the pipeline graph."""
    node_id: str
    block_type: BlockType
    block: BuildingBlock
    position: tuple[float, float] = (0.0, 0.0)
    configuration: dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineGraph:
    """Represents the complete pipeline graph."""
    nodes: dict[str, PipelineNode] = field(default_factory=dict)
    edges: list[Connection] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class PipelineError(Exception):
    """Exception raised for pipeline-related errors."""
    pass


class PipelineEngine:
    """
    Engine for pipeline construction and validation.
    
    Handles:
    - Graph construction from blocks
    - Structural validation
    - Schema validation
    - Graph normalization
    """
    
    def __init__(self) -> None:
        self._graphs: dict[str, PipelineGraph] = {}
    
    def create_graph(self, graph_id: str) -> PipelineGraph:
        """Create a new pipeline graph."""
        graph = PipelineGraph()
        self._graphs[graph_id] = graph
        return graph
    
    def add_node(self, graph: PipelineGraph, node: PipelineNode) -> None:
        """Add a node to the pipeline graph."""
        graph.nodes[node.node_id] = node
    
    def add_connection(self, graph: PipelineGraph, connection: Connection) -> None:
        """Add a connection to the pipeline graph."""
        graph.edges.append(connection)
    
    def validate(self, graph: PipelineGraph) -> list[str]:
        """
        Validate the pipeline graph structure.
        
        Validates:
        - Pipeline starts with INGESTION node(s)
        - No cycles in the graph
        - No orphan nodes (all nodes connected)
        - Data flows follow: ingestion → storage → transform → orchestration → output
        
        Returns:
            List of validation errors (empty if valid).
        """
        errors: list[str] = []
        
        if not graph.nodes:
            errors.append("Pipeline must have at least one node")
            return errors
        
        # Check for valid connections
        for connection in graph.edges:
            if connection.source_id not in graph.nodes:
                errors.append(f"Connection source '{connection.source_id}' not found")
            if connection.target_id not in graph.nodes:
                errors.append(f"Connection target '{connection.target_id}' not found")
        
        if errors:
            return errors  # Can't continue validation with invalid connections
        
        # Build adjacency list
        adjacency: dict[str, list[str]] = defaultdict(list)
        in_degree: dict[str, int] = {node_id: 0 for node_id in graph.nodes.keys()}
        
        for connection in graph.edges:
            if connection.connection_type == ConnectionType.DATA_FLOW:
                adjacency[connection.source_id].append(connection.target_id)
                in_degree[connection.target_id] += 1
        
        # 1. Ensure pipeline starts with INGESTION node(s)
        ingestion_nodes = [
            node_id for node_id, node in graph.nodes.items()
            if node.block_type == BlockType.INGESTION
        ]
        
        if not ingestion_nodes:
            errors.append("Pipeline must have at least one INGESTION node")
        else:
            # Check that ingestion nodes have no incoming edges
            for node_id in ingestion_nodes:
                if in_degree[node_id] > 0:
                    errors.append(
                        f"Ingestion node '{node_id}' ({graph.nodes[node_id].block.name}) "
                        f"has incoming connections - ingestion nodes should be sources"
                    )
        
        # 2. Check for cycles using DFS
        visited: set[str] = set()
        rec_stack: set[str] = set()
        
        def has_cycle(node_id: str) -> bool:
            """Check for cycles starting from this node."""
            visited.add(node_id)
            rec_stack.add(node_id)
            
            for neighbor in adjacency.get(node_id, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node_id)
            return False
        
        for node_id in graph.nodes.keys():
            if node_id not in visited:
                if has_cycle(node_id):
                    errors.append("Pipeline contains cycles - data flow must be acyclic")
                    break
        
        # 3. Check for orphan nodes (nodes with no connections)
        connected_nodes: set[str] = set()
        for connection in graph.edges:
            connected_nodes.add(connection.source_id)
            connected_nodes.add(connection.target_id)
        
        orphan_nodes = [
            node_id for node_id in graph.nodes.keys()
            if node_id not in connected_nodes
        ]
        
        if orphan_nodes:
            for node_id in orphan_nodes:
                node = graph.nodes[node_id]
                errors.append(
                    f"Orphan node '{node_id}' ({node.block.name}) has no connections"
                )
        
        # 4. Validate data flow order: ingestion → storage → transform → orchestration → output
        # Define valid transitions
        valid_transitions: dict[BlockType, set[BlockType]] = {
            BlockType.INGESTION: {BlockType.STORAGE, BlockType.TRANSFORM},
            BlockType.STORAGE: {BlockType.STORAGE, BlockType.TRANSFORM, BlockType.ORCHESTRATION},
            BlockType.TRANSFORM: {BlockType.STORAGE, BlockType.TRANSFORM, BlockType.ORCHESTRATION},
            BlockType.ORCHESTRATION: {BlockType.STORAGE, BlockType.TRANSFORM},
        }
        
        for connection in graph.edges:
            if connection.connection_type == ConnectionType.DATA_FLOW:
                source_node = graph.nodes.get(connection.source_id)
                target_node = graph.nodes.get(connection.target_id)
                
                if source_node and target_node:
                    source_type = source_node.block_type
                    target_type = target_node.block_type
                    
                    # Storage can be both input and output (data lake pattern)
                    if target_type == BlockType.STORAGE:
                        continue  # Storage can receive from any type
                    
                    if source_type not in valid_transitions:
                        errors.append(
                            f"Invalid source type '{source_type.value}' for connection "
                            f"{connection.source_id} → {connection.target_id}"
                        )
                    elif target_type not in valid_transitions.get(source_type, set()):
                        errors.append(
                            f"Invalid data flow: {source_type.value} → {target_type.value} "
                            f"({connection.source_id} → {connection.target_id}). "
                            f"Valid flows: ingestion → storage/transform, "
                            f"storage → storage/transform/orchestration, "
                            f"transform → storage/transform/orchestration, "
                            f"orchestration → storage/transform"
                        )
        
        return errors
    
    def normalize(self, graph: PipelineGraph) -> PipelineGraph:
        """
        Normalize the pipeline graph for analysis.
        
        Returns:
            Normalized copy of the graph.
        """
        # TODO: Implement graph normalization
        return graph
    
    def simulate(self, graph: PipelineGraph) -> dict[str, Any]:
        """
        Simulate the pipeline by executing mock services for each node type.
        
        For each node type:
        - Kafka → FakeKafka.simulate_ingestion()
        - S3 → FakeS3.put/get
        - Spark → FakeSparkJob.run()
        - SQL/dbt → FakeSQL.execute()
        
        Aggregates results:
        - latency_total: Sum of all latencies
        - cost_total: Sum of all costs
        - throughput_min: Minimum throughput (bottleneck)
        - quality_score: Average quality score
        
        Args:
            graph: The pipeline graph to simulate
            
        Returns:
            Dictionary containing aggregated simulation results:
            {
                "latency_total": float,
                "cost_total": float,
                "throughput_min": float,
                "quality_score": float,
                "node_results": dict[str, dict],
                "cost": CostResult or None,
                "quality": QualityResult or None,
                "throughput": ThroughputResult or None,
            }
        """
        # Normalize graph first to get topological order
        normalized_graph = self.normalize(graph)
        
        # Initialize aggregated metrics
        latency_total = 0.0
        cost_total = 0.0
        throughput_values: list[float] = []
        quality_scores: list[float] = []
        node_results: dict[str, dict[str, Any]] = {}
        
        # Map node names to simulation functions
        # Process nodes in topological order
        topological_order = normalized_graph.metadata.get("topological_order", list(normalized_graph.nodes.keys()))
        
        for node_id in topological_order:
            node = normalized_graph.nodes.get(node_id)
            if not node:
                continue
            
            node_name = node.block.name.lower()
            node_type = node.block_type
            metrics: dict[str, Any] = {}
            
            try:
                # Kafka Source → simulate ingestion
                if "kafka" in node_name or node_type == BlockType.INGESTION:
                    from backend.simulation.mock_kafka import FakeKafka
                    kafka = FakeKafka(topic=f"topic_{node_id}", partitions=3, records_per_second=1000.0)
                    kafka_metrics = kafka.simulate_ingestion(n_seconds=1.0)
                    metrics = {
                        "latency_ms": kafka_metrics.latency_ms,
                        "cost_units": kafka_metrics.cost_units,
                        "throughput": kafka_metrics.throughput,
                        "warnings": kafka_metrics.warnings,
                    }
                    latency_total += kafka_metrics.latency_ms
                    cost_total += kafka_metrics.cost_units
                    if kafka_metrics.throughput > 0:
                        throughput_values.append(kafka_metrics.throughput)
                    quality_scores.append(0.95)  # High quality for ingestion
                
                # S3 Storage → simulate put/get operations
                elif "s3" in node_name or "delta" in node_name or node_type == BlockType.STORAGE:
                    from backend.simulation.mock_s3 import FakeS3
                    s3 = FakeS3(bucket=f"bucket_{node_id}")
                    # Simulate PUT operation
                    test_data = b"test data" * 1000  # 9KB test data
                    s3_metrics = s3.put_object(key=f"data_{node_id}.json", data=test_data)
                    metrics = {
                        "latency_ms": s3_metrics.latency_ms,
                        "cost_units": s3_metrics.cost_units,
                        "throughput": s3_metrics.throughput,
                        "warnings": s3_metrics.warnings,
                        "bytes_transferred": s3_metrics.bytes_transferred,
                    }
                    latency_total += s3_metrics.latency_ms
                    cost_total += s3_metrics.cost_units
                    if s3_metrics.throughput > 0:
                        throughput_values.append(s3_metrics.throughput)
                    quality_scores.append(0.90)  # Good quality for storage
                
                # Spark Transform → simulate job execution
                elif "spark" in node_name or node_type == BlockType.TRANSFORM:
                    from backend.simulation.mock_spark import FakeSpark, SparkJob, SparkOperation
                    spark = FakeSpark(app_name=f"app_{node_id}")
                    spark_job = SparkJob(
                        name=f"job_{node_id}",
                        operations=[SparkOperation.MAP, SparkOperation.FILTER],
                        input_rows=100000,
                        partitions=200,
                    )
                    spark_metrics = spark.execute_job(spark_job)
                    metrics = {
                        "latency_ms": spark_metrics.latency_ms,
                        "cost_units": spark_metrics.cost_units,
                        "throughput": spark_metrics.throughput,
                        "warnings": spark_metrics.warnings,
                        "rows_processed": spark_metrics.rows_processed,
                    }
                    latency_total += spark_metrics.latency_ms
                    cost_total += spark_metrics.cost_units
                    if spark_metrics.throughput > 0:
                        throughput_values.append(spark_metrics.throughput)
                    quality_scores.append(0.85)  # Good quality for transforms
                
                # SQL/dbt → simulate query execution
                elif "dbt" in node_name or "sql" in node_name or "database" in node_name:
                    from backend.simulation.mock_sql import FakeSQL
                    sql_db = FakeSQL(database=":memory:")
                    sql_db.connect()
                    # Simulate a SELECT query
                    query_result = sql_db.execute("SELECT 1 as test")
                    sql_metrics = query_result.metrics
                    metrics = {
                        "latency_ms": sql_metrics.latency_ms,
                        "cost_units": sql_metrics.cost_units,
                        "throughput": sql_metrics.throughput,
                        "warnings": sql_metrics.warnings,
                        "rows_returned": sql_metrics.rows_returned,
                    }
                    latency_total += sql_metrics.latency_ms
                    cost_total += sql_metrics.cost_units
                    if sql_metrics.throughput > 0:
                        throughput_values.append(sql_metrics.throughput)
                    quality_scores.append(0.88)  # Good quality for SQL
                    sql_db.disconnect()
                
                # Orchestration (Airflow) → simulate workflow
                elif "airflow" in node_name or node_type == BlockType.ORCHESTRATION:
                    # Orchestration adds overhead but no direct data processing
                    metrics = {
                        "latency_ms": 50.0,  # Overhead latency
                        "cost_units": 0.01,  # Minimal cost
                        "throughput": float('inf'),  # No bottleneck
                        "warnings": [],
                    }
                    latency_total += 50.0
                    cost_total += 0.01
                    quality_scores.append(0.92)  # High quality for orchestration
                
                # Default: minimal simulation
                else:
                    metrics = {
                        "latency_ms": 10.0,
                        "cost_units": 0.001,
                        "throughput": 1000.0,
                        "warnings": [],
                    }
                    latency_total += 10.0
                    cost_total += 0.001
                    throughput_values.append(1000.0)
                    quality_scores.append(0.80)
                
            except Exception as e:
                metrics = {
                    "latency_ms": 0.0,
                    "cost_units": 0.0,
                    "throughput": 0.0,
                    "warnings": [f"Simulation error: {str(e)}"],
                    "error": str(e),
                }
            
            node_results[node_id] = metrics
        
        # Calculate aggregated metrics
        throughput_min = min(throughput_values) if throughput_values else 0.0
        quality_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
        
        # Also try to get results from dedicated engines (if implemented)
        results: dict[str, Any] = {
            "latency_total": latency_total,
            "cost_total": cost_total,
            "throughput_min": throughput_min,
            "quality_score": quality_score,
            "node_results": node_results,
            "cost": None,
            "quality": None,
            "throughput": None,
        }
        
        # Import engines here to avoid circular imports
        try:
            from backend.engine.cost_engine import CostEngine
            cost_engine = CostEngine()
            results["cost"] = cost_engine.calculate(normalized_graph)
        except (NotImplementedError, Exception):
            pass
        
        try:
            from backend.engine.quality_engine import QualityEngine
            quality_engine = QualityEngine()
            results["quality"] = quality_engine.calculate(normalized_graph)
        except (NotImplementedError, Exception):
            pass
        
        try:
            from backend.engine.throughput_engine import ThroughputEngine
            throughput_engine = ThroughputEngine()
            results["throughput"] = throughput_engine.calculate(normalized_graph)
        except (NotImplementedError, Exception):
            pass
        
        return results
