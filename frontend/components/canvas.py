import streamlit as st


class Canvas:
    """ETL Pipeline Canvas for building data pipelines."""

    def __init__(self):
        """Initialize the canvas with session state for block management."""
        # Initialize session state for canvas blocks if not exists
        if 'canvas_blocks' not in st.session_state:
            st.session_state.canvas_blocks = []

        if 'selected_block' not in st.session_state:
            st.session_state.selected_block = None

        if 'connections' not in st.session_state:
            st.session_state.connections = []

        if 'next_block_id' not in st.session_state:
            st.session_state.next_block_id = 1

    def add_block(self, block_type, x=100, y=100, width=120, height=80):
        """Add a new block to the canvas with specified geometry."""
        block_id = st.session_state.next_block_id
        st.session_state.next_block_id += 1

        new_block = {
            'id': block_id,
            'type': block_type,
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'selected': False
        }

        st.session_state.canvas_blocks.append(new_block)
        return block_id

    def remove_block(self, block_id):
        """Remove a block from the canvas by its ID."""
        st.session_state.canvas_blocks = [
            block for block in st.session_state.canvas_blocks
            if block['id'] != block_id
        ]

        # Also remove any connections involving this block
        st.session_state.connections = [
            conn for conn in st.session_state.connections
            if conn['from_block'] != block_id and conn['to_block'] != block_id
        ]

    def move_block(self, block_id, new_position):
        """Move a block to a new position on the canvas."""
        for block in st.session_state.canvas_blocks:
            if block['id'] == block_id:
                block['x'] = new_position.get('x', block['x'])
                block['y'] = new_position.get('y', block['y'])
                break

    def render(self):
        """Render the canvas placeholder with current blocks."""
        st.markdown("### 🎨 Pipeline Canvas")
        st.markdown("---")

        # Canvas placeholder
        with st.container():
            canvas_placeholder = st.empty()
            with canvas_placeholder.container():
                st.markdown("""
                <div style="
                    border: 2px dashed #4CAF50;
                    border-radius: 10px;
                    padding: 40px;
                    text-align: center;
                    background-color: #f8f9fa;
                    min-height: 400px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                ">
                    <h3 style="color: #4CAF50; margin-bottom: 20px;">🎯 Drag & Drop ETL Blocks Here</h3>
                    <p style="color: #666; font-size: 16px; margin-bottom: 20px;">
                        Build your data pipeline by dragging blocks from the library on the left
                    </p>
                    <div style="font-size: 48px;">📊 ➜ 🔄 ➜ 📤</div>
                    <p style="color: #888; margin-top: 20px;">
                        Canvas implementation coming soon...
                    </p>
                </div>
                """, unsafe_allow_html=True)

        # Display current blocks on canvas
        if st.session_state.canvas_blocks:
            st.markdown("---")
            st.markdown("#### 📋 Blocks on Canvas:")

            # Show blocks in a grid format
            cols = st.columns(3)
            for i, block in enumerate(st.session_state.canvas_blocks):
                col_idx = i % 3
                with cols[col_idx]:
                    with st.container():
                        st.markdown(f"**{block['type']}** (ID: {block['id']})")
                        st.caption(f"📍 Position: ({block['x']}, {block['y']})")
                        st.caption(f"📐 Size: {block['width']}×{block['height']}")

                        # Block controls
                        control_cols = st.columns(2)
                        with control_cols[0]:
                            if st.button(f"✏️ Edit", key=f"edit_{block['id']}", use_container_width=True):
                                st.session_state.selected_block = block['id']
                                st.info(f"Selected block {block['id']} for editing")
                        with control_cols[1]:
                            if st.button(f"🗑️ Remove", key=f"remove_{block['id']}", use_container_width=True):
                                self.remove_block(block['id'])
                                st.success(f"Removed block {block['id']}")
                                st.rerun()
        else:
            st.caption("No blocks on canvas yet. Select blocks from the library to get started!")

        # Pipeline controls
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("▶️ Run Pipeline", use_container_width=True):
                if not st.session_state.canvas_blocks:
                    st.warning("Add some blocks to the canvas first!")
                else:
                    st.success("Pipeline executed successfully!")
        with col2:
            if st.button("⏹️ Stop", use_container_width=True):
                st.info("Pipeline stopped")
        with col3:
            if st.button("💾 Save", use_container_width=True):
                if not st.session_state.canvas_blocks:
                    st.warning("Nothing to save!")
                else:
                    st.info("Pipeline saved")
        with col4:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.canvas_blocks = []
                st.session_state.connections = []
                st.success("Canvas cleared")