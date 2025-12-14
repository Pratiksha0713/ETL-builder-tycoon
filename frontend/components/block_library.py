import streamlit as st


def render_block_library():
    """Render the ETL block library with categorized blocks."""
    st.markdown("### 🧱 Block Library")
    st.markdown("---")

    # Ingestion Blocks
    st.markdown("#### 📥 Ingestion Blocks")
    ingestion_col1, ingestion_col2 = st.columns(2)

    with ingestion_col1:
        if st.button("🗃️🛢️ Database Reader", use_container_width=True,
                     help="Connect to relational databases (MySQL, PostgreSQL, SQL Server) to read data"):
            st.info("Database Reader block selected")
        if st.button("📄📊 CSV Reader", use_container_width=True,
                     help="Read data from CSV files with automatic delimiter detection and header parsing"):
            st.info("CSV Reader block selected")
        if st.button("🌐🔗 API Reader", use_container_width=True,
                     help="Fetch data from REST APIs with authentication and pagination support"):
            st.info("API Reader block selected")

    with ingestion_col2:
        if st.button("📊🌊 Streaming Reader", use_container_width=True,
                     help="Process real-time streaming data from Kafka, Kinesis, or other streaming platforms"):
            st.info("Streaming Reader block selected")
        if st.button("📋📈 Excel Reader", use_container_width=True,
                     help="Read data from Excel files (.xlsx, .xls) with multiple sheet support"):
            st.info("Excel Reader block selected")
        if st.button("🗂️💿 File System Reader", use_container_width=True,
                     help="Read files from local or cloud storage (S3, GCS, Azure) with pattern matching"):
            st.info("File System Reader block selected")

    st.markdown("---")

    # Storage Blocks
    st.markdown("#### 💾 Storage Blocks")
    storage_col1, storage_col2 = st.columns(2)

    with storage_col1:
        if st.button("🗃️ Database Writer", use_container_width=True,
                     help="Write data to relational databases with transaction support and error handling"):
            st.info("Database Writer block selected")
        if st.button("📄 CSV Writer", use_container_width=True,
                     help="Export data to CSV files with customizable delimiters and encoding options"):
            st.info("CSV Writer block selected")
        if st.button("📊 Data Lake Writer", use_container_width=True,
                     help="Write data to data lakes (S3, Delta Lake) with partitioning and file format options"):
            st.info("Data Lake Writer block selected")

    with storage_col2:
        if st.button("💾 Cache Writer", use_container_width=True,
                     help="Store intermediate results in Redis, Memcached, or in-memory cache for performance"):
            st.info("Cache Writer block selected")
        if st.button("📋 Excel Writer", use_container_width=True,
                     help="Export data to Excel files with formatting, multiple sheets, and chart support"):
            st.info("Excel Writer block selected")
        if st.button("🗂️ File System Writer", use_container_width=True,
                     help="Write files to local or cloud storage with compression and archiving options"):
            st.info("File System Writer block selected")

    st.markdown("---")

    # Transform Blocks
    st.markdown("#### 🔄 Transform Blocks")
    transform_col1, transform_col2 = st.columns(2)

    with transform_col1:
        if st.button("🔍🎯 Filter", use_container_width=True,
                     help="Filter rows based on conditions, remove duplicates, or sample data"):
            st.info("Filter block selected")
        if st.button("🔀🔗 Join", use_container_width=True,
                     help="Combine datasets using inner, left, right, or full joins on common columns"):
            st.info("Join block selected")
        if st.button("📈🧮 Aggregate", use_container_width=True,
                     help="Group data and calculate aggregations (sum, count, avg, min, max)"):
            st.info("Aggregate block selected")
        if st.button("➕🔗 Union", use_container_width=True,
                     help="Combine multiple datasets with the same schema using union operations"):
            st.info("Union block selected")

    with transform_col2:
        if st.button("🏷️ Rename Columns", use_container_width=True,
                     help="Rename column headers and standardize naming conventions"):
            st.info("Rename Columns block selected")
        if st.button("➗ Split", use_container_width=True,
                     help="Split datasets based on conditions or split columns into multiple columns"):
            st.info("Split block selected")
        if st.button("🔢 Type Converter", use_container_width=True,
                     help="Convert data types (string to number, date parsing, boolean conversion)"):
            st.info("Type Converter block selected")
        if st.button("🧹 Data Cleaner", use_container_width=True,
                     help="Handle missing values, outliers, and data quality issues"):
            st.info("Data Cleaner block selected")

    st.markdown("---")

    # Orchestration Blocks
    st.markdown("#### 🎯 Orchestration Blocks")
    orchestration_col1, orchestration_col2 = st.columns(2)

    with orchestration_col1:
        if st.button("⏰📅 Scheduler", use_container_width=True,
                     help="Schedule pipeline execution at specific times or intervals (cron expressions)"):
            st.info("Scheduler block selected")
        if st.button("🔄🔁 Loop", use_container_width=True,
                     help="Iterate over datasets or repeat operations for each item in a collection"):
            st.info("Loop block selected")
        if st.button("🔀❓ Conditional", use_container_width=True,
                     help="Execute different paths based on conditions or data validation results"):
            st.info("Conditional block selected")

    with orchestration_col2:
        if st.button("📊🌿 Branch", use_container_width=True,
                     help="Split pipeline execution into multiple parallel branches for concurrent processing"):
            st.info("Branch block selected")
        if st.button("🔔⚡ Trigger", use_container_width=True,
                     help="Wait for external events or file arrivals before continuing pipeline execution"):
            st.info("Trigger block selected")
        if st.button("⚡🔀 Parallel", use_container_width=True,
                     help="Execute multiple operations simultaneously to improve pipeline performance"):
            st.info("Parallel block selected")