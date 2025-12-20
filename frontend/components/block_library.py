import streamlit as st


def render_block_library(canvas):
    """Render the ETL block library with categorized blocks."""
    st.markdown("### 🧱 Block Library")
    st.markdown("---")

    # Ingestion Blocks
    st.markdown("#### 📥 Ingestion Blocks")
    ingestion_col1, ingestion_col2 = st.columns(2)

    with ingestion_col1:
        if st.button("🗃️🛢️ Database Reader", use_container_width=True,
                     help="Connect to relational databases (MySQL, PostgreSQL, SQL Server) to read data"):
            block_id = canvas.add_block("Database Reader")
            st.success(f"Added Database Reader block (ID: {block_id}) to canvas")
        if st.button("📄📊 CSV Reader", use_container_width=True,
                     help="Read data from CSV files with automatic delimiter detection and header parsing"):
            block_id = canvas.add_block("CSV Reader")
            st.success(f"Added CSV Reader block (ID: {block_id}) to canvas")
        if st.button("🌐🔗 API Reader", use_container_width=True,
                     help="Fetch data from REST APIs with authentication and pagination support"):
            block_id = canvas.add_block("API Reader")
            st.success(f"Added API Reader block (ID: {block_id}) to canvas")

    with ingestion_col2:
        if st.button("📊🌊 Streaming Reader", use_container_width=True,
                     help="Process real-time streaming data from Kafka, Kinesis, or other streaming platforms"):
            block_id = canvas.add_block("Streaming Reader")
            st.success(f"Added Streaming Reader block (ID: {block_id}) to canvas")
        if st.button("📋📈 Excel Reader", use_container_width=True,
                     help="Read data from Excel files (.xlsx, .xls) with multiple sheet support"):
            block_id = canvas.add_block("Excel Reader")
            st.success(f"Added Excel Reader block (ID: {block_id}) to canvas")
        if st.button("🗂️💿 File System Reader", use_container_width=True,
                     help="Read files from local or cloud storage (S3, GCS, Azure) with pattern matching"):
            block_id = canvas.add_block("File System Reader")
            st.success(f"Added File System Reader block (ID: {block_id}) to canvas")

    st.markdown("---")

    # Storage Blocks
    st.markdown("#### 💾 Storage Blocks")
    storage_col1, storage_col2 = st.columns(2)

    with storage_col1:
        if st.button("🗃️ Database Writer", use_container_width=True,
                     help="Write data to relational databases with transaction support and error handling"):
            block_id = canvas.add_block("Database Writer")
            st.success(f"Added Database Writer block (ID: {block_id}) to canvas")
        if st.button("📄 CSV Writer", use_container_width=True,
                     help="Export data to CSV files with customizable delimiters and encoding options"):
            block_id = canvas.add_block("CSV Writer")
            st.success(f"Added CSV Writer block (ID: {block_id}) to canvas")
        if st.button("📊 Data Lake Writer", use_container_width=True,
                     help="Write data to data lakes (S3, Delta Lake) with partitioning and file format options"):
            block_id = canvas.add_block("Data Lake Writer")
            st.success(f"Added Data Lake Writer block (ID: {block_id}) to canvas")

    with storage_col2:
        if st.button("💾 Cache Writer", use_container_width=True,
                     help="Store intermediate results in Redis, Memcached, or in-memory cache for performance"):
            block_id = canvas.add_block("Cache Writer")
            st.success(f"Added Cache Writer block (ID: {block_id}) to canvas")
        if st.button("📋 Excel Writer", use_container_width=True,
                     help="Export data to Excel files with formatting, multiple sheets, and chart support"):
            block_id = canvas.add_block("Excel Writer")
            st.success(f"Added Excel Writer block (ID: {block_id}) to canvas")
        if st.button("🗂️ File System Writer", use_container_width=True,
                     help="Write files to local or cloud storage with compression and archiving options"):
            block_id = canvas.add_block("File System Writer")
            st.success(f"Added File System Writer block (ID: {block_id}) to canvas")

    st.markdown("---")

    # Transform Blocks
    st.markdown("#### 🔄 Transform Blocks")
    transform_col1, transform_col2 = st.columns(2)

    with transform_col1:
        if st.button("🔍🎯 Filter", use_container_width=True,
                     help="Filter rows based on conditions, remove duplicates, or sample data"):
            block_id = canvas.add_block("Filter")
            st.success(f"Added Filter block (ID: {block_id}) to canvas")
        if st.button("🔀🔗 Join", use_container_width=True,
                     help="Combine datasets using inner, left, right, or full joins on common columns"):
            block_id = canvas.add_block("Join")
            st.success(f"Added Join block (ID: {block_id}) to canvas")
        if st.button("📈🧮 Aggregate", use_container_width=True,
                     help="Group data and calculate aggregations (sum, count, avg, min, max)"):
            block_id = canvas.add_block("Aggregate")
            st.success(f"Added Aggregate block (ID: {block_id}) to canvas")
        if st.button("➕🔗 Union", use_container_width=True,
                     help="Combine multiple datasets with the same schema using union operations"):
            block_id = canvas.add_block("Union")
            st.success(f"Added Union block (ID: {block_id}) to canvas")

    with transform_col2:
        if st.button("🏷️ Rename Columns", use_container_width=True,
                     help="Rename column headers and standardize naming conventions"):
            block_id = canvas.add_block("Rename Columns")
            st.success(f"Added Rename Columns block (ID: {block_id}) to canvas")
        if st.button("➗ Split", use_container_width=True,
                     help="Split datasets based on conditions or split columns into multiple columns"):
            block_id = canvas.add_block("Split")
            st.success(f"Added Split block (ID: {block_id}) to canvas")
        if st.button("🔢 Type Converter", use_container_width=True,
                     help="Convert data types (string to number, date parsing, boolean conversion)"):
            block_id = canvas.add_block("Type Converter")
            st.success(f"Added Type Converter block (ID: {block_id}) to canvas")
        if st.button("🧹 Data Cleaner", use_container_width=True,
                     help="Handle missing values, outliers, and data quality issues"):
            block_id = canvas.add_block("Data Cleaner")
            st.success(f"Added Data Cleaner block (ID: {block_id}) to canvas")

    st.markdown("---")

    # Orchestration Blocks
    st.markdown("#### 🎯 Orchestration Blocks")
    orchestration_col1, orchestration_col2 = st.columns(2)

    with orchestration_col1:
        if st.button("⏰📅 Scheduler", use_container_width=True,
                     help="Schedule pipeline execution at specific times or intervals (cron expressions)"):
            block_id = canvas.add_block("Scheduler")
            st.success(f"Added Scheduler block (ID: {block_id}) to canvas")
        if st.button("🔄🔁 Loop", use_container_width=True,
                     help="Iterate over datasets or repeat operations for each item in a collection"):
            block_id = canvas.add_block("Loop")
            st.success(f"Added Loop block (ID: {block_id}) to canvas")
        if st.button("🔀❓ Conditional", use_container_width=True,
                     help="Execute different paths based on conditions or data validation results"):
            block_id = canvas.add_block("Conditional")
            st.success(f"Added Conditional block (ID: {block_id}) to canvas")

    with orchestration_col2:
        if st.button("📊🌿 Branch", use_container_width=True,
                     help="Split pipeline execution into multiple parallel branches for concurrent processing"):
            block_id = canvas.add_block("Branch")
            st.success(f"Added Branch block (ID: {block_id}) to canvas")
        if st.button("🔔⚡ Trigger", use_container_width=True,
                     help="Wait for external events or file arrivals before continuing pipeline execution"):
            block_id = canvas.add_block("Trigger")
            st.success(f"Added Trigger block (ID: {block_id}) to canvas")
        if st.button("⚡🔀 Parallel", use_container_width=True,
                     help="Execute multiple operations simultaneously to improve pipeline performance"):
            block_id = canvas.add_block("Parallel")
            st.success(f"Added Parallel block (ID: {block_id}) to canvas")

