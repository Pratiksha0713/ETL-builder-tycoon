"""
Home Page Component - Enhanced home page with action buttons.
"""

import streamlit as st
from frontend.utils.ui_helpers import create_action_button_group, render_section_divider


def render_home():
    """Render the home page content."""
    st.title("🚀 ETL Builder Tycoon")

    # Prominent Start Game button
    col_start, col_space = st.columns([1, 3])
    with col_start:
        if st.button("🎮 Start Game", use_container_width=True, type="primary"):
            st.info("🚧 Game functionality coming soon! 🚧")
    with col_space:
        st.markdown("### 🌟 Welcome to the ultimate ETL pipeline simulation game! 🌟")

    st.markdown("""
    🏭 **Ever wondered what it's like to run your own data pipeline empire?** 🏭

    💼 Build, optimize, and scale ETL pipelines while managing clients, budgets, and tech debt. 💼

    📊 Take on challenging projects, hire the right team, invest in infrastructure, and watch your data empire grow! 📊

    🎯 **Game Features:**
    - 🛠️ Design and build complex ETL pipelines
    - 👥 Manage a team of data engineers and analysts
    - 💰 Balance budgets and maximize profits
    - ⚡ Handle performance bottlenecks and scaling challenges
    - 🏆 Compete on global leaderboards

    Choose an option from the sidebar to get started building your data empire! 🚀
    """)

    # Quick start section
    render_section_divider()
    st.markdown("### 🎯 Quick Start Options")

    quick_start_buttons = [
        ("🎮 Start Playing", "game", "⚡ Jump right into the action!", 
         "Begin your ETL empire journey immediately."),
        ("📚 Learn Basics", "tutorial", "🎓 Master the fundamentals",
         "Learn ETL concepts and game mechanics before playing."),
        ("🏆 View Leaderboard", "leaderboard", "🌟 See who's on top",
         "Check out the highest-scoring data pipeline tycoons."),
    ]
    
    create_action_button_group(quick_start_buttons, num_columns=3)
