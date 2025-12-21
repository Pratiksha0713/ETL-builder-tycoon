"""
Game Page - Main gameplay interface for ETL Builder Tycoon.

Features:
- Block Library (left column)
- Drag-and-Drop Canvas (center column)
- Metrics Panel (right column)
- Real-time validation and simulation
- Level-based gameplay with scoring
"""

import streamlit as st
import yaml
import os
from pathlib import Path
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
    ScoringEngine,
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


def load_level(level_number: int) -> dict:
    """
    Load level configuration from YAML file.
    
    Args:
        level_number: Level number (1, 2, or 3)
        
    Returns:
        Dictionary with level configuration
    """
    level_file = Path(__file__).parent.parent.parent / "data" / "levels" / f"level{level_number}.yaml"
    
    if not level_file.exists():
        return {}
    
    with open(level_file, 'r') as f:
        return yaml.safe_load(f)


def detect_pipeline_mode(graph: PipelineGraph) -> str:
    """
    Detect if pipeline is batch or streaming based on nodes.
    
    Args:
        graph: The pipeline graph
        
    Returns:
        "streaming" or "batch"
    """
    node_names = [node.block.name.lower() for node in graph.nodes.values()]
    
    # Check for streaming indicators
    streaming_indicators = ["kafka", "streaming", "kinesis"]
    if any(indicator in " ".join(node_names) for indicator in streaming_indicators):
        return "streaming"
    
    # Default to batch
    return "batch"


def render_metrics_panel(
    graph: PipelineGraph,
    validation_errors: list[str],
    level_config: dict | None = None
):
    """
    Render the metrics panel showing validation errors, simulation results, and scoring.
    
    Args:
        graph: The pipeline graph
        validation_errors: List of validation error messages
        level_config: Level configuration dictionary (optional)
    """
    st.markdown("### 📊 Metrics Panel")
    st.markdown("---")
    
    # Validation Status - show live errors
    if validation_errors:
        st.error("❌ **Pipeline Validation Failed**")
        st.markdown("**Errors:**")
        for error in validation_errors:
            st.markdown(f"- {error}")
        st.markdown("---")
        st.info("Fix the errors above to see simulation metrics.")
        return
    
    # Pipeline is valid - run simulation
    st.success("✅ **Pipeline Valid**")
    st.markdown("---")
    
    # Run simulation
    pipeline_engine = PipelineEngine()
    simulation_results = pipeline_engine.simulate(graph)
    
    # Extract metrics
    latency_total = simulation_results.get("latency_total", 0.0)
    throughput_min = simulation_results.get("throughput_min", 0.0)
    cost_total = simulation_results.get("cost_total", 0.0)
    quality_score = simulation_results.get("quality_score", 0.0)
    
    # Collect all warnings
    all_warnings: list[str] = []
    node_results = simulation_results.get("node_results", {})
    for node_id, node_metrics in node_results.items():
        node_warnings = node_metrics.get("warnings", [])
        all_warnings.extend(node_warnings)
    
    # Display simulation metrics
    st.markdown("#### ⚡ Simulation Results")
    st.metric("Total Latency", f"{latency_total:.2f} ms")
    st.metric("Throughput (min)", f"{throughput_min:.2f} records/sec")
    st.metric("Total Cost", f"{cost_total:.2f} units")
    st.metric("Quality Score", f"{quality_score:.1%}")
    
    # Show warnings if any
    if all_warnings:
        st.markdown("---")
        st.warning("⚠️ **Warnings:**")
        for warning in all_warnings[:5]:  # Show first 5 warnings
            st.markdown(f"- {warning}")
        if len(all_warnings) > 5:
            st.caption(f"... and {len(all_warnings) - 5} more warnings")
    
    st.markdown("---")
    
    # Compute score
    scoring_engine = ScoringEngine()
    scoring_result = scoring_engine.compute_score(
        latency_total=latency_total,
        throughput_min=throughput_min,
        cost_total=cost_total,
        quality_score=quality_score,
        warnings=all_warnings if all_warnings else None
    )
    
    # Display score
    st.markdown("#### 🎯 Score")
    st.metric("Final Score", f"{scoring_result.final_score:.1f}")
    
    # Display score breakdown
    with st.expander("Score Breakdown"):
        breakdown = scoring_result.breakdown
        st.write(f"**Latency Score:** {breakdown.latency_score:.1f}")
        st.write(f"**Throughput Score:** {breakdown.throughput_score:.1f}")
        st.write(f"**Quality Score:** {breakdown.quality_score:.1f}")
        st.write(f"**Cost Penalty:** -{breakdown.cost_penalty:.1f}")
    
    # Display badges
    if scoring_result.badges:
        st.markdown("---")
        st.markdown("#### 🏆 Badges Earned")
        for badge in scoring_result.badges:
            st.success(f"🏅 {badge}")
    
    # Check level completion
    if level_config:
        constraints = level_config.get("constraints", {})
        max_cost = constraints.get("max_cost", float('inf'))
        max_latency = constraints.get("max_latency", float('inf'))
        base_score = level_config.get("scoring", {}).get("base_score", 100)
        
        # Level completion criteria
        cost_ok = cost_total <= max_cost
        latency_ok = latency_total <= max_latency
        score_ok = scoring_result.final_score >= base_score
        
        if cost_ok and latency_ok and score_ok:
            st.markdown("---")
            st.balloons()
            st.success("🎉 **Level Complete!** 🎉")
            st.markdown(f"**Score:** {scoring_result.final_score:.1f} (Target: {base_score})")
            st.markdown(f"**Cost:** {cost_total:.2f} / {max_cost} units ✅")
            st.markdown(f"**Latency:** {latency_total:.2f} / {max_latency} ms ✅")
        else:
            st.markdown("---")
            st.info("**Level Progress:**")
            if not cost_ok:
                st.error(f"❌ Cost: {cost_total:.2f} / {max_cost} units (over limit)")
            else:
                st.success(f"✅ Cost: {cost_total:.2f} / {max_cost} units")
            
            if not latency_ok:
                st.error(f"❌ Latency: {latency_total:.2f} / {max_latency} ms (over limit)")
            else:
                st.success(f"✅ Latency: {latency_total:.2f} / {max_latency} ms")
            
            if not score_ok:
                st.warning(f"⚠️ Score: {scoring_result.final_score:.1f} / {base_score} (need {base_score - scoring_result.final_score:.1f} more)")
            else:
                st.success(f"✅ Score: {scoring_result.final_score:.1f} / {base_score}")
    
    st.markdown("---")
    
    # Pipeline Summary
    st.markdown("#### 📋 Pipeline Summary")
    st.write(f"**Nodes:** {len(graph.nodes)}")
    st.write(f"**Connections:** {len(graph.edges)}")
    
    # Detect and display pipeline mode
    mode = detect_pipeline_mode(graph)
    mode_emoji = "🌊" if mode == "streaming" else "📦"
    st.write(f"**Mode:** {mode_emoji} {mode.title()}")


def render_game():
    """Render the main game page."""
    st.title("🎮 ETL Builder Tycoon - Game")
    
    # Level selection
    if "current_level" not in st.session_state:
        st.session_state.current_level = 1
    
    col_level1, col_level2, col_level3, col_spacer = st.columns([1, 1, 1, 2])
    with col_level1:
        if st.button("Level 1", use_container_width=True):
            st.session_state.current_level = 1
            st.rerun()
    with col_level2:
        if st.button("Level 2", use_container_width=True):
            st.session_state.current_level = 2
            st.rerun()
    with col_level3:
        if st.button("Level 3", use_container_width=True):
            st.session_state.current_level = 3
            st.rerun()
    
    # Load level configuration
    level_config = load_level(st.session_state.current_level)
    
    if level_config:
        st.markdown("---")
        st.markdown(f"### {level_config.get('name', f'Level {st.session_state.current_level}')}")
        st.caption(f"**Difficulty:** {level_config.get('difficulty', 'Unknown')}")
        st.write(level_config.get('description', ''))
        
        # Display level objectives
        objectives = level_config.get('objectives', [])
        if objectives:
            st.markdown("**Objectives:**")
            for obj in objectives:
                st.markdown(f"- {obj}")
        
        # Display target blocks
        target_blocks = level_config.get('target_blocks', [])
        if target_blocks:
            st.markdown("**Required Blocks:**")
            st.markdown(", ".join(target_blocks))
        
        constraints = level_config.get('constraints', {})
        if constraints:
            st.markdown(f"**Constraints:** Max Cost: {constraints.get('max_cost', 'N/A')} units, "
                       f"Max Latency: {constraints.get('max_latency', 'N/A')} ms")
    
    st.markdown("---")
    
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
        
        # Validate pipeline - show live errors
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
        # Render metrics panel with level config
        render_metrics_panel(pipeline_graph, validation_errors, level_config)
