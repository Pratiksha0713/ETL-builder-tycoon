import streamlit as st


def render_game():
    """Render the main game page with ETL pipeline builder."""
    st.title("🎮 ETL Builder Tycoon - Game")

    # Create three-column layout
    left_col, center_col, right_col = st.columns([2, 4, 2])

    # Left Column: Block Library
    with left_col:
        st.markdown("### 🧱 Block Library")
        st.markdown("---")

        # Data Sources
        st.markdown("#### 📥 Data Sources")
        if st.button("🗃️ Database", use_container_width=True):
            st.info("Database block selected")
        if st.button("📄 CSV File", use_container_width=True):
            st.info("CSV File block selected")
        if st.button("🌐 API", use_container_width=True):
            st.info("API block selected")
        if st.button("📊 Streaming", use_container_width=True):
            st.info("Streaming block selected")

        st.markdown("---")

        # Transformations
        st.markdown("#### 🔄 Transformations")
        if st.button("🔍 Filter", use_container_width=True):
            st.info("Filter block selected")
        if st.button("🔀 Join", use_container_width=True):
            st.info("Join block selected")
        if st.button("📈 Aggregate", use_container_width=True):
            st.info("Aggregate block selected")
        if st.button("🏷️ Rename", use_container_width=True):
            st.info("Rename block selected")
        if st.button("➗ Split", use_container_width=True):
            st.info("Split block selected")

        st.markdown("---")

        # Outputs
        st.markdown("#### 📤 Outputs")
        if st.button("💾 Database", use_container_width=True):
            st.info("Output Database block selected")
        if st.button("📋 CSV Export", use_container_width=True):
            st.info("CSV Export block selected")
        if st.button("📊 Dashboard", use_container_width=True):
            st.info("Dashboard block selected")

    # Center Column: Canvas Placeholder
    with center_col:
        st.markdown("### 🎨 Pipeline Canvas")
        st.markdown("---")

        # Canvas placeholder
        with st.container():
            canvas_placeholder = st.empty()
            with canvas_placeholder.container():
                st.markdown("""
                <div style="
                    border: 2px dashed #4CAF50;
                    border-radius: 10px;
                    padding: 40px;
                    text-align: center;
                    background-color: #f8f9fa;
                    min-height: 400px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                ">
                    <h3 style="color: #4CAF50; margin-bottom: 20px;">🎯 Drag & Drop ETL Blocks Here</h3>
                    <p style="color: #666; font-size: 16px; margin-bottom: 20px;">
                        Build your data pipeline by dragging blocks from the library on the left
                    </p>
                    <div style="font-size: 48px;">📊 ➜ 🔄 ➜ 📤</div>
                    <p style="color: #888; margin-top: 20px;">
                        Canvas implementation coming soon...
                    </p>
                </div>
                """, unsafe_allow_html=True)

        # Pipeline controls
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("▶️ Run Pipeline", use_container_width=True):
                st.success("Pipeline executed successfully!")
        with col2:
            if st.button("⏹️ Stop", use_container_width=True):
                st.info("Pipeline stopped")
        with col3:
            if st.button("💾 Save", use_container_width=True):
                st.info("Pipeline saved")
        with col4:
            if st.button("🗑️ Clear", use_container_width=True):
                st.warning("Canvas cleared")

    # Right Column: Metrics Panel + Event Log
    with right_col:
        # Metrics Panel
        with st.container():
            st.markdown("### 📊 Metrics Panel")
            st.markdown("---")

            # Key Metrics
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.metric("💰 Budget", "$50,000", "+$2,500")
                st.metric("👥 Team Size", "5", "+1")
            with metric_col2:
                st.metric("⚡ Throughput", "1.2M rows/s", "+15%")
                st.metric("🎯 Success Rate", "98.5%", "+0.3%")

            st.markdown("---")

            # Performance Metrics
            st.markdown("#### 🚀 Performance")
            progress_bar = st.progress(0.75)
            st.caption("Pipeline Efficiency: 75%")

            st.markdown("#### 💡 Quality Score")
            quality_bar = st.progress(0.92)
            st.caption("Data Quality: 92%")

        st.markdown("---")

        # Event Log
        with st.container():
            st.markdown("### 📋 Event Log")
            st.markdown("---")

            event_log = st.empty()
            with event_log.container():
                st.markdown("""
                <div style="
                    background-color: #f8f9fa;
                    border-radius: 5px;
                    padding: 10px;
                    max-height: 300px;
                    overflow-y: auto;
                    font-family: monospace;
                    font-size: 12px;
                ">
                    <div style="color: #28a745;">[10:30:15] ✓ Pipeline started successfully</div>
                    <div style="color: #007bff;">[10:30:16] ℹ Processing 1.2M records from database</div>
                    <div style="color: #ffc107;">[10:30:18] ⚠ High memory usage detected</div>
                    <div style="color: #28a745;">[10:30:20] ✓ Filter transformation completed</div>
                    <div style="color: #28a745;">[10:30:22] ✓ Join operation successful</div>
                    <div style="color: #007bff;">[10:30:25] ℹ Exporting to data warehouse</div>
                    <div style="color: #28a745;">[10:30:28] ✓ Pipeline completed in 13 seconds</div>
                    <div style="color: #28a745;">[10:30:28] 💰 Revenue: +$1,250</div>
                </div>
                """, unsafe_allow_html=True)

        # Quick Actions
        st.markdown("---")
        st.markdown("#### ⚡ Quick Actions")
        if st.button("🔧 Optimize Pipeline", use_container_width=True):
            st.info("Optimization suggestions generated")
        if st.button("👥 Hire Engineer", use_container_width=True):
            st.info("Engineer recruitment initiated")
        if st.button("💻 Upgrade Infrastructure", use_container_width=True):
            st.info("Infrastructure upgrade options shown")