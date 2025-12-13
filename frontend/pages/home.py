import streamlit as st


def render_home():
    """Render the home page content."""
    st.title("ETL Builder Tycoon")

    st.markdown("### Welcome to the ultimate ETL pipeline simulation game!")

    st.markdown("""
    Ever wondered what it's like to run your own data pipeline empire?
    Build, optimize, and scale ETL pipelines while managing clients, budgets, and tech debt.

    Choose an option from the sidebar to get started building your data empire!
    """)

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
