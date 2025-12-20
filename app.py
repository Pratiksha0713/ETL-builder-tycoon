"""
ETL Builder Tycoon - Main Application Entry Point
"""

import streamlit as st
from frontend.utils.ui_helpers import render_navigation_sidebar, render_page_section, render_section_divider

# Page configuration
st.set_page_config(
    page_title="ETL Builder Tycoon",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Navigation configuration
NAVIGATION_ITEMS = [
    ("🏠 Home", "home"),
    ("🎮 Game", "game"),
    ("📚 Tutorial", "tutorial"),
    ("🏆 Leaderboard", "leaderboard"),
]

# Page content configuration
PAGE_CONTENT = {
    "home": {
        "title": "Welcome to ETL Builder Tycoon!",
        "info": None,
        "content": """
        Build and manage the most efficient ETL pipelines in the industry!

        ### Features:
        - **Drag & Drop Pipeline Builder**: Create complex data workflows visually
        - **Real-time Performance Metrics**: Monitor throughput, latency, and costs
        - **Business Simulation**: Manage clients, budgets, and tech debt
        - **Multiple Data Sources**: Handle APIs, databases, streaming data, and files

        Choose an option from the sidebar to get started!
        """
    },
    "game": {
        "title": "🎮 Game",
        "info": "🚧 Game interface coming soon! 🚧",
        "content": """
        This is where the main game will be implemented:
        - Pipeline builder canvas
        - Node palette
        - Real-time metrics dashboard
        - Resource management
        """
    },
    "tutorial": {
        "title": "📚 Tutorial",
        "info": "🚧 Tutorial content coming soon! 🚧",
        "content": """
        Learn how to:
        - Build your first ETL pipeline
        - Optimize for performance and cost
        - Manage data sources and destinations
        - Handle production challenges
        """
    },
    "leaderboard": {
        "title": "🏆 Leaderboard",
        "info": "🚧 Leaderboard coming soon! 🚧",
        "content": """
        Compete with other players:
        - Top pipeline efficiency scores
        - Most profitable companies
        - Longest uptime records
        - Innovation achievements
        """
    },
}

# Render navigation sidebar
render_navigation_sidebar(NAVIGATION_ITEMS)

# Main content area with routing
current_page = st.session_state.page
page_config = PAGE_CONTENT.get(current_page, PAGE_CONTENT["home"])

render_page_section(
    title=page_config["title"],
    info_message=page_config["info"],
    content=page_config["content"]
)

# Footer
render_section_divider()
st.markdown("*Your data. Your pipelines. Your empire.*")
