"""
Pipeline Engine - Core pipeline graph representation and validation.

Handles pipeline construction, validation, and graph operations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


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
        
        Returns:
            List of validation errors (empty if valid).
        """
        errors: list[str] = []
        
        # Check for at least one source and one destination
        has_source = any(
            node.block_type == BlockType.INGESTION 
            for node in graph.nodes.values()
        )
        has_destination = any(
            node.block_type == BlockType.STORAGE 
            for node in graph.nodes.values()
        )
        
        if not has_source:
            errors.append("Pipeline must have at least one ingestion block")
        if not has_destination:
            errors.append("Pipeline must have at least one storage block")
        
        # Check for valid connections
        for connection in graph.edges:
            if connection.source_id not in graph.nodes:
                errors.append(f"Connection source '{connection.source_id}' not found")
            if connection.target_id not in graph.nodes:
                errors.append(f"Connection target '{connection.target_id}' not found")
        
        return errors
    
    def normalize(self, graph: PipelineGraph) -> PipelineGraph:
        """
        Normalize the pipeline graph for analysis.
        
        Returns:
            Normalized copy of the graph.
        """
        # TODO: Implement graph normalization
        return graph
