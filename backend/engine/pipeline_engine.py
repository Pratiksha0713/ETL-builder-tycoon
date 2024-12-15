"""
Pipeline Engine - Core pipeline validation and graph representation.

Handles the construction, validation, and normalization of ETL pipelines
from building blocks (ingestion, storage, transform, orchestration).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class BlockType(Enum):
    """Types of building blocks in a pipeline."""
    INGESTION = "ingestion"
    STORAGE = "storage"
    TRANSFORM = "transform"
    ORCHESTRATION = "orchestration"


class ConnectionType(Enum):
    """Types of connections between blocks."""
    DATA_FLOW = "data_flow"
    CONTROL_FLOW = "control_flow"
    TRIGGER = "trigger"


@dataclass
class BuildingBlock:
    """Represents a single building block in the pipeline."""
    id: str
    block_type: BlockType
    name: str
    config: dict[str, Any] = field(default_factory=dict)
    inputs: list[str] = field(default_factory=list)  # IDs of blocks that feed into this one
    outputs: list[str] = field(default_factory=list)  # IDs of blocks this one feeds into
    
    # Block-specific properties
    latency_ms: float = 0.0
    throughput_per_sec: float = 0.0
    cost_per_operation: float = 0.0
    error_rate: float = 0.0


@dataclass
class Connection:
    """Represents a connection between two building blocks."""
    id: str
    source_id: str
    target_id: str
    connection_type: ConnectionType = ConnectionType.DATA_FLOW
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineError:
    """Represents a validation error in the pipeline."""
    code: str
    message: str
    block_id: str | None = None
    connection_id: str | None = None
    severity: str = "error"  # "error", "warning", "info"


@dataclass
class PipelineNode:
    """Normalized representation of a node in the pipeline graph."""
    id: str
    block_type: str
    name: str
    depth: int  # Distance from source nodes
    parents: list[str] = field(default_factory=list)
    children: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineGraph:
    """Normalized pipeline graph representation."""
    nodes: dict[str, PipelineNode] = field(default_factory=dict)
    edges: list[tuple[str, str]] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)  # Entry points (no inputs)
    sinks: list[str] = field(default_factory=list)  # Exit points (no outputs)
    is_valid: bool = False
    errors: list[PipelineError] = field(default_factory=list)
    
    @property
    def node_count(self) -> int:
        return len(self.nodes)
    
    @property
    def edge_count(self) -> int:
        return len(self.edges)
    
    def get_topological_order(self) -> list[str]:
        """Returns nodes in topological order (for execution scheduling)."""
        if not self.is_valid:
            return []
        
        visited: set[str] = set()
        order: list[str] = []
        
        def dfs(node_id: str) -> None:
            if node_id in visited:
                return
            visited.add(node_id)
            for child_id in self.nodes[node_id].children:
                dfs(child_id)
            order.append(node_id)
        
        for source_id in self.sources:
            dfs(source_id)
        
        return list(reversed(order))


class PipelineEngine:
    """
    Core engine for pipeline construction, validation, and graph representation.
    
    Accepts building blocks and connections, validates the pipeline structure,
    and produces a normalized graph representation for execution engines.
    """
    
    def __init__(self) -> None:
        self._blocks: dict[str, BuildingBlock] = {}
        self._connections: dict[str, Connection] = {}
        self._errors: list[PipelineError] = []
    
    def add_block(self, block: BuildingBlock) -> None:
        """Add a building block to the pipeline."""
        self._blocks[block.id] = block
    
    def add_blocks(self, blocks: list[BuildingBlock]) -> None:
        """Add multiple building blocks to the pipeline."""
        for block in blocks:
            self.add_block(block)
    
    def remove_block(self, block_id: str) -> bool:
        """Remove a building block from the pipeline."""
        if block_id in self._blocks:
            del self._blocks[block_id]
            # Remove associated connections
            self._connections = {
                conn_id: conn 
                for conn_id, conn in self._connections.items()
                if conn.source_id != block_id and conn.target_id != block_id
            }
            return True
        return False
    
    def add_connection(self, connection: Connection) -> None:
        """Add a connection between two blocks."""
        self._connections[connection.id] = connection
    
    def connect(
        self, 
        source_id: str, 
        target_id: str, 
        connection_type: ConnectionType = ConnectionType.DATA_FLOW
    ) -> Connection:
        """Create and add a connection between two blocks."""
        conn_id = f"{source_id}->{target_id}"
        connection = Connection(
            id=conn_id,
            source_id=source_id,
            target_id=target_id,
            connection_type=connection_type
        )
        self.add_connection(connection)
        return connection
    
    def remove_connection(self, connection_id: str) -> bool:
        """Remove a connection from the pipeline."""
        if connection_id in self._connections:
            del self._connections[connection_id]
            return True
        return False
    
    def validate(self) -> list[PipelineError]:
        """
        Validate the pipeline structure and connections.
        
        Returns a list of errors found during validation.
        """
        self._errors = []
        
        self._validate_block_references()
        self._validate_connection_types()
        self._validate_no_cycles()
        self._validate_no_orphans()
        self._validate_has_source_and_sink()
        
        return self._errors
    
    def _validate_block_references(self) -> None:
        """Ensure all connections reference existing blocks."""
        for conn in self._connections.values():
            if conn.source_id not in self._blocks:
                self._errors.append(PipelineError(
                    code="INVALID_SOURCE",
                    message=f"Connection references non-existent source block: {conn.source_id}",
                    connection_id=conn.id
                ))
            if conn.target_id not in self._blocks:
                self._errors.append(PipelineError(
                    code="INVALID_TARGET",
                    message=f"Connection references non-existent target block: {conn.target_id}",
                    connection_id=conn.id
                ))
    
    def _validate_connection_types(self) -> None:
        """Validate that connection types are compatible with block types."""
        valid_outputs: dict[BlockType, set[BlockType]] = {
            BlockType.INGESTION: {BlockType.TRANSFORM, BlockType.STORAGE},
            BlockType.TRANSFORM: {BlockType.TRANSFORM, BlockType.STORAGE},
            BlockType.STORAGE: {BlockType.TRANSFORM, BlockType.ORCHESTRATION},
            BlockType.ORCHESTRATION: {BlockType.INGESTION, BlockType.TRANSFORM, BlockType.STORAGE},
        }
        
        for conn in self._connections.values():
            source = self._blocks.get(conn.source_id)
            target = self._blocks.get(conn.target_id)
            
            if source and target:
                allowed_targets = valid_outputs.get(source.block_type, set())
                if target.block_type not in allowed_targets:
                    self._errors.append(PipelineError(
                        code="INVALID_CONNECTION_TYPE",
                        message=f"Cannot connect {source.block_type.value} to {target.block_type.value}",
                        connection_id=conn.id,
                        severity="warning"
                    ))
    
    def _validate_no_cycles(self) -> None:
        """Ensure the pipeline graph has no cycles."""
        adjacency = self._build_adjacency_list()
        visited: set[str] = set()
        rec_stack: set[str] = set()
        
        def has_cycle(node_id: str) -> bool:
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
        
        for block_id in self._blocks:
            if block_id not in visited:
                if has_cycle(block_id):
                    self._errors.append(PipelineError(
                        code="CYCLE_DETECTED",
                        message="Pipeline contains a cycle, which would cause infinite execution",
                        block_id=block_id
                    ))
                    break
    
    def _validate_no_orphans(self) -> None:
        """Check for blocks that aren't connected to anything."""
        connected_blocks: set[str] = set()
        
        for conn in self._connections.values():
            connected_blocks.add(conn.source_id)
            connected_blocks.add(conn.target_id)
        
        # Only flag as orphan if we have more than one block
        if len(self._blocks) > 1:
            for block_id, block in self._blocks.items():
                if block_id not in connected_blocks:
                    self._errors.append(PipelineError(
                        code="ORPHAN_BLOCK",
                        message=f"Block '{block.name}' is not connected to any other block",
                        block_id=block_id,
                        severity="warning"
                    ))
    
    def _validate_has_source_and_sink(self) -> None:
        """Ensure pipeline has at least one source and one sink."""
        if not self._blocks:
            self._errors.append(PipelineError(
                code="EMPTY_PIPELINE",
                message="Pipeline has no blocks"
            ))
            return
        
        sources, sinks = self._find_sources_and_sinks()
        
        if not sources:
            self._errors.append(PipelineError(
                code="NO_SOURCE",
                message="Pipeline has no source blocks (blocks with no inputs)"
            ))
        
        if not sinks:
            self._errors.append(PipelineError(
                code="NO_SINK",
                message="Pipeline has no sink blocks (blocks with no outputs)"
            ))
    
    def _build_adjacency_list(self) -> dict[str, list[str]]:
        """Build an adjacency list from connections."""
        adjacency: dict[str, list[str]] = {block_id: [] for block_id in self._blocks}
        for conn in self._connections.values():
            if conn.source_id in adjacency:
                adjacency[conn.source_id].append(conn.target_id)
        return adjacency
    
    def _build_reverse_adjacency(self) -> dict[str, list[str]]:
        """Build a reverse adjacency list (for finding parents)."""
        reverse: dict[str, list[str]] = {block_id: [] for block_id in self._blocks}
        for conn in self._connections.values():
            if conn.target_id in reverse:
                reverse[conn.target_id].append(conn.source_id)
        return reverse
    
    def _find_sources_and_sinks(self) -> tuple[list[str], list[str]]:
        """Find source nodes (no inputs) and sink nodes (no outputs)."""
        has_input: set[str] = set()
        has_output: set[str] = set()
        
        for conn in self._connections.values():
            has_input.add(conn.target_id)
            has_output.add(conn.source_id)
        
        sources = [bid for bid in self._blocks if bid not in has_input]
        sinks = [bid for bid in self._blocks if bid not in has_output]
        
        return sources, sinks
    
    def _compute_depths(self, sources: list[str], adjacency: dict[str, list[str]]) -> dict[str, int]:
        """Compute the depth of each node from source nodes."""
        depths: dict[str, int] = {}
        queue = [(src, 0) for src in sources]
        
        while queue:
            node_id, depth = queue.pop(0)
            if node_id not in depths or depths[node_id] < depth:
                depths[node_id] = depth
            for child in adjacency.get(node_id, []):
                queue.append((child, depth + 1))
        
        return depths
    
    def build_graph(self) -> PipelineGraph:
        """
        Build and return a normalized pipeline graph representation.
        
        The graph includes validation status and any errors found.
        """
        errors = self.validate()
        has_critical_errors = any(e.severity == "error" for e in errors)
        
        sources, sinks = self._find_sources_and_sinks()
        adjacency = self._build_adjacency_list()
        reverse_adjacency = self._build_reverse_adjacency()
        depths = self._compute_depths(sources, adjacency)
        
        # Build normalized nodes
        nodes: dict[str, PipelineNode] = {}
        for block_id, block in self._blocks.items():
            nodes[block_id] = PipelineNode(
                id=block_id,
                block_type=block.block_type.value,
                name=block.name,
                depth=depths.get(block_id, 0),
                parents=reverse_adjacency.get(block_id, []),
                children=adjacency.get(block_id, []),
                metadata={
                    "config": block.config,
                    "latency_ms": block.latency_ms,
                    "throughput_per_sec": block.throughput_per_sec,
                    "cost_per_operation": block.cost_per_operation,
                    "error_rate": block.error_rate,
                }
            )
        
        # Build edge list
        edges = [(conn.source_id, conn.target_id) for conn in self._connections.values()]
        
        return PipelineGraph(
            nodes=nodes,
            edges=edges,
            sources=sources,
            sinks=sinks,
            is_valid=not has_critical_errors,
            errors=errors
        )
    
    def get_errors(self) -> list[PipelineError]:
        """Return the list of validation errors."""
        return self._errors.copy()
    
    def clear(self) -> None:
        """Clear all blocks and connections from the engine."""
        self._blocks.clear()
        self._connections.clear()
        self._errors.clear()
    
    def to_dict(self) -> dict[str, Any]:
        """Serialize the pipeline to a dictionary."""
        return {
            "blocks": [
                {
                    "id": b.id,
                    "type": b.block_type.value,
                    "name": b.name,
                    "config": b.config,
                    "latency_ms": b.latency_ms,
                    "throughput_per_sec": b.throughput_per_sec,
                    "cost_per_operation": b.cost_per_operation,
                    "error_rate": b.error_rate,
                }
                for b in self._blocks.values()
            ],
            "connections": [
                {
                    "id": c.id,
                    "source_id": c.source_id,
                    "target_id": c.target_id,
                    "type": c.connection_type.value,
                }
                for c in self._connections.values()
            ]
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PipelineEngine:
        """Deserialize a pipeline from a dictionary."""
        engine = cls()
        
        for block_data in data.get("blocks", []):
            block = BuildingBlock(
                id=block_data["id"],
                block_type=BlockType(block_data["type"]),
                name=block_data["name"],
                config=block_data.get("config", {}),
                latency_ms=block_data.get("latency_ms", 0.0),
                throughput_per_sec=block_data.get("throughput_per_sec", 0.0),
                cost_per_operation=block_data.get("cost_per_operation", 0.0),
                error_rate=block_data.get("error_rate", 0.0),
            )
            engine.add_block(block)
        
        for conn_data in data.get("connections", []):
            connection = Connection(
                id=conn_data["id"],
                source_id=conn_data["source_id"],
                target_id=conn_data["target_id"],
                connection_type=ConnectionType(conn_data.get("type", "data_flow")),
            )
            engine.add_connection(connection)
        
        return engine


def validate(graph: dict) -> list[dict]:
    """
    Validate a pipeline graph from the canvas.
    
    Args:
        graph: Dictionary containing:
            - blocks: dict[str, dict] - block_id -> block data
            - connections: dict[str, list[str]] - adjacency list (source_id -> [target_ids])
    
    Returns:
        List of error/warning dictionaries with keys: type, message, block_id (optional)
    """
    errors: list[dict] = []
    
    blocks = graph.get('blocks', {})
    connections = graph.get('connections', {})
    
    # Check 1: Empty pipeline
    if not blocks:
        errors.append({
            'type': 'error',
            'message': 'Pipeline is empty - add at least one block'
        })
        return errors
    
    # Check 2: Start block exists (blocks with no incoming connections)
    has_incoming: set[str] = set()
    for source_id, targets in connections.items():
        for target_id in targets:
            has_incoming.add(target_id)
    
    start_blocks = [bid for bid in blocks if bid not in has_incoming]
    
    if not start_blocks:
        errors.append({
            'type': 'error',
            'message': 'No start block found - pipeline needs at least one block with no incoming connections'
        })
    
    # Check 3: Invalid connections (reference non-existent blocks)
    for source_id, targets in connections.items():
        if source_id not in blocks:
            errors.append({
                'type': 'error',
                'message': f'Connection from non-existent block: {source_id[:8]}...',
                'block_id': source_id
            })
        for target_id in targets:
            if target_id not in blocks:
                errors.append({
                    'type': 'error',
                    'message': f'Connection to non-existent block: {target_id[:8]}...',
                    'block_id': target_id
                })
    
    # Check 4: Self-connections
    for source_id, targets in connections.items():
        if source_id in targets:
            block_name = blocks.get(source_id, {}).get('type', 'Unknown')
            errors.append({
                'type': 'error',
                'message': f'Block "{block_name}" cannot connect to itself',
                'block_id': source_id
            })
    
    # Check 5: Cycles detection using DFS
    cycle_errors = _detect_cycles(blocks, connections)
    errors.extend(cycle_errors)
    
    # Check 6: Orphan blocks (blocks not connected to anything)
    if len(blocks) > 1:
        connected_blocks: set[str] = set()
        for source_id, targets in connections.items():
            if targets:  # Only count if there are actual connections
                connected_blocks.add(source_id)
                connected_blocks.update(targets)
        
        for block_id, block in blocks.items():
            if block_id not in connected_blocks:
                errors.append({
                    'type': 'warning',
                    'message': f'Block "{block.get("type", "Unknown")}" is not connected to any other block',
                    'block_id': block_id
                })
    
    # Check 7: End block exists (blocks with no outgoing connections)
    has_outgoing: set[str] = set()
    for source_id, targets in connections.items():
        if targets:
            has_outgoing.add(source_id)
    
    end_blocks = [bid for bid in blocks if bid not in has_outgoing]
    
    if not end_blocks and len(blocks) > 1:
        errors.append({
            'type': 'warning',
            'message': 'No end block found - pipeline should have at least one block with no outgoing connections'
        })
    
    return errors


def _detect_cycles(blocks: dict, connections: dict) -> list[dict]:
    """
    Detect cycles in the graph using DFS.
    
    Args:
        blocks: dict of block_id -> block data
        connections: adjacency list (source_id -> [target_ids])
    
    Returns:
        List of cycle error dictionaries
    """
    errors: list[dict] = []
    visited: set[str] = set()
    rec_stack: set[str] = set()
    cycle_path: list[str] = []
    
    def dfs(node_id: str) -> bool:
        """Returns True if a cycle is detected."""
        visited.add(node_id)
        rec_stack.add(node_id)
        cycle_path.append(node_id)
        
        for neighbor in connections.get(node_id, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                # Found a cycle - build the cycle description
                cycle_start_idx = cycle_path.index(neighbor)
                cycle_nodes = cycle_path[cycle_start_idx:] + [neighbor]
                cycle_names = [
                    blocks.get(nid, {}).get('type', nid[:8]) 
                    for nid in cycle_nodes
                ]
                errors.append({
                    'type': 'error',
                    'message': f'Cycle detected: {" → ".join(cycle_names)}',
                    'block_id': neighbor
                })
                return True
        
        cycle_path.pop()
        rec_stack.remove(node_id)
        return False
    
    for block_id in blocks:
        if block_id not in visited:
            if dfs(block_id):
                break  # Stop after finding first cycle
    
    return errors


@dataclass
class SimulationResult:
    """Result of a pipeline simulation."""
    total_latency_ms: float = 0.0
    total_cost: float = 0.0
    throughput: float = 0.0
    block_metrics: dict[str, dict] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    success: bool = True


def simulate(graph: dict) -> SimulationResult:
    """
    Simulate a pipeline execution using fake services.
    
    Calls FakeKafka, FakeS3, FakeSparkJob, FakeSQL based on block types
    and aggregates metrics.
    
    Args:
        graph: Dictionary containing:
            - blocks: dict[str, dict] - block_id -> block data with 'type' key
            - connections: dict[str, list[str]] - adjacency list
    
    Returns:
        SimulationResult with latency, cost, throughput, and per-block metrics
    """
    from backend.simulation.mock_kafka import FakeKafka
    from backend.simulation.mock_s3 import FakeS3
    from backend.simulation.mock_spark import FakeSpark, SparkOperation
    from backend.simulation.mock_sql import FakeSQL
    
    blocks = graph.get('blocks', {})
    connections = graph.get('connections', {})
    
    if not blocks:
        return SimulationResult(
            success=False,
            warnings=['No blocks to simulate']
        )
    
    # Initialize fake services
    kafka = FakeKafka(topic="etl-pipeline", partitions=4, records_per_second=10000)
    s3 = FakeS3(bucket="etl-data-bucket")
    spark = FakeSpark(app_name="ETLSimulation", default_parallelism=200)
    sql = FakeSQL()
    sql.connect()
    
    # Map block types to simulation functions
    block_type_to_service = {
        # Ingestion blocks
        'Database Reader': 'sql',
        'CSV Reader': 's3',
        'API Reader': 's3',
        'Streaming Reader': 'kafka',
        'Excel Reader': 's3',
        'File System Reader': 's3',
        # Storage blocks
        'Database Writer': 'sql',
        'CSV Writer': 's3',
        'Data Lake Writer': 's3',
        'Cache Writer': 'kafka',
        'Excel Writer': 's3',
        'File System Writer': 's3',
        # Transform blocks
        'Filter': 'spark',
        'Join': 'spark',
        'Aggregate': 'spark',
        'Union': 'spark',
        'Rename Columns': 'spark',
        'Split': 'spark',
        'Type Converter': 'spark',
        'Data Cleaner': 'spark',
        # Orchestration blocks
        'Scheduler': 'orchestration',
        'Loop': 'orchestration',
        'Conditional': 'orchestration',
        'Branch': 'orchestration',
        'Trigger': 'orchestration',
        'Parallel': 'orchestration',
    }
    
    # Spark operation mapping
    spark_op_map = {
        'Filter': SparkOperation.FILTER,
        'Join': SparkOperation.JOIN,
        'Aggregate': SparkOperation.AGGREGATE,
        'Union': SparkOperation.REDUCE,
        'Rename Columns': SparkOperation.MAP,
        'Split': SparkOperation.MAP,
        'Type Converter': SparkOperation.MAP,
        'Data Cleaner': SparkOperation.FILTER,
    }
    
    # Simulate each block
    total_latency_ms = 0.0
    total_cost = 0.0
    all_warnings: list[str] = []
    block_metrics: dict[str, dict] = {}
    
    # Default simulation parameters
    default_rows = 100000
    default_data_size = 1024 * 1024  # 1MB
    
    # Get topological order for simulation (sources first)
    execution_order = _get_execution_order(blocks, connections)
    
    for block_id in execution_order:
        block = blocks[block_id]
        block_type = block.get('type', 'Unknown')
        service = block_type_to_service.get(block_type, 'orchestration')
        
        latency = 0.0
        cost = 0.0
        throughput = 0.0
        warnings: list[str] = []
        
        if service == 'kafka':
            # Simulate Kafka streaming
            metrics = kafka.simulate_ingestion(n_seconds=1.0)
            latency = metrics.latency_ms
            cost = metrics.cost_units
            throughput = metrics.throughput
            warnings = metrics.warnings
            
        elif service == 's3':
            # Simulate S3 read/write
            if 'Reader' in block_type:
                _, metrics = s3.get_object(f"data/{block_type.lower().replace(' ', '_')}.data")
                # Simulate putting some data first for get to work
                s3.put_object(f"data/{block_type.lower().replace(' ', '_')}.data", b"x" * default_data_size)
                _, metrics = s3.get_object(f"data/{block_type.lower().replace(' ', '_')}.data")
            else:
                metrics = s3.put_object(
                    f"output/{block_type.lower().replace(' ', '_')}.data",
                    b"x" * default_data_size
                )
            latency = metrics.latency_ms
            cost = metrics.cost_units
            throughput = metrics.throughput
            warnings = metrics.warnings
            
        elif service == 'spark':
            # Simulate Spark transformation
            operation = spark_op_map.get(block_type, SparkOperation.MAP)
            metrics = spark.simulate_transformation(
                operation=operation,
                input_rows=default_rows
            )
            latency = metrics.latency_ms
            cost = metrics.cost_units
            throughput = metrics.throughput
            warnings = metrics.warnings
            
        elif service == 'sql':
            # Simulate SQL query
            if 'Reader' in block_type:
                # Create a test table and simulate read
                sql.create_table("test_data", {"id": "INTEGER", "value": "TEXT"})
                result = sql.execute("SELECT * FROM test_data LIMIT 1000")
            else:
                result = sql.execute("INSERT INTO test_data (id, value) VALUES (?, ?)", (1, "test"))
            latency = result.metrics.latency_ms
            cost = result.metrics.cost_units
            throughput = result.metrics.throughput
            warnings = result.metrics.warnings
            
        else:  # orchestration
            # Minimal overhead for orchestration blocks
            latency = 5.0  # 5ms overhead
            cost = 0.001
            throughput = 0.0
            warnings = []
        
        # Store block metrics
        block_metrics[block_id] = {
            'type': block_type,
            'latency_ms': latency,
            'cost': cost,
            'throughput': throughput,
            'warnings': warnings
        }
        
        # Aggregate totals
        total_latency_ms += latency
        total_cost += cost
        all_warnings.extend([f"[{block_type}] {w}" for w in warnings])
    
    # Cleanup
    sql.disconnect()
    
    # Calculate overall throughput (bottleneck is the slowest block)
    if block_metrics:
        min_throughput = min(
            (m['throughput'] for m in block_metrics.values() if m['throughput'] > 0),
            default=0.0
        )
    else:
        min_throughput = 0.0
    
    return SimulationResult(
        total_latency_ms=total_latency_ms,
        total_cost=total_cost,
        throughput=min_throughput,
        block_metrics=block_metrics,
        warnings=all_warnings,
        success=True
    )


def _get_execution_order(blocks: dict, connections: dict) -> list[str]:
    """
    Get blocks in topological order for simulation.
    
    Args:
        blocks: dict of block_id -> block data
        connections: adjacency list
    
    Returns:
        List of block IDs in execution order
    """
    # Find blocks with no incoming connections (sources)
    has_incoming: set[str] = set()
    for targets in connections.values():
        has_incoming.update(targets)
    
    sources = [bid for bid in blocks if bid not in has_incoming]
    
    # BFS from sources
    visited: set[str] = set()
    order: list[str] = []
    queue = sources.copy()
    
    while queue:
        node_id = queue.pop(0)
        if node_id in visited:
            continue
        visited.add(node_id)
        order.append(node_id)
        
        # Add children to queue
        for target in connections.get(node_id, []):
            if target not in visited:
                queue.append(target)
    
    # Add any remaining disconnected blocks
    for block_id in blocks:
        if block_id not in visited:
            order.append(block_id)
    
    return order









