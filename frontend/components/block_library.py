import streamlit as st


def render_block_library():
    """Render the ETL block library with categorized blocks."""
    st.markdown("### 🧱 Block Library")
    st.markdown("---")

    # Ingestion Blocks
    st.markdown("#### 📥 Ingestion Blocks")
    ingestion_col1, ingestion_col2 = st.columns(2)

    with ingestion_col1:
        if st.button("🗃️ Database Reader", use_container_width=True):
            st.info("Database Reader block selected")
        if st.button("📄 CSV Reader", use_container_width=True):
            st.info("CSV Reader block selected")
        if st.button("🌐 API Reader", use_container_width=True):
            st.info("API Reader block selected")

    with ingestion_col2:
        if st.button("📊 Streaming Reader", use_container_width=True):
            st.info("Streaming Reader block selected")
        if st.button("📋 Excel Reader", use_container_width=True):
            st.info("Excel Reader block selected")
        if st.button("🗂️ File System Reader", use_container_width=True):
            st.info("File System Reader block selected")

    st.markdown("---")

    # Storage Blocks
    st.markdown("#### 💾 Storage Blocks")
    storage_col1, storage_col2 = st.columns(2)

    with storage_col1:
        if st.button("🗃️ Database Writer", use_container_width=True):
            st.info("Database Writer block selected")
        if st.button("📄 CSV Writer", use_container_width=True):
            st.info("CSV Writer block selected")
        if st.button("📊 Data Lake Writer", use_container_width=True):
            st.info("Data Lake Writer block selected")

    with storage_col2:
        if st.button("💾 Cache Writer", use_container_width=True):
            st.info("Cache Writer block selected")
        if st.button("📋 Excel Writer", use_container_width=True):
            st.info("Excel Writer block selected")
        if st.button("🗂️ File System Writer", use_container_width=True):
            st.info("File System Writer block selected")

    st.markdown("---")

    # Transform Blocks
    st.markdown("#### 🔄 Transform Blocks")
    transform_col1, transform_col2 = st.columns(2)

    with transform_col1:
        if st.button("🔍 Filter", use_container_width=True):
            st.info("Filter block selected")
        if st.button("🔀 Join", use_container_width=True):
            st.info("Join block selected")
        if st.button("📈 Aggregate", use_container_width=True):
            st.info("Aggregate block selected")
        if st.button("➕ Union", use_container_width=True):
            st.info("Union block selected")

    with transform_col2:
        if st.button("🏷️ Rename Columns", use_container_width=True):
            st.info("Rename Columns block selected")
        if st.button("➗ Split", use_container_width=True):
            st.info("Split block selected")
        if st.button("🔢 Type Converter", use_container_width=True):
            st.info("Type Converter block selected")
        if st.button("🧹 Data Cleaner", use_container_width=True):
            st.info("Data Cleaner block selected")

    st.markdown("---")

    # Orchestration Blocks
    st.markdown("#### 🎯 Orchestration Blocks")
    orchestration_col1, orchestration_col2 = st.columns(2)

    with orchestration_col1:
        if st.button("⏰ Scheduler", use_container_width=True):
            st.info("Scheduler block selected")
        if st.button("🔄 Loop", use_container_width=True):
            st.info("Loop block selected")
        if st.button("🔀 Conditional", use_container_width=True):
            st.info("Conditional block selected")

    with orchestration_col2:
        if st.button("📊 Branch", use_container_width=True):
            st.info("Branch block selected")
        if st.button("🔔 Trigger", use_container_width=True):
            st.info("Trigger block selected")
        if st.button("⚡ Parallel", use_container_width=True):
            st.info("Parallel block selected")