import streamlit as st
from frontend.components.block_library import render_block_library
from frontend.components.canvas import Canvas
from backend.engine.pipeline_engine import validate, simulate


def _generate_optimization_suggestions(result, blocks) -> list[dict]:
    """Generate optimization suggestions based on simulation results."""
    suggestions = []
    
    if not result or not result.success:
        return suggestions
    
    # Find bottleneck (block with highest latency)
    if result.block_metrics:
        bottleneck = max(result.block_metrics.items(), key=lambda x: x[1]['latency_ms'])
        bottleneck_type = bottleneck[1]['type']
        bottleneck_latency = bottleneck[1]['latency_ms']
        
        if bottleneck_latency > 100:
            suggestions.append({
                'type': 'warning',
                'title': '🔴 Remove bottleneck',
                'description': f'"{bottleneck_type}" is slowing down your pipeline ({bottleneck_latency:.0f}ms). Consider optimizing or replacing it.',
                'impact': 'High'
            })
    
    # Check for partitioning opportunities
    spark_blocks = [b for b in blocks.values() if b.get('type') in ['Join', 'Aggregate', 'Filter', 'Union']]
    if len(spark_blocks) >= 2:
        suggestions.append({
            'type': 'info',
            'title': '📊 Add partitioning',
            'description': 'Multiple transform blocks detected. Add partitioning to improve parallel processing.',
            'impact': 'Medium'
        })
    
    # Check throughput
    if result.throughput < 1000:
        suggestions.append({
            'type': 'warning',
            'title': '⚡ Increase throughput',
            'description': f'Current throughput ({result.throughput:.0f}/s) is low. Consider adding caching or parallel processing.',
            'impact': 'High'
        })
    
    # Check cost efficiency
    if result.total_cost > 0.1:
        suggestions.append({
            'type': 'info',
            'title': '💰 Reduce costs',
            'description': f'Pipeline cost (${result.total_cost:.4f}) could be optimized. Consider batch processing.',
            'impact': 'Medium'
        })
    
    # Check for streaming opportunities
    reader_blocks = [b for b in blocks.values() if 'Reader' in b.get('type', '')]
    if len(reader_blocks) > 1:
        suggestions.append({
            'type': 'info',
            'title': '🌊 Use streaming',
            'description': 'Multiple data sources detected. Consider using Streaming Reader for real-time processing.',
            'impact': 'Low'
        })
    
    # Check for caching
    if len(blocks) > 3 and not any('Cache' in b.get('type', '') for b in blocks.values()):
        suggestions.append({
            'type': 'info',
            'title': '💾 Add caching',
            'description': 'Pipeline has multiple blocks. Add Cache Writer to store intermediate results.',
            'impact': 'Medium'
        })
    
    return suggestions


def render_game():
    """Render the main game page with ETL pipeline builder."""
    st.title("🎮 ETL Builder Tycoon - Game")

    # Sidebar: Optimization Suggestions
    with st.sidebar:
        st.markdown("## 🔧 Optimization Suggestions")
        st.markdown("---")
        
        if 'simulation_result' in st.session_state and st.session_state.simulation_result.success:
            result = st.session_state.simulation_result
            # Get blocks from session state
            blocks = st.session_state.get('canvas_blocks', {})
            suggestions = _generate_optimization_suggestions(result, blocks)
            
            if suggestions:
                for i, suggestion in enumerate(suggestions):
                    with st.expander(f"{suggestion['title']}", expanded=(i == 0)):
                        st.write(suggestion['description'])
                        
                        impact_color = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
                        st.caption(f"Impact: {impact_color.get(suggestion['impact'], '⚪')} {suggestion['impact']}")
                        
                        if st.button(f"Apply", key=f"apply_{i}", use_container_width=True):
                            st.success(f"Applied: {suggestion['title']}")
            else:
                st.success("✓ Pipeline is well optimized!")
        else:
            st.info("Run simulation to see suggestions")
        
        st.markdown("---")
        st.markdown("### 📈 Quick Tips")
        st.markdown("""
        - 🔄 **Partitioning**: Split large datasets
        - ⚡ **Caching**: Store intermediate results  
        - 🌊 **Streaming**: Process data in real-time
        - 📦 **Batching**: Group operations together
        """)

    # Create three-column layout
    left_col, center_col, right_col = st.columns([2, 4, 2])

    # Center Column: Canvas (initialize first)
    with center_col:
        canvas = Canvas()
        canvas.render()

    # Left Column: Block Library
    with left_col:
        render_block_library(canvas)

    # Right Column: Metrics Panel + Event Log
    with right_col:
        # Build graph from canvas
        graph = {
            'blocks': canvas.blocks,
            'connections': canvas.connections
        }

        # Validation Section
        with st.container():
            st.markdown("### ✅ Pipeline Validation")
            st.markdown("---")

            if canvas.blocks:
                errors = validate(graph)
                
                error_count = sum(1 for e in errors if e['type'] == 'error')
                warning_count = sum(1 for e in errors if e['type'] == 'warning')
                
                if not errors:
                    st.success("✓ Pipeline is valid!")
                else:
                    for err in errors:
                        if err['type'] == 'error':
                            st.error(f"❌ {err['message']}")
                        else:
                            st.warning(f"⚠️ {err['message']}")
                
                st.caption(f"Errors: {error_count} | Warnings: {warning_count}")
            else:
                st.info("Add blocks to validate pipeline")

        st.markdown("---")

        # Simulation Section
        with st.container():
            st.markdown("### 📊 Simulation Metrics")
            st.markdown("---")

            if canvas.blocks:
                if st.button("▶️ Run Simulation", use_container_width=True):
                    with st.spinner("Simulating pipeline..."):
                        result = simulate(graph)
                        st.session_state.simulation_result = result

                # Display simulation results if available
                if 'simulation_result' in st.session_state:
                    result = st.session_state.simulation_result

                    if result.success:
                        # Key Metrics
                        metric_col1, metric_col2 = st.columns(2)
                        with metric_col1:
                            st.metric("⏱️ Latency", f"{result.total_latency_ms:.1f}ms")
                            st.metric("📦 Blocks", len(canvas.blocks))
                        with metric_col2:
                            st.metric("💰 Cost", f"${result.total_cost:.4f}")
                            st.metric("⚡ Throughput", f"{result.throughput:.0f}/s")

                        # Performance bar
                        st.markdown("#### 🚀 Performance")
                        # Calculate efficiency (inverse of latency, capped at 100%)
                        efficiency = min(1.0, 1000 / max(result.total_latency_ms, 1))
                        st.progress(efficiency)
                        st.caption(f"Pipeline Efficiency: {efficiency * 100:.0f}%")

                        # Warnings
                        if result.warnings:
                            st.markdown("#### ⚠️ Warnings")
                            for w in result.warnings[:5]:  # Show first 5 warnings
                                st.caption(f"• {w}")
                    else:
                        st.error("Simulation failed")
                else:
                    st.caption("Click 'Run Simulation' to see metrics")
            else:
                st.info("Add blocks to run simulation")

        st.markdown("---")

        # Event Log
        with st.container():
            st.markdown("### 📋 Event Log")
            st.markdown("---")

            # Dynamic event log based on simulation
            if 'simulation_result' in st.session_state and st.session_state.simulation_result.success:
                result = st.session_state.simulation_result
                events = []
                events.append('<div style="color: #28a745;">[✓] Simulation started</div>')
                
                for block_id, metrics in list(result.block_metrics.items())[:5]:
                    block_type = metrics['type']
                    latency = metrics['latency_ms']
                    events.append(f'<div style="color: #007bff;">[ℹ] {block_type}: {latency:.1f}ms</div>')
                
                events.append(f'<div style="color: #28a745;">[✓] Total: {result.total_latency_ms:.1f}ms, Cost: ${result.total_cost:.4f}</div>')
                
                st.markdown(f"""
                <div style="
                    background-color: #f8f9fa;
                    border-radius: 5px;
                    padding: 10px;
                    max-height: 200px;
                    overflow-y: auto;
                    font-family: monospace;
                    font-size: 11px;
                ">
                    {''.join(events)}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.caption("Run simulation to see events")

        # Quick Actions
        st.markdown("---")
        st.markdown("#### ⚡ Quick Actions")
        if st.button("🔧 Optimize Pipeline", use_container_width=True):
            if 'simulation_result' in st.session_state:
                st.info("💡 Check sidebar for optimization suggestions!")
            else:
                st.warning("Run simulation first to get suggestions")
        if st.button("🗑️ Clear Simulation", use_container_width=True):
            if 'simulation_result' in st.session_state:
                del st.session_state.simulation_result
                st.rerun()

