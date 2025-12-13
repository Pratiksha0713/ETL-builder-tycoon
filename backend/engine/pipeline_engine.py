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






