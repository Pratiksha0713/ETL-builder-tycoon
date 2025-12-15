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
        """Render the canvas with blocks and connections in a visual grid layout."""
        st.markdown("### 🖼️ Pipeline Canvas")
        st.markdown("---")

        # Canvas area
        canvas_container = st.container()

        with canvas_container:
            # Display current blocks
            if not self.blocks:
                st.info("🖼️ Canvas is empty. Add blocks from the library to start building your pipeline!")
            else:
                # Create visual grid representation
                self._render_visual_grid()

                # Control buttons below the grid
                st.markdown("---")
                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("🔄 Refresh Canvas", use_container_width=True):
                        st.rerun()

                with col2:
                    if self.selected_block_id:
                        if st.button("❌ Clear Selection", use_container_width=True):
                            self.select_block(None)
                            st.rerun()

                with col3:
                    if st.button("🗑️ Clear All", use_container_width=True):
                        self.blocks.clear()
                        self.connections.clear()
                        self.select_block(None)
                        st.rerun()

        # Update session state
        st.session_state.canvas_blocks = self.blocks
        st.session_state.canvas_connections = self.connections
        st.session_state.selected_block_id = self.selected_block_id

    def _render_visual_grid(self):
        """Render blocks in a visual grid layout with connections."""
        # Create a 4x4 grid (can be made dynamic later)
        grid_size = 4
        grid = [['   ' for _ in range(grid_size)] for _ in range(grid_size)]

        # Block type abbreviations for display
        type_abbr = {
            'Database Reader': 'DB_R',
            'CSV Reader': 'CSV_R',
            'API Reader': 'API_R',
            'Streaming Reader': 'STR_R',
            'Excel Reader': 'XLS_R',
            'File System Reader': 'FS_R',
            'Database Writer': 'DB_W',
            'CSV Writer': 'CSV_W',
            'Data Lake Writer': 'DL_W',
            'Cache Writer': 'CACHE',
            'Excel Writer': 'XLS_W',
            'File System Writer': 'FS_W',
            'Filter': 'FLTR',
            'Join': 'JOIN',
            'Aggregate': 'AGG',
            'Union': 'UNION',
            'Rename Columns': 'RENAME',
            'Split': 'SPLIT',
            'Type Converter': 'CONV',
            'Data Cleaner': 'CLEAN',
            'Scheduler': 'SCHED',
            'Loop': 'LOOP',
            'Conditional': 'COND',
            'Branch': 'BRANCH',
            'Trigger': 'TRIG',
            'Parallel': 'PARAL'
        }

        # Place blocks in grid positions
        block_positions = {}
        block_list = list(self.blocks.items())

        for idx, (block_id, block) in enumerate(block_list):
            row = idx // grid_size
            col = idx % grid_size
            if row < grid_size and col < grid_size:
                abbr = type_abbr.get(block['type'], block['type'][:5])
                selected = self.selected_block_id == block_id
                if selected:
                    grid[row][col] = f'[{abbr}]'
                else:
                    grid[row][col] = f' {abbr} '
                block_positions[block_id] = (row, col)

        # Draw connections
        for source_id, targets in self.connections.items():
            if source_id in block_positions and targets:
                source_pos = block_positions[source_id]
                for target_id in targets:
                    if target_id in block_positions:
                        target_pos = block_positions[target_id]
                        self._draw_connection(grid, source_pos, target_pos)

        # Render the grid
        grid_lines = []
        grid_lines.append("```")
        grid_lines.append("┌───┬───┬───┬───┐")

        for i, row in enumerate(grid):
            row_str = "│" + "│".join(cell.center(3) for cell in row) + "│"
            grid_lines.append(row_str)
            if i < len(grid) - 1:
                grid_lines.append("├───┼───┼───┼───┤")
            else:
                grid_lines.append("└───┴───┴───┴───┘")

        grid_lines.append("```")
        st.markdown("\n".join(grid_lines))

        # Block interaction buttons
        st.markdown("### 🎛️ Block Controls")
        cols = st.columns(min(4, len(self.blocks)))
        for i, (block_id, block) in enumerate(self.blocks.items()):
            with cols[i % len(cols)]:
                selected = self.selected_block_id == block_id
                button_label = f"{'✓' if selected else ''} {block['type']}"
                if st.button(button_label, key=f"select_{block_id}", use_container_width=True):
                    self.select_block(block_id)

                # Connection buttons (only show if a block is selected and it's not the current block)
                if self.selected_block_id and self.selected_block_id != block_id:
                    if st.button(f"🔗 Connect", key=f"connect_{block_id}", use_container_width=True):
                        self.connect_block(self.selected_block_id, block_id)

        # Connection details
        if any(self.connections.values()):
            st.markdown("### 🔗 Active Connections")
            for source_id, targets in self.connections.items():
                if targets:
                    source_type = self.blocks[source_id]['type']
                    st.markdown(f"**{source_type}** → {len(targets)} connection{'s' if len(targets) > 1 else ''}")

    def _draw_connection(self, grid, source_pos, target_pos):
        """Draw a connection line between two positions in the grid."""
        source_row, source_col = source_pos
        target_row, target_col = target_pos

        # Simple connection: just mark target with arrow if it's right/down
        if target_col > source_col:  # right connection
            if grid[target_row][target_col].strip():
                grid[target_row][target_col] = grid[target_row][target_col].replace(' ', '→')
        elif target_row > source_row:  # down connection
            if grid[target_row][target_col].strip():
                grid[target_row][target_col] = grid[target_row][target_col].replace(' ', '↓')