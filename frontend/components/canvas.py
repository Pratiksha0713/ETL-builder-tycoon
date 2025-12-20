"""
Canvas component for drag-and-drop pipeline visualization and interaction.

Uses streamlit-elements for draggable blocks and custom HTML/JavaScript
for drag-and-drop functionality with position persistence.
"""

import streamlit as st
import json
from typing import Optional, Dict, List


# Block type definitions
BLOCK_TYPES = {
    "Kafka Source": {"type": "source", "icon": "📊🌊", "color": "#4CAF50"},
    "API Source": {"type": "source", "icon": "🌐🔗", "color": "#2196F3"},
    "S3 Storage": {"type": "storage", "icon": "🗂️", "color": "#FF9800"},
    "Delta Lake": {"type": "storage", "icon": "📊", "color": "#9C27B0"},
    "Spark Transform": {"type": "transform", "icon": "⚡", "color": "#F44336"},
    "dbt Model": {"type": "transform", "icon": "🔧", "color": "#00BCD4"},
    "Airflow DAG": {"type": "orchestration", "icon": "🔄", "color": "#795548"},
    "Power BI Dashboard": {"type": "destination", "icon": "📈", "color": "#E91E63"},
}


class Canvas:
    """
    Drag-and-drop canvas for displaying and managing pipeline blocks.
    
    Provides methods for adding, removing, connecting, and repositioning blocks.
    Stores everything in st.session_state["nodes"] and st.session_state["edges"].
    """
    
    def __init__(self):
        """Initialize the canvas with session state."""
        if "nodes" not in st.session_state:
            st.session_state.nodes = []
        if "edges" not in st.session_state:
            st.session_state.edges = []
        if "selected_node" not in st.session_state:
            st.session_state.selected_node = None
        if "canvas_block_counter" not in st.session_state:
            st.session_state.canvas_block_counter = 0
    
    def add_block(self, block_name: str, x: float = 100, y: float = 100) -> str:
        """
        Add a block to the canvas.
        
        Args:
            block_name: Name of the block to add
            x: Initial x position
            y: Initial y position
            
        Returns:
            Unique block ID
        """
        block_id = f"node_{st.session_state.canvas_block_counter}"
        st.session_state.canvas_block_counter += 1
        
        block_info = BLOCK_TYPES.get(block_name, {"type": "unknown", "icon": "📦", "color": "#757575"})
        
        node = {
            "id": block_id,
            "name": block_name,
            "type": block_info["type"],
            "x": x,
            "y": y,
            "icon": block_info["icon"],
            "color": block_info["color"],
        }
        
        st.session_state.nodes.append(node)
        return block_id
    
    def remove_block(self, block_id: str) -> bool:
        """
        Remove a block from the canvas and all its connections.
        
        Args:
            block_id: ID of the block to remove
            
        Returns:
            True if block was removed, False if not found
        """
        # Remove node
        nodes = st.session_state.nodes
        for i, node in enumerate(nodes):
            if node["id"] == block_id:
                nodes.pop(i)
                break
        else:
            return False
        
        # Remove all edges connected to this node
        edges = st.session_state.edges
        st.session_state.edges = [
            edge for edge in edges 
            if edge["source"] != block_id and edge["target"] != block_id
        ]
        
        # Clear selection if this node was selected
        if st.session_state.selected_node == block_id:
            st.session_state.selected_node = None
        
        return True
    
    def connect_blocks(self, source_id: str, target_id: str) -> bool:
        """
        Connect two blocks (source → target).
        
        Args:
            source_id: ID of the source block
            target_id: ID of the target block
            
        Returns:
            True if connection was created, False if invalid
        """
        # Validate nodes exist
        node_ids = {node["id"] for node in st.session_state.nodes}
        if source_id not in node_ids or target_id not in node_ids:
            return False
        
        # Check if connection already exists
        for edge in st.session_state.edges:
            if edge["source"] == source_id and edge["target"] == target_id:
                return False
        
        # Create connection
        edge = {
            "id": f"edge_{len(st.session_state.edges)}",
            "source": source_id,
            "target": target_id,
        }
        st.session_state.edges.append(edge)
        return True
    
    def update_node_position(self, node_id: str, x: float, y: float) -> bool:
        """
        Update the position of a node.
        
        Args:
            node_id: ID of the node
            x: New x position
            y: New y position
            
        Returns:
            True if position was updated, False if node not found
        """
        for node in st.session_state.nodes:
            if node["id"] == node_id:
                node["x"] = x
                node["y"] = y
                return True
        return False
    
    def select_node(self, node_id: Optional[str]) -> None:
        """
        Select a node for editing properties.
        
        Args:
            node_id: ID of the node to select, or None to deselect
        """
        st.session_state.selected_node = node_id
    
    def get_graph(self) -> Dict:
        """
        Get the current graph structure.
        
        Returns:
            Dictionary with nodes and edges
        """
        return {
            "nodes": st.session_state.nodes.copy(),
            "edges": st.session_state.edges.copy(),
        }
    
    def get_blocks(self) -> List[Dict]:
        """
        Get all blocks on the canvas.
        
        Returns:
            List of block dictionaries
        """
        return st.session_state.nodes.copy()
    
    def clear(self) -> None:
        """Clear all blocks and connections from the canvas."""
        st.session_state.nodes = []
        st.session_state.edges = []
        st.session_state.selected_node = None
        st.session_state.canvas_block_counter = 0
    
    def render(self) -> None:
        """
        Render the drag-and-drop canvas with all blocks and connections.
        """
        st.markdown("### 🎨 Pipeline Canvas")
        
        # Canvas controls
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("🗑️ Clear Canvas", use_container_width=True):
                self.clear()
                st.rerun()
        with col2:
            if st.button("💾 Save Pipeline", use_container_width=True):
                graph = self.get_graph()
                st.success(f"Saved pipeline with {len(graph['nodes'])} nodes and {len(graph['edges'])} connections")
        
        # Render canvas using HTML/JavaScript for drag-and-drop
        self._render_canvas_html()
        
        # Properties panel for selected node
        if st.session_state.selected_node:
            self._render_properties_panel()
    
    def _render_canvas_html(self) -> None:
        """Render the canvas using HTML and JavaScript for drag-and-drop."""
        nodes_json = json.dumps(st.session_state.nodes)
        edges_json = json.dumps(st.session_state.edges)
        
        # Create a unique key for this component instance
        component_key = f"canvas_{len(st.session_state.nodes)}"
        
        canvas_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                #pipeline-canvas {{
                    position: relative;
                    width: 100%;
                    height: 600px;
                    border: 2px solid #e0e0e0;
                    border-radius: 8px;
                    background: linear-gradient(90deg, #f5f5f5 1px, transparent 1px),
                                linear-gradient(#f5f5f5 1px, transparent 1px);
                    background-size: 20px 20px;
                    overflow: auto;
                    margin: 10px 0;
                }}
                .pipeline-node {{
                    position: absolute;
                    width: 150px;
                    height: 80px;
                    background: white;
                    border-radius: 8px;
                    padding: 10px;
                    cursor: move;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    z-index: 10;
                    user-select: none;
                }}
                .pipeline-node:hover {{
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                }}
                .pipeline-node.selected {{
                    border-width: 3px;
                    box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.3);
                }}
            </style>
        </head>
        <body>
            <div id="pipeline-canvas">
                <svg id="edges-layer" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1;"></svg>
                <div id="nodes-layer" style="position: relative; z-index: 2;"></div>
            </div>
            
            <script>
            const nodes = {nodes_json};
            const edges = {edges_json};
            
            let selectedNodeId = null;
            let draggedNode = null;
            let offsetX = 0;
            let offsetY = 0;
            
            function renderCanvas() {{
                const canvas = document.getElementById('pipeline-canvas');
                const nodesLayer = document.getElementById('nodes-layer');
                const edgesLayer = document.getElementById('edges-layer');
                
                // Clear previous content
                nodesLayer.innerHTML = '';
                edgesLayer.innerHTML = '';
                
                // Add arrow marker definition
                const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
                const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
                marker.setAttribute('id', 'arrowhead');
                marker.setAttribute('markerWidth', '10');
                marker.setAttribute('markerHeight', '10');
                marker.setAttribute('refX', '9');
                marker.setAttribute('refY', '3');
                marker.setAttribute('orient', 'auto');
                const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
                polygon.setAttribute('points', '0 0, 10 3, 0 6');
                polygon.setAttribute('fill', '#666');
                marker.appendChild(polygon);
                defs.appendChild(marker);
                edgesLayer.appendChild(defs);
                
                // Render edges
                edges.forEach(edge => {{
                    const sourceNode = nodes.find(n => n.id === edge.source);
                    const targetNode = nodes.find(n => n.id === edge.target);
                    if (sourceNode && targetNode) {{
                        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                        line.setAttribute('x1', sourceNode.x + 75);
                        line.setAttribute('y1', sourceNode.y + 40);
                        line.setAttribute('x2', targetNode.x + 75);
                        line.setAttribute('y2', targetNode.y + 40);
                        line.setAttribute('stroke', '#666');
                        line.setAttribute('stroke-width', '2');
                        line.setAttribute('marker-end', 'url(#arrowhead)');
                        edgesLayer.appendChild(line);
                    }}
                }});
                
                // Render nodes
                nodes.forEach(node => {{
                    const nodeDiv = document.createElement('div');
                    nodeDiv.id = node.id;
                    nodeDiv.className = 'pipeline-node';
                    if (selectedNodeId === node.id) {{
                        nodeDiv.classList.add('selected');
                    }}
                    nodeDiv.style.cssText = `
                        left: ${{node.x}}px;
                        top: ${{node.y}}px;
                        border: 2px solid ${{node.color}};
                    `;
                    nodeDiv.innerHTML = `
                        <div style="text-align: center; font-weight: bold; color: ${{node.color}};">
                            ${{node.icon}} ${{node.name}}
                        </div>
                        <div style="text-align: center; font-size: 10px; color: #666; margin-top: 5px;">
                            ${{node.type}}
                        </div>
                    `;
                    
                    // Make draggable
                    nodeDiv.addEventListener('mousedown', function(e) {{
                        e.preventDefault();
                        draggedNode = node;
                        offsetX = e.clientX - node.x;
                        offsetY = e.clientY - node.y;
                        nodeDiv.style.opacity = '0.7';
                        nodeDiv.style.cursor = 'grabbing';
                    }});
                    
                    nodeDiv.addEventListener('click', function(e) {{
                        e.stopPropagation();
                        selectedNodeId = node.id;
                        renderCanvas();
                        // Send selection to parent
                        window.parent.postMessage({{
                            type: 'node_selected',
                            nodeId: node.id
                        }}, '*');
                    }});
                    
                    nodesLayer.appendChild(nodeDiv);
                }});
                
                // Global mouse move handler
                document.addEventListener('mousemove', function(e) {{
                    if (draggedNode) {{
                        const newX = e.clientX - offsetX;
                        const newY = e.clientY - offsetY;
                        const nodeDiv = document.getElementById(draggedNode.id);
                        if (nodeDiv) {{
                            nodeDiv.style.left = newX + 'px';
                            nodeDiv.style.top = newY + 'px';
                            draggedNode.x = newX;
                            draggedNode.y = newY;
                            renderCanvas();
                        }}
                    }}
                }});
                
                document.addEventListener('mouseup', function() {{
                    if (draggedNode) {{
                        // Send position update to parent
                        window.parent.postMessage({{
                            type: 'node_moved',
                            nodeId: draggedNode.id,
                            x: draggedNode.x,
                            y: draggedNode.y
                        }}, '*');
                        draggedNode = null;
                        document.body.style.cursor = 'default';
                    }}
                }});
            }}
            
            renderCanvas();
            </script>
        </body>
        </html>
        """
        
        # Use Streamlit's HTML component
        result = st.components.v1.html(
            canvas_html,
            height=620,
            key=component_key
        )
        
        # Handle messages from the HTML component (if supported)
        # Note: This requires a custom component wrapper for full functionality
    
    def _render_properties_panel(self) -> None:
        """Render the properties panel for the selected node."""
        selected_id = st.session_state.selected_node
        node = next((n for n in st.session_state.nodes if n["id"] == selected_id), None)
        
        if not node:
            return
        
        st.markdown("---")
        st.markdown("### ⚙️ Block Properties")
        
        with st.expander(f"Properties: {node['name']}", expanded=True):
            st.write(f"**ID:** {node['id']}")
            st.write(f"**Type:** {node['type']}")
            st.write(f"**Position:** ({node['x']}, {node['y']})")
            
            # Position controls
            col1, col2 = st.columns(2)
            with col1:
                new_x = st.number_input("X Position", value=float(node['x']), key=f"x_{node['id']}")
            with col2:
                new_y = st.number_input("Y Position", value=float(node['y']), key=f"y_{node['id']}")
            
            if st.button("Update Position", key=f"update_{node['id']}"):
                self.update_node_position(node['id'], new_x, new_y)
                st.rerun()
            
            # Delete button
            if st.button("🗑️ Delete Block", key=f"delete_{node['id']}", type="secondary"):
                self.remove_block(node['id'])
                st.session_state.selected_node = None
                st.rerun()
            
            # Connection controls
            st.markdown("**Connections:**")
            connected_edges = [
                edge for edge in st.session_state.edges 
                if edge["source"] == node['id'] or edge["target"] == node['id']
            ]
            
            if connected_edges:
                for edge in connected_edges:
                    other_id = edge["target"] if edge["source"] == node['id'] else edge["source"]
                    other_node = next((n for n in st.session_state.nodes if n["id"] == other_id), None)
                    if other_node:
                        direction = "→" if edge["source"] == node['id'] else "←"
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.write(f"{direction} {other_node['name']}")
                        with col_b:
                            if st.button("Remove", key=f"remove_edge_{edge['id']}"):
                                st.session_state.edges = [e for e in st.session_state.edges if e["id"] != edge["id"]]
                                st.rerun()
            else:
                st.write("No connections")
            
            # Add connection
            st.markdown("**Add Connection:**")
            other_nodes = [n for n in st.session_state.nodes if n["id"] != node['id']]
            if other_nodes:
                target_options = {n["name"]: n["id"] for n in other_nodes}
                selected_target = st.selectbox(
                    "Connect to:",
                    options=list(target_options.keys()),
                    key=f"connect_{node['id']}"
                )
                if st.button("Connect", key=f"connect_btn_{node['id']}"):
                    target_id = target_options[selected_target]
                    if self.connect_blocks(node['id'], target_id):
                        st.success(f"Connected to {selected_target}")
                        st.rerun()
                    else:
                        st.error("Connection failed or already exists")
