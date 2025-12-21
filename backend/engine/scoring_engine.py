"""
Scoring Engine - Pipeline scoring and badge system for ETL Builder Tycoon.

Computes scores based on latency, throughput, cost, and quality metrics.
Awards badges for exceptional performance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ScoreBreakdown:
    """Breakdown of individual score components."""
    latency_score: float = 0.0
    throughput_score: float = 0.0
    quality_score: float = 0.0
    cost_penalty: float = 0.0
    final_score: float = 0.0


@dataclass
class ScoringResult:
    """Result of pipeline scoring."""
    final_score: float = 0.0
    breakdown: ScoreBreakdown = field(default_factory=ScoreBreakdown)
    badges: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class ScoringEngine:
    """
    Engine for computing pipeline scores and awarding badges.
    
    Computes scores based on:
    - Latency: max(0, 100 - latency_total/10)
    - Throughput: throughput_min / 10
    - Quality: 80 if no warnings else 40
    - Cost penalty: cost_total / 5
    
    Final Score = (latency_score + throughput_score + quality_score) - cost_penalty
    
    Awards badges:
    - Zero Latency: latency < 200ms
    - Cost Saver: cost < 10 units
    - Performance Guru: score > 150
    """
    
    def __init__(self) -> None:
        """Initialize the scoring engine."""
        pass
    
    def compute_score(
        self,
        latency_total: float,
        throughput_min: float,
        cost_total: float,
        quality_score: float,
        warnings: list[str] | None = None
    ) -> ScoringResult:
        """
        Compute the pipeline score based on metrics.
        
        Args:
            latency_total: Total latency in milliseconds.
            throughput_min: Minimum throughput (records per second).
            cost_total: Total cost units.
            quality_score: Quality score (0-100).
            warnings: List of warnings from simulation (optional).
            
        Returns:
            ScoringResult with final score, breakdown, and badges.
        """
        result_warnings: list[str] = []
        
        # Compute latency score: max(0, 100 - latency_total/10)
        latency_score = max(0.0, 100.0 - (latency_total / 10.0))
        
        # Compute throughput score: throughput_min / 10
        throughput_score = throughput_min / 10.0
        
        # Compute quality score: 80 if no warnings else 40
        if warnings is None:
            warnings = []
        
        if len(warnings) == 0:
            computed_quality_score = 80.0
        else:
            computed_quality_score = 40.0
            result_warnings.append(f"Quality reduced due to {len(warnings)} warning(s)")
        
        # Use provided quality_score if available, otherwise use computed
        if quality_score > 0:
            # Blend provided quality score with warning-based score
            quality_score_final = (quality_score * 0.5) + (computed_quality_score * 0.5)
        else:
            quality_score_final = computed_quality_score
        
        # Compute cost penalty: cost_total / 5
        cost_penalty = cost_total / 5.0
        
        # Compute final score: (latency_score + throughput_score + quality_score) - cost_penalty
        final_score = (latency_score + throughput_score + quality_score_final) - cost_penalty
        
        # Ensure score doesn't go negative
        final_score = max(0.0, final_score)
        
        # Create breakdown
        breakdown = ScoreBreakdown(
            latency_score=latency_score,
            throughput_score=throughput_score,
            quality_score=quality_score_final,
            cost_penalty=cost_penalty,
            final_score=final_score
        )
        
        # Award badges
        badges: list[str] = []
        
        # Zero Latency badge: latency < 200ms
        if latency_total < 200.0:
            badges.append("Zero Latency")
        
        # Cost Saver badge: cost < 10 units
        if cost_total < 10.0:
            badges.append("Cost Saver")
        
        # Performance Guru badge: score > 150
        if final_score > 150.0:
            badges.append("Performance Guru")
        
        return ScoringResult(
            final_score=final_score,
            breakdown=breakdown,
            badges=badges,
            warnings=result_warnings
        )
    
    def score_from_simulation(self, simulation_results: dict[str, Any]) -> ScoringResult:
        """
        Compute score from pipeline simulation results.
        
        Args:
            simulation_results: Dictionary from PipelineEngine.simulate() containing:
                - latency_total
                - throughput_min
                - cost_total
                - quality_score
                - node_results (for collecting warnings)
                
        Returns:
            ScoringResult with computed score and badges.
        """
        # Extract metrics from simulation results
        latency_total = simulation_results.get("latency_total", 0.0)
        throughput_min = simulation_results.get("throughput_min", 0.0)
        cost_total = simulation_results.get("cost_total", 0.0)
        quality_score = simulation_results.get("quality_score", 0.0)
        
        # Collect all warnings from node results
        all_warnings: list[str] = []
        node_results = simulation_results.get("node_results", {})
        for node_id, node_metrics in node_results.items():
            node_warnings = node_metrics.get("warnings", [])
            all_warnings.extend(node_warnings)
        
        return self.compute_score(
            latency_total=latency_total,
            throughput_min=throughput_min,
            cost_total=cost_total,
            quality_score=quality_score,
            warnings=all_warnings if all_warnings else None
        )
