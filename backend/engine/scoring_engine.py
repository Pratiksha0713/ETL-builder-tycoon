"""
Scoring Engine - Calculate pipeline performance scores.

Handles scoring of ETL pipelines based on various metrics
including latency, cost, throughput, and quality.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PipelineScore:
    """Represents a pipeline performance score."""
    total_score: float = 0.0
    latency_score: float = 0.0
    cost_score: float = 0.0
    throughput_score: float = 0.0
    quality_score: float = 0.0
    cost_penalty: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class ScoringEngine:
    """
    Engine for calculating pipeline performance scores.
    
    Evaluates pipelines based on multiple dimensions:
    - Latency (lower is better)
    - Cost (lower is better)
    - Throughput (higher is better)
    - Quality (higher is better)
    
    Score formula:
    total_score = latency_score + throughput_score + quality_score - cost_penalty
    """
    
    # Scoring thresholds and normalization constants
    MAX_LATENCY_MS = 10000.0  # 10 seconds - anything above gets 0 score
    IDEAL_LATENCY_MS = 100.0  # 100ms gets full score
    
    MAX_COST = 1.0  # $1.00 - anything above gets max penalty
    IDEAL_COST = 0.01  # $0.01 gets no penalty
    
    MIN_THROUGHPUT = 0.0  # 0 gets 0 score
    IDEAL_THROUGHPUT = 100000.0  # 100k/s gets full score
    
    MAX_QUALITY_SCORE = 100.0  # Perfect quality score
    
    def __init__(self) -> None:
        """Initialize the scoring engine."""
        pass
    
    def score(
        self,
        latency_ms: float = 0.0,
        cost: float = 0.0,
        throughput: float = 0.0,
        validation_errors: list[dict] | None = None,
        **kwargs
    ) -> PipelineScore:
        """
        Calculate pipeline performance score.
        
        Args:
            latency_ms: Total pipeline latency in milliseconds
            cost: Total pipeline cost in cost units
            throughput: Pipeline throughput (rows/operations per second)
            validation_errors: List of validation errors/warnings from validate()
            **kwargs: Additional optional parameters
        
        Returns:
            PipelineScore with calculated scores
        """
        # Calculate latency score (lower latency = higher score)
        latency_score = self._calculate_latency_score(latency_ms)
        
        # Calculate throughput score (higher throughput = higher score)
        throughput_score = self._calculate_throughput_score(throughput)
        
        # Calculate quality score (fewer errors = higher score)
        quality_score = self._calculate_quality_score(validation_errors or [])
        
        # Calculate cost penalty (higher cost = higher penalty)
        cost_penalty = self._calculate_cost_penalty(cost)
        
        # Calculate total score
        total_score = latency_score + throughput_score + quality_score - cost_penalty
        
        # Store cost_score for backward compatibility (inverse of penalty)
        cost_score = max(0.0, 100.0 - cost_penalty)
        
        metadata = {
            'latency_ms': latency_ms,
            'cost': cost,
            'throughput': throughput,
            'error_count': len([e for e in (validation_errors or []) if e.get('type') == 'error']),
            'warning_count': len([e for e in (validation_errors or []) if e.get('type') == 'warning']),
        }
        
        return PipelineScore(
            total_score=max(0.0, total_score),  # Ensure non-negative
            latency_score=latency_score,
            cost_score=cost_score,
            throughput_score=throughput_score,
            quality_score=quality_score,
            cost_penalty=cost_penalty,
            metadata=metadata
        )
    
    def _calculate_latency_score(self, latency_ms: float) -> float:
        """
        Calculate latency score (0-100 scale).
        
        Lower latency = higher score
        Ideal latency (100ms) = 100 points
        Max acceptable latency (10s) = 0 points
        """
        if latency_ms <= 0:
            return 0.0
        
        if latency_ms >= self.MAX_LATENCY_MS:
            return 0.0
        
        if latency_ms <= self.IDEAL_LATENCY_MS:
            return 100.0
        
        # Linear interpolation between ideal and max
        ratio = (self.MAX_LATENCY_MS - latency_ms) / (self.MAX_LATENCY_MS - self.IDEAL_LATENCY_MS)
        return max(0.0, min(100.0, ratio * 100.0))
    
    def _calculate_throughput_score(self, throughput: float) -> float:
        """
        Calculate throughput score (0-100 scale).
        
        Higher throughput = higher score
        Ideal throughput (100k/s) = 100 points
        Zero throughput = 0 points
        """
        if throughput <= 0:
            return 0.0
        
        if throughput >= self.IDEAL_THROUGHPUT:
            return 100.0
        
        # Linear scaling from 0 to ideal
        ratio = throughput / self.IDEAL_THROUGHPUT
        return max(0.0, min(100.0, ratio * 100.0))
    
    def _calculate_quality_score(self, validation_errors: list[dict]) -> float:
        """
        Calculate quality score (0-100 scale).
        
        Fewer errors/warnings = higher score
        No errors = 100 points
        Each error reduces score by 20 points
        Each warning reduces score by 5 points
        """
        error_count = len([e for e in validation_errors if e.get('type') == 'error'])
        warning_count = len([e for e in validation_errors if e.get('type') == 'warning'])
        
        # Start with perfect score
        score = self.MAX_QUALITY_SCORE
        
        # Deduct for errors (20 points each)
        score -= error_count * 20.0
        
        # Deduct for warnings (5 points each)
        score -= warning_count * 5.0
        
        return max(0.0, score)
    
    def _calculate_cost_penalty(self, cost: float) -> float:
        """
        Calculate cost penalty (0-100 scale).
        
        Higher cost = higher penalty
        Ideal cost ($0.01) = 0 penalty
        Max cost ($1.00) = 100 penalty
        """
        if cost <= 0:
            return 0.0
        
        if cost <= self.IDEAL_COST:
            return 0.0
        
        if cost >= self.MAX_COST:
            return 100.0
        
        # Linear interpolation between ideal and max
        ratio = (cost - self.IDEAL_COST) / (self.MAX_COST - self.IDEAL_COST)
        return max(0.0, min(100.0, ratio * 100.0))
