import time
from typing import Any, Dict


class FakeS3:
    def __init__(self, bucket_name: str, read_latency_ms: float = 50.0, write_latency_ms: float = 100.0):
        self.bucket_name = bucket_name
        self.storage: Dict[str, Any] = {}
        self.read_latency_ms = read_latency_ms
        self.write_latency_ms = write_latency_ms

    def put_object(self, key: str, data: Any) -> Dict[str, float]:
        """Store an object with simulated write latency."""
        # Simulate write latency
        time.sleep(self.write_latency_ms / 1000.0)

        self.storage[key] = data

        return {
            "latency_ms": self.write_latency_ms,
            "operation": "put_object"
        }

    def get_object(self, key: str) -> tuple[Any, Dict[str, float]]:
        """Retrieve an object with simulated read latency."""
        # Simulate read latency
        time.sleep(self.read_latency_ms / 1000.0)

        data = self.storage.get(key)

        return data, {
            "latency_ms": self.read_latency_ms,
            "operation": "get_object",
            "found": data is not None
        }

