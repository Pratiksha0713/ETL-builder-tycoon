"""
Latency Engine - Pipeline latency calculation and critical path analysis.

Handles the computation of end-to-end latency, per-node latency, and
critical path identification for pipelines.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.engine.pipeline_engine import PipelineGraph


@dataclass
class LatencyResult:
    """Result of latency calculation for a pipeline."""
    total_latency_ms: float = 0.0
    node_latencies: dict[str, float] = field(default_factory=dict)
    critical_path: list[str] = field(default_factory=list)
    parallelization_opportunities: list[str] = field(default_factory=list)


class LatencyEngine:
    """
    Engine for calculating and analyzing pipeline latency.

    Computes latency metrics including:
    - End-to-end pipeline latency
    - Per-node latency breakdown
    - Critical path identification
    - Parallelization opportunities
    """

    def __init__(self) -> None:
        self._base_latencies = {
            "INGESTION": 50.0,      # Kafka ingestion latency
            "STORAGE": 100.0,       # S3 storage latency
            "TRANSFORM": 200.0,     # Spark transform latency
            "ORCHESTRATION": 10.0,  # Airflow orchestration latency
        }

    def calculate(self, graph: PipelineGraph) -> LatencyResult:
        """
        Calculate latency metrics for the given pipeline graph.

        Args:
            graph: The normalized pipeline graph to analyze.

        Returns:
            LatencyResult with computed latency metrics.
        """
        node_latencies = {}

        # Calculate latency for each node
        for node_id, node in graph.nodes.items():
            latency = self._calculate_node_latency(node)
            node_latencies[node_id] = latency

        # Find critical path using topological analysis
        critical_path = self.find_critical_path(graph)

        # Calculate total latency (critical path sum)
        total_latency = sum(node_latencies.get(node_id, 0.0) for node_id in critical_path)

        # Identify parallelization opportunities
        parallelization_opportunities = self._find_parallelization_opportunities(graph)

        return LatencyResult(
            total_latency_ms=total_latency,
            node_latencies=node_latencies,
            critical_path=critical_path,
            parallelization_opportunities=parallelization_opportunities
        )

    def find_critical_path(self, graph: PipelineGraph) -> list[str]:
        """
        Find the critical path (longest path) in the pipeline graph.

        Args:
            graph: The pipeline graph.

        Returns:
            List of node IDs representing the critical path.
        """
        if not graph.nodes:
            return []

        # Simple topological sort for critical path approximation
        # In a real implementation, this would use proper critical path algorithm
        sorted_nodes = []
        visited = set()
        temp_visited = set()

        def topological_sort(node_id: str):
            if node_id in temp_visited:
                return  # Cycle detected, skip
            if node_id in visited:
                return

            temp_visited.add(node_id)

            # Visit all successors
            for edge in graph.edges:
                if edge.source_id == node_id:
                    topological_sort(edge.target_id)

            temp_visited.remove(node_id)
            visited.add(node_id)
            sorted_nodes.append(node_id)

        # Start from nodes with no incoming edges (sources)
        incoming_count = {node_id: 0 for node_id in graph.nodes.keys()}
        for edge in graph.edges:
            incoming_count[edge.target_id] += 1

        sources = [node_id for node_id, count in incoming_count.items() if count == 0]

        for source in sources:
            topological_sort(source)

        # Reverse to get topological order
        sorted_nodes.reverse()

        # For simplicity, return all nodes as critical path
        # Real implementation would calculate actual longest path
        return sorted_nodes

    def estimate_scaling_impact(
        self,
        graph: PipelineGraph,
        node_id: str,
        scale_factor: float
    ) -> LatencyResult:
        """
        Estimate latency impact of scaling a specific node.

        Args:
            graph: The pipeline graph.
            node_id: The node to scale.
            scale_factor: Scaling factor for the node's performance.

        Returns:
            LatencyResult with estimated metrics after scaling.
        """
        # Create a modified graph for estimation
        modified_latencies = {}

        for nid, node in graph.nodes.items():
            if nid == node_id:
                # Scale down latency for the target node
                base_latency = self._calculate_node_latency(node)
                modified_latencies[nid] = base_latency / scale_factor
            else:
                modified_latencies[nid] = self._calculate_node_latency(node)

        # Recalculate critical path and total latency
        critical_path = self.find_critical_path(graph)
        total_latency = sum(modified_latencies.get(nid, 0.0) for nid in critical_path)

        return LatencyResult(
            total_latency_ms=total_latency,
            node_latencies=modified_latencies,
            critical_path=critical_path,
            parallelization_opportunities=[]
        )

    def _calculate_node_latency(self, node) -> float:
        """Calculate latency for a single node."""
        base_latency = self._base_latencies.get(node.block_type.name, 50.0)

        # Adjust based on node configuration
        parallelism = node.configuration.get("parallelism", 1.0)
        data_volume = node.configuration.get("data_volume_gb", 1.0)

        # Parallelism reduces latency, data volume increases it
        latency = base_latency * (data_volume / parallelism)

        # Add some randomness/variation (±20%)
        import random
        variation = random.uniform(0.8, 1.2)
        return latency * variation

    def _find_parallelization_opportunities(self, graph) -> list[str]:
        """Find nodes that could benefit from parallelization."""
        opportunities = []

        for node_id, node in graph.nodes.items():
            # Check if node has high latency and could be parallelized
            base_latency = self._base_latencies.get(node.block_type.name, 50.0)
            if base_latency > 100.0:  # High latency operations
                opportunities.append(f"Consider parallelizing {node.block.name} operations")

        return opportunities[:3]  # Limit suggestions
