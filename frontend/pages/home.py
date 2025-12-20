import streamlit as st


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
    st.markdown("---")
    st.markdown("### 🎯 Quick Start Options")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🎮 Start Playing", use_container_width=True):
            st.session_state.page = "game"
        st.caption("⚡ Jump right into the action!")
        st.markdown("Begin your ETL empire journey immediately.")

    with col2:
        if st.button("📚 Learn Basics", use_container_width=True):
            st.session_state.page = "tutorial"
        st.caption("🎓 Master the fundamentals")
        st.markdown("Learn ETL concepts and game mechanics before playing.")

    with col3:
        if st.button("🏆 View Leaderboard", use_container_width=True):
            st.session_state.page = "leaderboard"
        st.caption("🌟 See who's on top")
        st.markdown("Check out the highest-scoring data pipeline tycoons.")
