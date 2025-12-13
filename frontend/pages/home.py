import streamlit as st


def render_home():
    """Render the home page content."""
    st.title("🏭 ETL Builder Tycoon")

    st.markdown("### 🎮 Welcome to the ultimate ETL pipeline simulation game!")

    st.markdown("""
    🚀 **Ever wondered what it's like to run your own data pipeline empire?**

    🏗️ **Build, optimize, and scale ETL pipelines** while managing clients, budgets, and tech debt.
    Experience the thrill of data engineering without the midnight alerts!

    📊 **Features:**
    - Drag-and-drop pipeline builder with real-time data flow visualization
    - Multiple data source types: APIs, databases, flat files, streaming sources
    - Performance metrics that actually matter (throughput, latency, error rates)
    - Business simulation with client contracts and resource management

    💡 **Think Factorio meets data engineering nightmares!** Start with a tiny data warehouse
    and build the most efficient data pipelines in the industry.

    ⚠️ *Your servers might catch fire (metaphorically... mostly).*
    """)

    # Start Game button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 Start Game", use_container_width=True, type="primary"):
            st.success("🚧 Game interface coming soon! 🚧")
            st.info("The main game will be implemented here with pipeline building, metrics dashboard, and business simulation.")

    # Quick start section
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🎮 Start Playing", use_container_width=True):
            st.session_state.page = "game"
        st.caption("Jump right into the game")

    with col2:
        if st.button("📚 Learn Basics", use_container_width=True):
            st.session_state.page = "tutorial"
        st.caption("Read the tutorial first")

    with col3:
        if st.button("🏆 View Leaderboard", use_container_width=True):
            st.session_state.page = "leaderboard"
        st.caption("See top players")
