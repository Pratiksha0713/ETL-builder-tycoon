"""
Canvas component for pipeline visualization and interaction.
"""

import streamlit as st
from typing import Optional


class Canvas:
    """
    Canvas for displaying and managing pipeline blocks.
    
    Provides methods for adding, removing, and connecting blocks.
    """
    
    def __init__(self):
        """Initialize the canvas."""
        if "canvas_blocks" not in st.session_state:
            st.session_state.canvas_blocks = []
        if "canvas_block_counter" not in st.session_state:
            st.session_state.canvas_block_counter = 0
    
    def add_block(self, block_name: str) -> str:
        """
        Add a block to the canvas.
        
        Args:
            block_name: Name of the block to add.
            
        Returns:
            Unique block ID.
        """
        block_id = f"block_{st.session_state.canvas_block_counter}"
        st.session_state.canvas_block_counter += 1
        
        block = {
            "id": block_id,
            "name": block_name,
            "position": (0, 0),
        }
        
        st.session_state.canvas_blocks.append(block)
        return block_id
    
    def remove_block(self, block_id: str) -> bool:
        """
        Remove a block from the canvas.
        
        Args:
            block_id: ID of the block to remove.
            
        Returns:
            True if block was removed, False if not found.
        """
        blocks = st.session_state.canvas_blocks
        for i, block in enumerate(blocks):
            if block["id"] == block_id:
                blocks.pop(i)
                return True
        return False
    
    def get_blocks(self) -> list[dict]:
        """
        Get all blocks on the canvas.
        
        Returns:
            List of block dictionaries.
        """
        return st.session_state.canvas_blocks.copy()
    
    def clear(self) -> None:
        """Clear all blocks from the canvas."""
        st.session_state.canvas_blocks = []
        st.session_state.canvas_block_counter = 0
