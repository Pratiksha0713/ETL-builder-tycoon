"""
Mock SQL - Simulated SQL database for pipeline simulation.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from typing import Any


@dataclass
class QueryMetrics:
    """Metrics from a SQL query execution."""
    rows_affected: int = 0
    execution_time_ms: float = 0.0
    rows_returned: int = 0


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
    
    def execute(self, query: str, params: tuple[Any, ...] = ()) -> QueryMetrics:
        """
        Execute a SQL query.
        
        Args:
            query: The SQL query to execute.
            params: Query parameters for parameterized queries.
            
        Returns:
            QueryMetrics with execution details.
        """
        pass
    
    def fetch_all(self, query: str, params: tuple[Any, ...] = ()) -> list[dict]:
        """
        Execute a query and fetch all results.
        
        Args:
            query: The SQL query to execute.
            params: Query parameters.
            
        Returns:
            List of rows as dictionaries.
        """
        pass
    
    def fetch_one(self, query: str, params: tuple[Any, ...] = ()) -> dict | None:
        """
        Execute a query and fetch a single result.
        
        Args:
            query: The SQL query to execute.
            params: Query parameters.
            
        Returns:
            Single row as dictionary, or None if no results.
        """
        pass
    
    def insert(self, table: str, data: dict[str, Any]) -> int:
        """
        Insert a row into a table.
        
        Args:
            table: The table name.
            data: Column-value pairs to insert.
            
        Returns:
            The rowid of the inserted row.
        """
        pass
    
    def bulk_insert(self, table: str, rows: list[dict[str, Any]]) -> int:
        """
        Insert multiple rows into a table.
        
        Args:
            table: The table name.
            rows: List of column-value pairs to insert.
            
        Returns:
            Number of rows inserted.
        """
        pass
    
    def create_table(self, table: str, schema: dict[str, str]) -> None:
        """
        Create a table with the given schema.
        
        Args:
            table: The table name.
            schema: Column name to SQL type mapping.
        """
        pass
    
    def drop_table(self, table: str) -> None:
        """
        Drop a table if it exists.
        
        Args:
            table: The table name.
        """
        pass
    
    def __enter__(self) -> FakeSQL:
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.disconnect()
