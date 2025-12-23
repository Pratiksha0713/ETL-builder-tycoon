"""
Block Library Component - Renders the ETL block library with categorized blocks.
"""

import streamlit as st
from frontend.utils.ui_helpers import render_block_category, render_section_divider


# Block definitions organized by category
BLOCK_DEFINITIONS = {
    "📥 Ingestion Blocks": [
        ("🗃️🛢️ Database Reader", "Database Reader", 
         "Connect to relational databases (MySQL, PostgreSQL, SQL Server) to read data"),
        ("📄📊 CSV Reader", "CSV Reader",
         "Read data from CSV files with automatic delimiter detection and header parsing"),
        ("🌐🔗 API Reader", "API Reader",
         "Fetch data from REST APIs with authentication and pagination support"),
        ("📊🌊 Streaming Reader", "Streaming Reader",
         "Process real-time streaming data from Kafka, Kinesis, or other streaming platforms"),
        ("📋📈 Excel Reader", "Excel Reader",
         "Read data from Excel files (.xlsx, .xls) with multiple sheet support"),
        ("🗂️💿 File System Reader", "File System Reader",
         "Read files from local or cloud storage (S3, GCS, Azure) with pattern matching"),
    ],
    "💾 Storage Blocks": [
        ("🗃️ Database Writer", "Database Writer",
         "Write data to relational databases with transaction support and error handling"),
        ("📄 CSV Writer", "CSV Writer",
         "Export data to CSV files with customizable delimiters and encoding options"),
        ("📊 Data Lake Writer", "Data Lake Writer",
         "Write data to data lakes (S3, Delta Lake) with partitioning and file format options"),
        ("💾 Cache Writer", "Cache Writer",
         "Store intermediate results in Redis, Memcached, or in-memory cache for performance"),
        ("📋 Excel Writer", "Excel Writer",
         "Export data to Excel files with formatting, multiple sheets, and chart support"),
        ("🗂️ File System Writer", "File System Writer",
         "Write files to local or cloud storage with compression and archiving options"),
    ],
    "🔄 Transform Blocks": [
        ("🔍🎯 Filter", "Filter",
         "Filter rows based on conditions, remove duplicates, or sample data"),
        ("🔀🔗 Join", "Join",
         "Combine datasets using inner, left, right, or full joins on common columns"),
        ("📈🧮 Aggregate", "Aggregate",
         "Group data and calculate aggregations (sum, count, avg, min, max)"),
        ("➕🔗 Union", "Union",
         "Combine multiple datasets with the same schema using union operations"),
        ("🏷️ Rename Columns", "Rename Columns",
         "Rename column headers and standardize naming conventions"),
        ("➗ Split", "Split",
         "Split datasets based on conditions or split columns into multiple columns"),
        ("🔢 Type Converter", "Type Converter",
         "Convert data types (string to number, date parsing, boolean conversion)"),
        ("🧹 Data Cleaner", "Data Cleaner",
         "Handle missing values, outliers, and data quality issues"),
    ],
    "🎯 Orchestration Blocks": [
        ("⏰📅 Scheduler", "Scheduler",
         "Schedule pipeline execution at specific times or intervals (cron expressions)"),
        ("🔄🔁 Loop", "Loop",
         "Iterate over datasets or repeat operations for each item in a collection"),
        ("🔀❓ Conditional", "Conditional",
         "Execute different paths based on conditions or data validation results"),
        ("📊🌿 Branch", "Branch",
         "Split pipeline execution into multiple parallel branches for concurrent processing"),
        ("🔔⚡ Trigger", "Trigger",
         "Wait for external events or file arrivals before continuing pipeline execution"),
        ("⚡🔀 Parallel", "Parallel",
         "Execute multiple operations simultaneously to improve pipeline performance"),
    ],
}


def render_block_library(canvas):
    """Render the ETL block library with categorized blocks."""
    st.markdown("### 🧱 Block Library")
    render_section_divider()
    
    # Render each category of blocks
    for category_title, blocks in BLOCK_DEFINITIONS.items():
        render_block_category(canvas, category_title, blocks, num_columns=2)
        render_section_divider()


