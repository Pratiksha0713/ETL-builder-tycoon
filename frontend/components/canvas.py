import streamlit as st
import uuid


class Canvas:
    """Interactive canvas for building ETL pipelines with drag-and-drop blocks."""

    def __init__(self):
        """Initialize the canvas with empty state."""
        if 'canvas_blocks' not in st.session_state:
            st.session_state.canvas_blocks = {}
        if 'canvas_connections' not in st.session_state:
            st.session_state.canvas_connections = {}  # Adjacency list: source_id -> [target_ids]
        if 'selected_block_id' not in st.session_state:
            st.session_state.selected_block_id = None

        self.blocks = st.session_state.canvas_blocks
        self.connections = st.session_state.canvas_connections
        self.selected_block_id = st.session_state.selected_block_id

    def add_block(self, block_type):
        """Add a new block to the canvas.

        Args:
            block_type (str): Type of block to add

        Returns:
            str: Unique ID of the added block
        """
        block_id = str(uuid.uuid4())
        self.blocks[block_id] = {
            'type': block_type,
            'id': block_id,
            'position': {'x': 100, 'y': 100},  # Default position
            'config': {}  # Block-specific configuration
        }
        self.connections[block_id] = []  # Initialize empty connections list
        return block_id

    def connect_block(self, source_id, target_id):
        """Connect two blocks in the pipeline.

        Args:
            source_id (str): ID of the source block
            target_id (str): ID of the target block

        Returns:
            bool: True if connection was successful, False otherwise
        """
        if source_id not in self.blocks or target_id not in self.blocks:
            st.error("Invalid block IDs for connection")
            return False

        if source_id == target_id:
            st.error("Cannot connect block to itself")
            return False

        # Prevent duplicate connections
        if target_id in self.connections[source_id]:
            st.warning("Connection already exists")
            return False

        # Add the connection
        self.connections[source_id].append(target_id)
        st.success(f"Connected {self.blocks[source_id]['type']} to {self.blocks[target_id]['type']}")
        return True

    def select_block(self, block_id):
        """Select a block on the canvas.

        Args:
            block_id (str): ID of the block to select
        """
        if block_id in self.blocks:
            self.selected_block_id = block_id
            st.session_state.selected_block_id = block_id
        else:
            self.selected_block_id = None
            st.session_state.selected_block_id = None

    def get_selected_block(self):
        """Get the currently selected block.

        Returns:
            dict or None: Selected block data or None if no selection
        """
        if self.selected_block_id and self.selected_block_id in self.blocks:
            return self.blocks[self.selected_block_id]
        return None

    def render(self):
        """Render the canvas with blocks and connections."""
        st.markdown("### 🖼️ Pipeline Canvas")
        st.markdown("---")

        # Canvas area
        canvas_container = st.container()

        with canvas_container:
            # Display current blocks
            if not self.blocks:
                st.info("🖼️ Canvas is empty. Add blocks from the library to start building your pipeline!")
            else:
                # Show blocks in a grid layout for now (can be improved with drag-and-drop later)
                cols = st.columns(3)
                for i, (block_id, block) in enumerate(self.blocks.items()):
                    col_idx = i % 3
                    with cols[col_idx]:
                        # Block container
                        selected = self.selected_block_id == block_id
                        border_color = "#007bff" if selected else "#dee2e6"

                        st.markdown(f"""
                        <div style="
                            border: 2px solid {border_color};
                            border-radius: 8px;
                            padding: 10px;
                            margin: 5px 0;
                            background-color: {'#f8f9ff' if selected else '#ffffff'};
                            cursor: pointer;
                        ">
                            <strong>{block['type']}</strong><br>
                            <small style="color: #6c757d;">ID: {block_id[:8]}...</small>
                        </div>
                        """, unsafe_allow_html=True)

                        # Selection button
                        if st.button(f"Select {block['type']}", key=f"select_{block_id}", use_container_width=True):
                            self.select_block(block_id)

                        # Connection section (only show if a block is selected and it's not the current block)
                        if self.selected_block_id and self.selected_block_id != block_id:
                            if st.button(f"🔗 Connect from selected", key=f"connect_{block_id}", use_container_width=True):
                                self.connect_block(self.selected_block_id, block_id)

                # Display connections
                if any(self.connections.values()):
                    st.markdown("---")
                    st.markdown("### 🔗 Pipeline Connections")

                    for source_id, targets in self.connections.items():
                        if targets:
                            source_type = self.blocks[source_id]['type']
                            st.markdown(f"**{source_type}** ({source_id[:8]}...) →")
                            for target_id in targets:
                                target_type = self.blocks[target_id]['type']
                                st.markdown(f"  └─ **{target_type}** ({target_id[:8]}...)")

                # Clear selection button
                if self.selected_block_id:
                    st.markdown("---")
                    if st.button("❌ Clear Selection", use_container_width=True):
                        self.select_block(None)
                        st.rerun()

        # Update session state
        st.session_state.canvas_blocks = self.blocks
        st.session_state.canvas_connections = self.connections
        st.session_state.selected_block_id = self.selected_block_id