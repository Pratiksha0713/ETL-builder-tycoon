"""
Simulation module - Mock services for ETL Builder Tycoon.

Contains simulated versions of:
- Kafka (streaming)
- S3 (object storage)
- Spark (distributed processing)
- SQL (relational databases)
"""

from backend.simulation.mock_kafka import *
from backend.simulation.mock_s3 import *
from backend.simulation.mock_spark import *
from backend.simulation.mock_sql import *

