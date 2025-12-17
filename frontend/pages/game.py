import streamlit as st
import yaml
from pathlib import Path


def load_level_config(level: str) -> dict:
    """
    Load level configuration from YAML file.
    
    Args:
        level: Level name (e.g., 'level1', 'level2', 'level3')
        
    Returns:
        Dictionary containing level configuration
    """
    # Get the project root directory (go up from frontend/pages/)
    project_root = Path(__file__).parent.parent.parent
    level_file = project_root / "data" / "levels" / f"{level}.yaml"
    
    try:
        with open(level_file, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        st.error(f"Level file not found: {level_file}")
        return {}
    except yaml.YAMLError as e:
        st.error(f"Error parsing YAML file: {e}")
        return {}


def render_game():
    """Render the game page with level selection."""
    st.title("🎮 Game")
    
    # Level selection
    st.markdown("### 📋 Level Selection")
    level_options = ["level1", "level2", "level3"]
    selected_level = st.selectbox(
        "Choose a level:",
        options=level_options,
        index=0,
        help="Select the difficulty level for your ETL pipeline challenge"
    )
    
    # Load level configuration
    level_config = load_level_config(selected_level)
    
    # Display level configuration
    if level_config:
        st.markdown("---")
        st.markdown("### 📊 Level Requirements")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Target Blocks",
                level_config.get("target_blocks", "N/A")
            )
        
        with col2:
            max_latency = level_config.get("max_latency", 0)
            st.metric(
                "Max Latency",
                f"{max_latency:.0f} ms"
            )
        
        with col3:
            min_throughput = level_config.get("min_throughput", 0)
            st.metric(
                "Min Throughput",
                f"{min_throughput:.0f} rps"
            )
        
        with col4:
            max_cost = level_config.get("max_cost", 0)
            st.metric(
                "Max Cost",
                f"{max_cost:.1f} units"
            )
        
        # Store level config in session state for use in game logic
        st.session_state.current_level = selected_level
        st.session_state.level_config = level_config
    
    st.markdown("---")
    st.info("🚧 Game interface coming soon! 🚧")
    st.markdown("""
    This is where the main game will be implemented:
    - Pipeline builder canvas
    - Node palette
    - Real-time metrics dashboard
    - Resource management
    """)
