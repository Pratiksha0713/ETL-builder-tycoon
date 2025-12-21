"""
Mock S3 - Simulated S3 storage for pipeline simulation.
"""

from __future__ import annotations


class FakeS3:
    """
    Simulated S3 storage for pipeline testing and simulation.
    
    Provides basic S3 functionality without requiring actual AWS services.
    """
    
    def __init__(self, bucket: str = "default-bucket") -> None:
        """
        Initialize a fake S3 bucket.
        
        Args:
            bucket: The S3 bucket name.
        """
        self.bucket = bucket
        self._total_cost_units = 0.0
    
    def put_object(self, size_mb: float) -> dict[str, float | list[str]]:
        """
        Simulate putting an object to S3.
        
        Args:
            size_mb: Size of the object in megabytes.
            
        Returns:
            Dictionary with simulation metrics:
            {
                "latency_ms": size_mb * 2,
                "cost_units": size_mb * 0.01,
                "throughput": calculated throughput,
                "warnings": [...]
            }
        """
        warnings: list[str] = []
        
        # Calculate latency: size_mb * 2 ms
        latency_ms = size_mb * 2.0
        
        # Calculate cost: size_mb * 0.01
        cost_units = size_mb * 0.01
        self._total_cost_units += cost_units
        
        # Calculate throughput (MB per second)
        throughput = (size_mb / (latency_ms / 1000.0)) if latency_ms > 0 else 0.0
        
        # Generate warnings
        if size_mb > 100:
            warnings.append(f"Large object ({size_mb:.2f} MB) - consider multipart upload")
        
        if size_mb > 5000:  # 5GB
            warnings.append(f"Very large object ({size_mb:.2f} MB) - exceeds 5GB single upload limit")
        
        return {
            "latency_ms": latency_ms,
            "cost_units": cost_units,
            "throughput": throughput,
            "warnings": warnings,
        }
    
    def get_object(self, size_mb: float) -> dict[str, float | list[str]]:
        """
        Simulate getting an object from S3.
        
        Args:
            size_mb: Size of the object in megabytes.
            
        Returns:
            Dictionary with simulation metrics:
            {
                "latency_ms": size_mb * 1.5,
                "cost_units": size_mb * 0.01,
                "throughput": calculated throughput,
                "warnings": [...]
            }
        """
        warnings: list[str] = []
        
        # Calculate latency: size_mb * 1.5 ms
        latency_ms = size_mb * 1.5
        
        # Calculate cost: size_mb * 0.01
        cost_units = size_mb * 0.01
        self._total_cost_units += cost_units
        
        # Calculate throughput (MB per second)
        throughput = (size_mb / (latency_ms / 1000.0)) if latency_ms > 0 else 0.0
        
        # Generate warnings
        if size_mb > 100:
            warnings.append(f"Large object ({size_mb:.2f} MB) - download may take time")
        
        return {
            "latency_ms": latency_ms,
            "cost_units": cost_units,
            "throughput": throughput,
            "warnings": warnings,
        }
    
    def get_total_cost(self) -> float:
        """
        Get the total cost accumulated from all operations.
        
        Returns:
            Total cost units accumulated.
        """
        return self._total_cost_units
