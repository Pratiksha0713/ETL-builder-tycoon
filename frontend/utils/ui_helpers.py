"""
UI Helper Functions - Common Streamlit UI patterns and utilities.
"""

import streamlit as st
from typing import Optional


def create_block_button(
    canvas,
    button_label: str,
    block_name: str,
    help_text: str,
    use_container_width: bool = True
) -> Optional[str]:
    """
    Create a button that adds a block to the canvas when clicked.
    
    Args:
        canvas: Canvas instance with add_block method
        button_label: Text to display on the button
        block_name: Name of the block to add
        help_text: Tooltip text for the button
        use_container_width: Whether button should use full container width
        
    Returns:
        Block ID if button was clicked, None otherwise
    """
    if st.button(button_label, use_container_width=use_container_width, help=help_text):
        block_id = canvas.add_block(block_name)
        st.success(f"Added {block_name} block (ID: {block_id}) to canvas")
        return block_id
    return None


def render_block_category(
    canvas,
    category_title: str,
    blocks: list[tuple[str, str, str]],
    num_columns: int = 2
) -> None:
    """
    Render a category of blocks with buttons.
    
    Args:
        canvas: Canvas instance
        category_title: Title for the category section
        blocks: List of tuples (button_label, block_name, help_text)
        num_columns: Number of columns to use for layout
    """
    st.markdown(f"#### {category_title}")
    columns = st.columns(num_columns)
    
    for idx, (button_label, block_name, help_text) in enumerate(blocks):
        col = columns[idx % num_columns]
        with col:
            create_block_button(canvas, button_label, block_name, help_text)


def render_navigation_sidebar(
    navigation_items: list[tuple[str, str]],
    app_title: str = "ETL Builder Tycoon 🏭"
) -> None:
    """
    Render the navigation sidebar with buttons.
    
    Args:
        navigation_items: List of tuples (button_label, page_name)
        app_title: Title to display in sidebar
    """
    st.sidebar.title(app_title)
    st.sidebar.markdown("---")
    
    for button_label, page_name in navigation_items:
        if st.sidebar.button(button_label, use_container_width=True):
            st.session_state.page = page_name
    
    st.sidebar.markdown("---")


def render_page_section(
    title: str,
    info_message: Optional[str] = None,
    content: Optional[str] = None
) -> None:
    """
    Render a standard page section with title, optional info, and content.
    
    Args:
        title: Page title
        info_message: Optional info message to display
        content: Optional markdown content
    """
    st.title(title)
    
    if info_message:
        st.info(info_message)
    
    if content:
        st.markdown(content)


def create_action_button_group(
    buttons: list[tuple[str, str, str, Optional[str]]],
    num_columns: int = 3
) -> None:
    """
    Create a group of action buttons with captions and descriptions.
    
    Args:
        buttons: List of tuples (button_label, page_name, caption, description)
        num_columns: Number of columns for layout
    """
    columns = st.columns(num_columns)
    
    for idx, (button_label, page_name, caption, description) in enumerate(buttons):
        col = columns[idx % num_columns]
        with col:
            if st.button(button_label, use_container_width=True):
                st.session_state.page = page_name
            if caption:
                st.caption(caption)
            if description:
                st.markdown(description)


def render_section_divider() -> None:
    """Render a standard section divider."""
    st.markdown("---")

