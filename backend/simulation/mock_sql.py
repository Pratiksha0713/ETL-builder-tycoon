"""
Mock SQL - Simulated SQL database for pipeline simulation.
"""

from __future__ import annotations

import sqlite3
from typing import Any


class FakeSQL:
    """
    Simulated SQL database using SQLite for pipeline testing and simulation.
    
    Provides basic SQL functionality with an in-memory SQLite backend
    for testing pipelines without requiring an external database.
    """
    
    def __init__(self, database: str = ":memory:") -> None:
        """
        Initialize a fake SQL database.
        
        Args:
            database: Path to SQLite database file, or ":memory:" for in-memory.
        """
        self.database = database
        self._connection: sqlite3.Connection | None = None
        self._cursor: sqlite3.Cursor | None = None
    
    def connect(self) -> None:
        """Establish connection to the database."""
        self._connection = sqlite3.connect(self.database)
        self._connection.row_factory = sqlite3.Row
        self._cursor = self._connection.cursor()
    
    def disconnect(self) -> None:
        """Close the database connection."""
        if self._cursor:
            self._cursor.close()
            self._cursor = None
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def execute(self, query: str) -> dict[str, Any]:
        """
        Execute a SQL query.
        
        Calculates:
        - op_estimate = len(query)
        - latency = op_estimate * 0.3 ms
        - cost = op_estimate * 0.001
        
        Args:
            query: The SQL query to execute.
            
        Returns:
            Dictionary with simulation metrics:
            {
                "latency_ms": op_estimate * 0.3,
                "cost_units": op_estimate * 0.001,
                "throughput": calculated throughput,
                "warnings": [...]
            }
        """
        warnings: list[str] = []
        
        # Ensure connection is established
        if not self._connection or not self._cursor:
            self.connect()
        
        # Calculate operation estimate and metrics
        op_estimate = len(query)
        latency_ms = op_estimate * 0.3
        cost_units = op_estimate * 0.001
        
        # Execute the query
        try:
            self._cursor.execute(query)
            self._connection.commit()
            
            # Try to fetch results if it's a SELECT query
            rows_data = []
            if query.strip().upper().startswith("SELECT"):
                rows = self._cursor.fetchall()
                rows_data = [dict(row) for row in rows]
            
            # Calculate throughput (rows per second)
            throughput = (len(rows_data) / (latency_ms / 1000.0)) if latency_ms > 0 else 0.0
            
            # Generate warnings
            if op_estimate > 1000:
                warnings.append(f"Very long query ({op_estimate} chars) - may be slow")
            
            if "SELECT *" in query.upper():
                warnings.append("SELECT * may return unnecessary columns")
            
            if "WHERE" not in query.upper() and query.strip().upper().startswith("SELECT"):
                warnings.append("Query has no WHERE clause - may return large result set")
            
            if len(rows_data) > 10000:
                warnings.append(f"Large result set: {len(rows_data)} rows returned")
            
            return {
                "latency_ms": latency_ms,
                "cost_units": cost_units,
                "throughput": throughput,
                "warnings": warnings,
                "rows_returned": len(rows_data),
                "success": True,
            }
            
        except sqlite3.Error as e:
            warnings.append(f"Query failed: {str(e)}")
            return {
                "latency_ms": latency_ms,
                "cost_units": cost_units,
                "throughput": 0.0,
                "warnings": warnings,
                "rows_returned": 0,
                "success": False,
                "error": str(e),
            }
    
    def __enter__(self) -> "FakeSQL":
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.disconnect()
