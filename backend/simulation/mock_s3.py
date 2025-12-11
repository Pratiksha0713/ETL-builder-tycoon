"""
Mock S3 - Simulated S3 storage for pipeline simulation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SimulationMetrics:
    """Standard metrics returned by all simulation classes."""
    latency_ms: float = 0.0
    cost_units: float = 0.0
    throughput: float = 0.0
    warnings: list[str] = field(default_factory=list)


@dataclass
class S3Metrics(SimulationMetrics):
    """Metrics from an S3 operation."""
    bytes_transferred: int = 0
    objects_affected: int = 0
    operation_type: str = ""


@dataclass
class S3Object:
    """Represents an object stored in S3."""
    key: str
    data: bytes
    metadata: dict[str, str] = field(default_factory=dict)
    size_bytes: int = 0
    
    def __post_init__(self) -> None:
        self.size_bytes = len(self.data)


class FakeS3:
    """
    Simulated S3 storage for pipeline testing and simulation.
    
    Provides basic S3 functionality with in-memory storage
    for testing pipelines without requiring actual AWS services.
    """
    
    # Cost simulation constants (based on AWS S3 pricing model)
    COST_PER_1K_PUT = 0.005  # Cost units per 1000 PUT requests
    COST_PER_1K_GET = 0.0004  # Cost units per 1000 GET requests
    COST_PER_GB_STORED = 0.023  # Cost units per GB stored per month
    COST_PER_GB_TRANSFER = 0.09  # Cost units per GB transferred out
    
    # Latency simulation constants
    BASE_LATENCY_MS = 20.0  # Base S3 API latency
    LATENCY_PER_MB = 10.0  # Additional latency per MB transferred
    
    def __init__(self, bucket: str) -> None:
        """
        Initialize a fake S3 bucket.
        
        Args:
            bucket: The S3 bucket name.
        """
        self.bucket = bucket
        self._objects: dict[str, S3Object] = {}
    
    def _calculate_latency(self, size_bytes: int) -> float:
        """Calculate simulated latency based on data size."""
        size_mb = size_bytes / (1024 * 1024)
        return self.BASE_LATENCY_MS + (size_mb * self.LATENCY_PER_MB)
    
    def _calculate_transfer_cost(self, size_bytes: int) -> float:
        """Calculate cost for data transfer."""
        size_gb = size_bytes / (1024 * 1024 * 1024)
        return size_gb * self.COST_PER_GB_TRANSFER
    
    def put_object(
        self, 
        key: str, 
        data: bytes, 
        metadata: dict[str, str] | None = None
    ) -> S3Metrics:
        """
        Store an object in the bucket.
        
        Args:
            key: The object key (path).
            data: The object data as bytes.
            metadata: Optional metadata dictionary.
            
        Returns:
            S3Metrics with latency, cost, throughput, and warnings.
        """
        warnings: list[str] = []
        
        obj = S3Object(
            key=key,
            data=data,
            metadata=metadata or {}
        )
        
        # Check for overwrites
        if key in self._objects:
            warnings.append(f"Overwriting existing object: {key}")
        
        # Size warnings
        if obj.size_bytes > 5 * 1024 * 1024 * 1024:  # 5GB
            warnings.append("Object exceeds 5GB - consider multipart upload")
        elif obj.size_bytes > 100 * 1024 * 1024:  # 100MB
            warnings.append("Large object detected - consider multipart upload for reliability")
        
        self._objects[key] = obj
        
        latency_ms = self._calculate_latency(obj.size_bytes)
        cost_units = self.COST_PER_1K_PUT / 1000 + self._calculate_transfer_cost(obj.size_bytes)
        throughput = (obj.size_bytes / latency_ms * 1000) if latency_ms > 0 else 0.0
        
        return S3Metrics(
            latency_ms=latency_ms,
            cost_units=cost_units,
            throughput=throughput,
            warnings=warnings,
            bytes_transferred=obj.size_bytes,
            objects_affected=1,
            operation_type="PUT"
        )
    
    def get_object(self, key: str) -> tuple[bytes | None, S3Metrics]:
        """
        Retrieve an object from the bucket.
        
        Args:
            key: The object key (path).
            
        Returns:
            Tuple of (object data or None, S3Metrics).
        """
        warnings: list[str] = []
        
        obj = self._objects.get(key)
        
        if obj is None:
            warnings.append(f"Object not found: {key}")
            return None, S3Metrics(
                latency_ms=self.BASE_LATENCY_MS,
                cost_units=self.COST_PER_1K_GET / 1000,
                throughput=0.0,
                warnings=warnings,
                bytes_transferred=0,
                objects_affected=0,
                operation_type="GET"
            )
        
        latency_ms = self._calculate_latency(obj.size_bytes)
        cost_units = self.COST_PER_1K_GET / 1000 + self._calculate_transfer_cost(obj.size_bytes)
        throughput = (obj.size_bytes / latency_ms * 1000) if latency_ms > 0 else 0.0
        
        return obj.data, S3Metrics(
            latency_ms=latency_ms,
            cost_units=cost_units,
            throughput=throughput,
            warnings=warnings,
            bytes_transferred=obj.size_bytes,
            objects_affected=1,
            operation_type="GET"
        )
    
    def delete_object(self, key: str) -> S3Metrics:
        """
        Delete an object from the bucket.
        
        Args:
            key: The object key (path).
            
        Returns:
            S3Metrics with operation details.
        """
        warnings: list[str] = []
        
        if key not in self._objects:
            warnings.append(f"Object not found for deletion: {key}")
            objects_affected = 0
        else:
            del self._objects[key]
            objects_affected = 1
        
        return S3Metrics(
            latency_ms=self.BASE_LATENCY_MS,
            cost_units=0.0,  # Deletes are free
            throughput=0.0,
            warnings=warnings,
            bytes_transferred=0,
            objects_affected=objects_affected,
            operation_type="DELETE"
        )
    
    def list_objects(self, prefix: str = "") -> tuple[list[str], S3Metrics]:
        """
        List objects in the bucket with optional prefix filter.
        
        Args:
            prefix: Optional prefix to filter objects.
            
        Returns:
            Tuple of (list of keys, S3Metrics).
        """
        warnings: list[str] = []
        
        keys = [k for k in self._objects.keys() if k.startswith(prefix)]
        
        if len(keys) > 1000:
            warnings.append("Result truncated - more than 1000 objects match")
        
        return keys, S3Metrics(
            latency_ms=self.BASE_LATENCY_MS,
            cost_units=self.COST_PER_1K_GET / 1000,
            throughput=len(keys),
            warnings=warnings,
            bytes_transferred=0,
            objects_affected=len(keys),
            operation_type="LIST"
        )
    
    def copy_object(self, source_key: str, dest_key: str) -> S3Metrics:
        """
        Copy an object within the bucket.
        
        Args:
            source_key: Source object key.
            dest_key: Destination object key.
            
        Returns:
            S3Metrics with operation details.
        """
        warnings: list[str] = []
        
        source_obj = self._objects.get(source_key)
        
        if source_obj is None:
            warnings.append(f"Source object not found: {source_key}")
            return S3Metrics(
                latency_ms=self.BASE_LATENCY_MS,
                cost_units=0.0,
                throughput=0.0,
                warnings=warnings,
                bytes_transferred=0,
                objects_affected=0,
                operation_type="COPY"
            )
        
        if dest_key in self._objects:
            warnings.append(f"Overwriting existing object: {dest_key}")
        
        self._objects[dest_key] = S3Object(
            key=dest_key,
            data=source_obj.data,
            metadata=source_obj.metadata.copy()
        )
        
        latency_ms = self._calculate_latency(source_obj.size_bytes)
        cost_units = self.COST_PER_1K_PUT / 1000  # Copy is charged as PUT
        throughput = (source_obj.size_bytes / latency_ms * 1000) if latency_ms > 0 else 0.0
        
        return S3Metrics(
            latency_ms=latency_ms,
            cost_units=cost_units,
            throughput=throughput,
            warnings=warnings,
            bytes_transferred=source_obj.size_bytes,
            objects_affected=1,
            operation_type="COPY"
        )
    
    def get_bucket_size(self) -> tuple[int, S3Metrics]:
        """
        Calculate total size of all objects in the bucket.
        
        Returns:
            Tuple of (total size in bytes, S3Metrics).
        """
        total_size = sum(obj.size_bytes for obj in self._objects.values())
        
        warnings: list[str] = []
        size_gb = total_size / (1024 * 1024 * 1024)
        if size_gb > 100:
            warnings.append(f"Large bucket: {size_gb:.2f} GB stored")
        
        return total_size, S3Metrics(
            latency_ms=self.BASE_LATENCY_MS,
            cost_units=0.0,
            throughput=0.0,
            warnings=warnings,
            bytes_transferred=0,
            objects_affected=len(self._objects),
            operation_type="SIZE"
        )
