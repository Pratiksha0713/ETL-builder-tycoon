"""
Mock SQL - Simulated SQL database for pipeline simulation.
"""

from __future__ import annotations

import sqlite3
import time
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
class QueryMetrics(SimulationMetrics):
    """Metrics from a SQL query execution."""
    rows_affected: int = 0
    rows_returned: int = 0
    execution_time_ms: float = 0.0
    operations_estimate: int = 0


@dataclass
class QueryResult:
    """Result of a SQL query execution."""
    data: list[dict] = field(default_factory=list)
    metrics: QueryMetrics = field(default_factory=QueryMetrics)
    success: bool = True
    error: str | None = None


class FakeSQL:
    """
    Simulated SQL database using SQLite for pipeline testing and simulation.
    
    Provides basic SQL functionality with an in-memory SQLite backend
    for testing pipelines without requiring an external database.
    """
    
    # Latency simulation constants
    BASE_LATENCY_MS = 0.5  # Base latency per query
    LATENCY_PER_CHAR = 0.01  # Additional latency per character in query
    
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
    
    def _estimate_operations(self, query: str) -> int:
        """
        Estimate the number of operations for a query.
        
        Uses query complexity heuristics based on keywords and length.
        """
        query_upper = query.upper()
        
        # Base operations from query length
        operations = len(query)
        
        # Additional operations for complex keywords
        if "JOIN" in query_upper:
            operations += 500
        if "GROUP BY" in query_upper:
            operations += 300
        if "ORDER BY" in query_upper:
            operations += 200
        if "HAVING" in query_upper:
            operations += 150
        if "DISTINCT" in query_upper:
            operations += 100
        if "UNION" in query_upper:
            operations += 400
        if "SUBQUERY" in query_upper or query_upper.count("SELECT") > 1:
            operations += 600
        
        return operations
    
    def _calculate_latency(self, query: str) -> float:
        """Calculate simulated query latency based on query length."""
        return self.BASE_LATENCY_MS + (len(query) * self.LATENCY_PER_CHAR)
    
    def _generate_warnings(self, query: str, rows_returned: int) -> list[str]:
        """Generate warnings based on query characteristics."""
        warnings: list[str] = []
        query_upper = query.upper()
        
        # Check for potential performance issues
        if "SELECT *" in query_upper:
            warnings.append("SELECT * may return unnecessary columns")
        
        if "WHERE" not in query_upper and query_upper.startswith("SELECT"):
            warnings.append("Query has no WHERE clause - may return large result set")
        
        if rows_returned > 10000:
            warnings.append(f"Large result set: {rows_returned} rows returned")
        
        if query_upper.count("JOIN") > 3:
            warnings.append("Multiple JOINs detected - consider query optimization")
        
        if "LIKE '%" in query_upper:
            warnings.append("Leading wildcard in LIKE may prevent index usage")
        
        return warnings
    
    def execute(self, query: str, params: tuple[Any, ...] = ()) -> QueryResult:
        """
        Execute a SQL query.
        
        Args:
            query: The SQL query to execute.
            params: Query parameters for parameterized queries.
            
        Returns:
            QueryResult with data and metrics including latency, cost, throughput, and warnings.
        """
        if not self._cursor or not self._connection:
            return QueryResult(
                success=False,
                error="Database not connected. Call connect() first.",
                metrics=QueryMetrics(
                    warnings=["Database connection not established"]
                )
            )
        
        # Calculate simulated latency and cost
        latency_ms = self._calculate_latency(query)
        operations_estimate = self._estimate_operations(query)
        cost_units = operations_estimate / 1000.0
        
        start_time = time.perf_counter()
        
        try:
            self._cursor.execute(query, params)
            self._connection.commit()
            
            # Fetch results if it's a SELECT query
            rows_data: list[dict] = []
            if query.strip().upper().startswith("SELECT"):
                rows = self._cursor.fetchall()
                rows_data = [dict(row) for row in rows]
            
            end_time = time.perf_counter()
            execution_time_ms = (end_time - start_time) * 1000
            
            # Calculate throughput (rows per second)
            throughput = (len(rows_data) / execution_time_ms * 1000) if execution_time_ms > 0 else 0.0
            
            # Generate warnings
            warnings = self._generate_warnings(query, len(rows_data))
            
            metrics = QueryMetrics(
                latency_ms=latency_ms,
                cost_units=cost_units,
                throughput=throughput,
                warnings=warnings,
                rows_affected=self._cursor.rowcount,
                rows_returned=len(rows_data),
                execution_time_ms=execution_time_ms,
                operations_estimate=operations_estimate
            )
            
            return QueryResult(
                data=rows_data,
                metrics=metrics,
                success=True
            )
            
        except sqlite3.Error as e:
            end_time = time.perf_counter()
            execution_time_ms = (end_time - start_time) * 1000
            
            metrics = QueryMetrics(
                latency_ms=latency_ms,
                cost_units=cost_units,
                throughput=0.0,
                warnings=[f"Query failed: {str(e)}"],
                execution_time_ms=execution_time_ms,
                operations_estimate=operations_estimate
            )
            
            return QueryResult(
                metrics=metrics,
                success=False,
                error=str(e)
            )
    
    def fetch_all(self, query: str, params: tuple[Any, ...] = ()) -> list[dict]:
        """
        Execute a query and fetch all results.
        
        Args:
            query: The SQL query to execute.
            params: Query parameters.
            
        Returns:
            List of rows as dictionaries.
        """
        result = self.execute(query, params)
        return result.data if result.success else []
    
    def fetch_one(self, query: str, params: tuple[Any, ...] = ()) -> dict | None:
        """
        Execute a query and fetch a single result.
        
        Args:
            query: The SQL query to execute.
            params: Query parameters.
            
        Returns:
            Single row as dictionary, or None if no results.
        """
        result = self.execute(query, params)
        if result.success and result.data:
            return result.data[0]
        return None
    
    def insert(self, table: str, data: dict[str, Any]) -> int:
        """
        Insert a row into a table.
        
        Args:
            table: The table name.
            data: Column-value pairs to insert.
            
        Returns:
            The rowid of the inserted row, or -1 on failure.
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        result = self.execute(query, tuple(data.values()))
        
        if result.success and self._cursor:
            return self._cursor.lastrowid or -1
        return -1
    
    def bulk_insert(self, table: str, rows: list[dict[str, Any]]) -> int:
        """
        Insert multiple rows into a table.
        
        Args:
            table: The table name.
            rows: List of column-value pairs to insert.
            
        Returns:
            Number of rows inserted.
        """
        if not rows:
            return 0
        
        columns = ", ".join(rows[0].keys())
        placeholders = ", ".join("?" * len(rows[0]))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        inserted = 0
        for row in rows:
            result = self.execute(query, tuple(row.values()))
            if result.success:
                inserted += 1
        
        return inserted
    
    def create_table(self, table: str, schema: dict[str, str]) -> None:
        """
        Create a table with the given schema.
        
        Args:
            table: The table name.
            schema: Column name to SQL type mapping.
        """
        columns = ", ".join(f"{col} {dtype}" for col, dtype in schema.items())
        query = f"CREATE TABLE IF NOT EXISTS {table} ({columns})"
        self.execute(query)
    
    def drop_table(self, table: str) -> None:
        """
        Drop a table if it exists.
        
        Args:
            table: The table name.
        """
        query = f"DROP TABLE IF EXISTS {table}"
        self.execute(query)
    
    def __enter__(self) -> FakeSQL:
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.disconnect()
