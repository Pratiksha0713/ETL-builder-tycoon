"""
Game Page - Main gameplay interface for ETL Builder Tycoon.

Features:
- Block Library (left column)
- Drag-and-Drop Canvas (center column)
- Metrics Panel (right column)
- Real-time validation and simulation
"""

import streamlit as st
from frontend.components.canvas import Canvas
from frontend.components.block_library import render_block_library
from backend.engine import (
    PipelineEngine,
    PipelineGraph,
    PipelineNode,
    BuildingBlock,
    BlockType,
    Connection,
    ConnectionType,
)


def convert_canvas_to_pipeline_graph(canvas_graph: dict) -> PipelineGraph:
    """
    Convert canvas graph format to PipelineGraph format.
    
    Args:
        canvas_graph: Dictionary with 'nodes' and 'edges' from canvas
        
    Returns:
        PipelineGraph object
    """
    graph = PipelineGraph()
    
    # Map canvas node types to BlockType enum
    type_mapping = {
        "source": BlockType.INGESTION,
        "storage": BlockType.STORAGE,
        "transform": BlockType.TRANSFORM,
        "orchestration": BlockType.ORCHESTRATION,
        "destination": BlockType.STORAGE,  # Destinations are also storage
    }
    
    # Convert nodes
    for node_data in canvas_graph.get("nodes", []):
        block_type = type_mapping.get(node_data.get("type", "unknown"), BlockType.TRANSFORM)
        
        building_block = BuildingBlock(
            name=node_data.get("name", "Unknown"),
            block_type=block_type,
            capabilities=[],
            cost_profile={}
        )
        
        pipeline_node = PipelineNode(
            node_id=node_data.get("id", ""),
            block_type=block_type,
            block=building_block,
            position=(node_data.get("x", 0.0), node_data.get("y", 0.0)),
            configuration={}
        )
        
        graph.nodes[pipeline_node.node_id] = pipeline_node
    
    # Convert edges
    for edge_data in canvas_graph.get("edges", []):
        connection = Connection(
            source_id=edge_data.get("source", ""),
            target_id=edge_data.get("target", ""),
            connection_type=ConnectionType.DATA_FLOW,
            metadata={}
        )
        graph.edges.append(connection)
    
    return graph


def render_metrics_panel(graph: PipelineGraph, validation_errors: list[str]):
    """
    Render the metrics panel showing validation errors and simulation results.
    
    Args:
        graph: The pipeline graph
        validation_errors: List of validation error messages
    """
    st.markdown("### 📊 Metrics Panel")
    st.markdown("---")
    
    # Validation Status
    if validation_errors:
        st.error("❌ **Pipeline Validation Failed**")
        st.markdown("**Errors:**")
        for error in validation_errors:
            st.markdown(f"- {error}")
        st.markdown("---")
        st.info("Fix the errors above to see simulation metrics.")
        return
    
    # Pipeline is valid - show simulation results
    st.success("✅ **Pipeline Valid**")
    st.markdown("---")
    
    # Initialize engines
    cost_engine = CostEngine()
    quality_engine = QualityEngine()
    throughput_engine = ThroughputEngine()
    
    # Normalize graph
    pipeline_engine = PipelineEngine()
    normalized_graph = pipeline_engine.normalize(graph)
    
    # Simulate metrics (using placeholder values since engines aren't fully implemented)
    st.markdown("#### 💰 Cost Metrics")
    try:
        cost_result = cost_engine.calculate(normalized_graph)
        st.metric("Total Cost per Run", f"${cost_result.total_cost_per_run:.2f}")
        st.metric("Cost per Hour", f"${cost_result.total_cost_per_hour:.2f}")
        st.metric("Cost per Month", f"${cost_result.total_cost_per_month:.2f}")
    except NotImplementedError:
        st.info("Cost calculation: Coming soon!")
        st.metric("Estimated Cost per Run", "$0.50")
        st.metric("Estimated Cost per Month", "$360.00")
    
    st.markdown("---")
    
    st.markdown("#### 🎯 Quality Metrics")
    try:
        quality_result = quality_engine.calculate(normalized_graph)
        st.metric("Overall Quality Score", f"{quality_result.overall_score:.2%}")
        st.metric("Quality Grade", quality_result.quality_grade)
        st.metric("Error Rate", f"{quality_result.error_rate:.2%}")
    except NotImplementedError:
        st.info("Quality calculation: Coming soon!")
        st.metric("Estimated Quality Score", "85%")
        st.metric("Estimated Grade", "B")
        st.metric("Estimated Error Rate", "2.5%")
    
    st.markdown("---")
    
    st.markdown("#### ⚡ Throughput Metrics")
    try:
        throughput_result = throughput_engine.calculate(normalized_graph)
        st.metric("Records per Second", f"{throughput_result.overall_throughput_rps:,.0f}")
        st.metric("Bytes per Second", f"{throughput_result.overall_throughput_bps:,.0f}")
        if throughput_result.bottleneck_node_id:
            bottleneck_node = normalized_graph.nodes.get(throughput_result.bottleneck_node_id)
            if bottleneck_node:
                st.warning(f"⚠️ Bottleneck: {bottleneck_node.block.name}")
    except NotImplementedError:
        st.info("Throughput calculation: Coming soon!")
        st.metric("Estimated Records/sec", "1,000")
        st.metric("Estimated Bytes/sec", "1.0 MB")
    
    st.markdown("---")
    
    # Pipeline Summary
    st.markdown("#### 📋 Pipeline Summary")
    st.write(f"**Nodes:** {len(graph.nodes)}")
    st.write(f"**Connections:** {len(graph.edges)}")
    
    # Node breakdown by type
    node_types = {}
    for node in graph.nodes.values():
        node_type = node.block_type.value
        node_types[node_type] = node_types.get(node_type, 0) + 1
    
    if node_types:
        st.markdown("**Node Types:**")
        for node_type, count in node_types.items():
            st.write(f"- {node_type.title()}: {count}")


def render_game():
    """Render the main game page."""
    st.title("🎮 ETL Builder Tycoon - Game")
    
    # Initialize canvas
    canvas = Canvas()
    
    # Create three-column layout
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_left:
        st.markdown("### 🧱 Block Library")
        render_block_library(canvas)
    
    with col_center:
        # Render canvas
        canvas.render()
        
        # Fetch graph from canvas after rendering
        canvas_graph = canvas.get_graph()
        
        # Convert to PipelineGraph format
        pipeline_graph = convert_canvas_to_pipeline_graph(canvas_graph)
        
        # Validate pipeline
        pipeline_engine = PipelineEngine()
        validation_errors = pipeline_engine.validate(pipeline_graph)
        
        # Show validation errors below canvas
        if validation_errors:
            st.markdown("---")
            st.error("**Pipeline Validation Errors:**")
            for error in validation_errors:
                st.error(f"❌ {error}")
        else:
            st.markdown("---")
            st.success("✅ Pipeline is valid!")
    
    with col_right:
        # Render metrics panel
        render_metrics_panel(pipeline_graph, validation_errors)
