"""
Cost Engine - Pipeline cost calculation and optimization.

Handles the computation of operational costs for pipelines,
including compute costs, storage costs, and data transfer costs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.engine.pipeline_engine import PipelineGraph, BlockType

class CostCategory(Enum):
    """Categories of pipeline costs."""
    COMPUTE = "compute"
    STORAGE = "storage"
    NETWORK = "network"
    LICENSING = "licensing"
    MAINTENANCE = "maintenance"

@dataclass
class CostBreakdown:
    """Breakdown of costs by category."""
    compute_cost: float = 0.0
    storage_cost: float = 0.0
    network_cost: float = 0.0
    licensing_cost: float = 0.0
    maintenance_cost: float = 0.0
    
    @property
    def total(self) -> float:
        return (
            self.compute_cost 
            + self.storage_cost 
            + self.network_cost 
            + self.licensing_cost 
            + self.maintenance_cost
        )

@dataclass
class CostResult:
    """Result of cost calculation for a pipeline."""
    total_cost_per_run: float = 0.0
    total_cost_per_hour: float = 0.0
    total_cost_per_day: float = 0.0
    total_cost_per_month: float = 0.0
    node_costs: dict[str, float] = field(default_factory=dict)
    breakdown: CostBreakdown = field(default_factory=CostBreakdown)
    most_expensive_node_id: str | None = None
    optimization_suggestions: list[str] = field(default_factory=list        )


class CostEngine:
    """
    Engine for calculating and optimizing pipeline costs.

    Computes cost metrics including:
    - Cost per run / hour / day / month
    - Per-node cost breakdown
    - Cost by category (compute, storage, network, etc.)
    - Cost optimization suggestions
    """

    def __init__(self) -> None:
        self._compute_rate_per_ms: float = 0.0001  # $ per millisecond
        self._storage_rate_per_gb: float = 0.023   # $ per GB per month
        self._network_rate_per_gb: float = 0.09    # $ per GB transferred
        self._runs_per_hour: float = 1.0
        self._base_costs = {
            BlockType.INGESTION: 0.5,
            BlockType.STORAGE: 1.0,
            BlockType.TRANSFORM: 2.0,
            BlockType.ORCHESTRATION: 0.3,
        }
    """
    Engine for calculating and optimizing pipeline costs.
    
    Computes cost metrics including:
    - Cost per run / hour / day / month
    - Per-node cost breakdown
    - Cost by category (compute, storage, network, etc.)
    - Cost optimization suggestions
    """
    
    def __init__(self) -> None:
        self._compute_rate_per_ms: float = 0.0001  # $ per millisecond
        self._storage_rate_per_gb: float = 0.023   # $ per GB per month
        self._network_rate_per_gb: float = 0.09    # $ per GB transferred
        self._runs_per_hour: float = 1.0
    
    def set_compute_rate(self, rate_per_ms: float) -> None:
        """Set the compute cost rate per millisecond."""
        self._compute_rate_per_ms = rate_per_ms
    
    def set_storage_rate(self, rate_per_gb: float) -> None:
        """Set the storage cost rate per GB per month."""
        self._storage_rate_per_gb = rate_per_gb
    
    def set_network_rate(self, rate_per_gb: float) -> None:
        """Set the network transfer cost rate per GB."""
        self._network_rate_per_gb = rate_per_gb
    
    def set_run_frequency(self, runs_per_hour: float) -> None:
        """Set the expected number of pipeline runs per hour."""
        self._runs_per_hour = runs_per_hour
    
    def calculate(self, graph: PipelineGraph) -> CostResult:
        """
        Calculate cost metrics for the given pipeline graph.

        Args:
            graph: The normalized pipeline graph to analyze.

        Returns:
            CostResult with computed cost metrics.
        """
        node_costs: dict[str, float] = {}
        total_cost = 0.0

        # Calculate cost for each node based on block type and configuration
        for node_id, node in graph.nodes.items():
            node_cost = self._calculate_node_cost(node)
            node_costs[node_id] = node_cost
            total_cost += node_cost

        # Calculate time-based costs (assuming 1 hour of operation)
        total_cost_per_run = total_cost
        total_cost_per_hour = total_cost_per_run * self._runs_per_hour
        total_cost_per_day = total_cost_per_hour * 24
        total_cost_per_month = total_cost_per_day * 30

        # Find most expensive node
        most_expensive_node_id = max(node_costs.keys(), key=lambda k: node_costs[k]) if node_costs else None

        # Generate optimization suggestions
        optimization_suggestions = self._generate_optimization_suggestions(graph, node_costs)

        return CostResult(
            total_cost_per_run=total_cost_per_run,
            total_cost_per_hour=total_cost_per_hour,
            total_cost_per_day=total_cost_per_day,
            total_cost_per_month=total_cost_per_month,
            node_costs=node_costs,
            breakdown=CostBreakdown(
                compute_cost=total_cost * 0.6,  # Assume 60% compute
                storage_cost=total_cost * 0.25,  # 25% storage
                network_cost=total_cost * 0.1,   # 10% network
                licensing_cost=total_cost * 0.03, # 3% licensing
                maintenance_cost=total_cost * 0.02 # 2% maintenance
            ),
            most_expensive_node_id=most_expensive_node_id,
            optimization_suggestions=optimization_suggestions
        )
    
    def estimate_scaling_cost(
        self, 
        graph: PipelineGraph, 
        scale_factor: float
    ) -> CostResult:
        """
        Estimate costs if the pipeline is scaled by a given factor.
        
        Args:
            graph: The normalized pipeline graph.
            scale_factor: Multiplier for throughput/volume.
            
        Returns:
            CostResult for the scaled pipeline.
        """
        # TODO: Implement scaling cost estimation
        raise NotImplementedError("CostEngine.estimate_scaling_cost() not yet implemented")
    
    def find_cost_optimizations(self, graph: PipelineGraph) -> list[dict]:
        """
        Analyze the pipeline and suggest cost optimizations.
        
        Args:
            graph: The normalized pipeline graph.
            
        Returns:
            List of optimization suggestions with estimated savings.
        """
        # TODO: Implement optimization finding logic
        raise NotImplementedError("CostEngine.find_cost_optimizations() not yet implemented")
    
    def compare_costs(
        self, 
        graph_a: PipelineGraph, 
        graph_b: PipelineGraph
    ) -> dict:
        """
        Compare costs between two pipeline configurations.
        
        Args:
            graph_a: First pipeline graph.
            graph_b: Second pipeline graph.
            
        Returns:
            Comparison dict with cost differences.
        """
        # TODO: Implement cost comparison logic
        raise NotImplementedError("CostEngine.compare_costs() not yet implemented")
    
    def project_monthly_cost(
        self, 
        graph: PipelineGraph, 
        daily_runs: int,
        data_volume_gb: float
    ) -> CostBreakdown:
        """
        Project monthly costs based on usage patterns.
        
        Args:
            graph: The normalized pipeline graph.
            daily_runs: Number of pipeline runs per day.
            data_volume_gb: Average data volume per run in GB.
            
        Returns:
            CostBreakdown with projected monthly costs.
        """
        # TODO: Implement monthly projection logic
        raise NotImplementedError("CostEngine.project_monthly_cost() not yet implemented")

    def _calculate_node_cost(self, node) -> float:
        """Calculate cost for a single node."""
        base_cost = self._base_costs.get(node.block_type, 0.5)

        # Adjust cost based on configuration
        cost_multiplier = 1.0

        # Storage nodes cost more based on data volume
        if node.block_type == BlockType.STORAGE:
            data_volume = node.configuration.get("data_volume_gb", 1.0)
            cost_multiplier *= max(1.0, data_volume / 10.0)

        # Transform nodes cost more based on complexity
        elif node.block_type == BlockType.TRANSFORM:
            complexity = node.configuration.get("complexity", 1.0)
            cost_multiplier *= complexity

        # Ingestion nodes cost more with higher throughput
        elif node.block_type == BlockType.INGESTION:
            throughput = node.configuration.get("throughput_rps", 100.0)
            cost_multiplier *= max(1.0, throughput / 1000.0)

        return base_cost * cost_multiplier

    def _generate_optimization_suggestions(self, graph, node_costs) -> list[str]:
        """Generate cost optimization suggestions."""
        suggestions = []

        # Find expensive nodes
        expensive_nodes = sorted(node_costs.items(), key=lambda x: x[1], reverse=True)[:3]

        for node_id, cost in expensive_nodes:
            node = graph.nodes.get(node_id)
            if node:
                if node.block_type == BlockType.STORAGE:
                    suggestions.append(f"Consider using cheaper storage options for {node.block.name}")
                elif node.block_type == BlockType.TRANSFORM:
                    suggestions.append(f"Optimize {node.block.name} operations to reduce compute costs")
                elif node.block_type == BlockType.INGESTION:
                    suggestions.append(f"Review data ingestion patterns for {node.block.name}")

        # General suggestions
        if len(graph.nodes) > 5:
            suggestions.append("Consider consolidating similar operations to reduce infrastructure costs")

        if any(node.block_type == BlockType.STORAGE for node in graph.nodes.values()):
            suggestions.append("Implement data lifecycle management to move cold data to cheaper storage")

        return suggestions[:5]  # Limit to 5 suggestions


