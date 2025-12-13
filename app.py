import streamlit as st

# Page configuration
st.set_page_config(
    page_title="ETL Builder Tycoon",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
st.sidebar.title("ETL Builder Tycoon 🏭")
st.sidebar.markdown("---")

# Navigation buttons
if st.sidebar.button("🏠 Home", use_container_width=True):
    st.session_state.page = "home"

if st.sidebar.button("🎮 Game", use_container_width=True):
    st.session_state.page = "game"

if st.sidebar.button("📚 Tutorial", use_container_width=True):
    st.session_state.page = "tutorial"

if st.sidebar.button("🏆 Leaderboard", use_container_width=True):
    st.session_state.page = "leaderboard"

st.sidebar.markdown("---")

# Main content area with routing placeholders
current_page = st.session_state.get("page", "home")

if current_page == "home":
    st.title("Welcome to ETL Builder Tycoon!")
    st.markdown("""
    Build and manage the most efficient ETL pipelines in the industry!

    ### Features:
    - **Drag & Drop Pipeline Builder**: Create complex data workflows visually
    - **Real-time Performance Metrics**: Monitor throughput, latency, and costs
    - **Business Simulation**: Manage clients, budgets, and tech debt
    - **Multiple Data Sources**: Handle APIs, databases, streaming data, and files

    Choose an option from the sidebar to get started!
    """)

elif current_page == "game":
    st.title("🎮 Game")
    st.info("🚧 Game interface coming soon! 🚧")
    st.markdown("""
    This is where the main game will be implemented:
    - Pipeline builder canvas
    - Node palette
    - Real-time metrics dashboard
    - Resource management
    """)

elif current_page == "tutorial":
    st.title("📚 Tutorial")
    st.info("🚧 Tutorial content coming soon! 🚧")
    st.markdown("""
    Learn how to:
    - Build your first ETL pipeline
    - Optimize for performance and cost
    - Manage data sources and destinations
    - Handle production challenges
    """)

elif current_page == "leaderboard":
    st.title("🏆 Leaderboard")
    st.info("🚧 Leaderboard coming soon! 🚧")
    st.markdown("""
    Compete with other players:
    - Top pipeline efficiency scores
    - Most profitable companies
    - Longest uptime records
    - Innovation achievements
    """)

# Footer
st.markdown("---")
st.markdown("*Your data. Your pipelines. Your empire.*")
