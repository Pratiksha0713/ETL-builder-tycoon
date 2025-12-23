# ETL Builder Tycoon - Architecture Documentation

## Table of Contents
1. [Game Architecture Diagram](#game-architecture-diagram)
2. [Engine Design](#engine-design)
3. [Simulation Flow](#simulation-flow)

---

## Game Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ETL BUILDER TYCOON                              │
│                         Application Architecture                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND LAYER                             │
│                         (Streamlit Web Interface)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │   Home Page  │  │  Game Page   │  │ Tutorial Page│  │Leaderboard │ │
│  │   (home.py)  │  │  (game.py)   │  │              │  │            │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬─────┘ │
│         │                  │                  │                  │       │
│         └──────────────────┼──────────────────┼──────────────────┘       │
│                            │                  │                          │
│                  ┌─────────▼─────────┐  ┌─────▼──────┐                   │
│                  │  Block Library    │  │   Canvas   │                   │
│                  │ (block_library.py)│  │ (canvas.py) │                   │
│                  └─────────┬─────────┘  └─────┬──────┘                   │
│                            │                  │                          │
└────────────────────────────┼──────────────────┼──────────────────────────┘
                             │                  │
                             │ User Actions     │ Pipeline Definition
                             │                  │
┌────────────────────────────▼──────────────────▼──────────────────────────┐
│                         APPLICATION LAYER                                │
│                            (app.py)                                       │
│  - Page routing                                                            │
│  - Session state management                                                │
│  - UI orchestration                                                        │
└────────────────────────────┬──────────────────────────────────────────────┘
                             │
                             │ Pipeline Graph
                             │
┌────────────────────────────▼──────────────────────────────────────────────┐
│                          ENGINE LAYER                                     │
│                      (backend/engine/)                                    │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │                    Pipeline Engine                                    │ │
│  │                  (pipeline_engine.py)                                │ │
│  │  - PipelineGraph: Graph representation                                │ │
│  │  - PipelineNode: Individual block nodes                              │ │
│  │  - BuildingBlock: Block definitions                                  │ │
│  │  - Connection: Edge connections between nodes                         │ │
│  │  - Validation: Structure and schema validation                       │ │
│  └───────────────────────┬─────────────────────────────────────────────┘ │
│                          │                                                 │
│                          │ Normalized Pipeline Graph                       │
│                          │                                                 │
│  ┌───────────────────────▼─────────────────────────────────────────────┐ │
│  │                                                                       │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │ │
│  │  │   Cost       │  │  Throughput  │  │   Quality    │              │ │
│  │  │   Engine     │  │    Engine    │  │    Engine    │              │ │
│  │  │              │  │              │  │              │              │ │
│  │  │ - Compute    │  │ - RPS/BPS    │  │ - Completeness│             │ │
│  │  │ - Storage    │  │ - Bottlenecks│  │ - Accuracy   │             │ │
│  │  │ - Network    │  │ - Efficiency │  │ - Consistency│             │ │
│  │  │ - Licensing  │  │ - Saturation │  │ - Timeliness │             │ │
│  │  │ - Maintenance│  │ - Parallelism│  │ - Validity   │             │ │
│  │  │              │  │              │  │ - Uniqueness │             │ │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │ │
│  │         │                  │                  │                      │ │
│  │         └──────────────────┼──────────────────┘                      │ │
│  │                            │                                         │ │
│  │                  ┌─────────▼─────────┐                              │ │
│  │                  │  Latency Engine   │                              │ │
│  │                  │ (latency_engine.py)│                              │ │
│  │                  │ - End-to-end delay│                              │ │
│  │                  │ - Per-node latency│                              │ │
│  │                  │ - Critical path   │                              │ │
│  │                  └───────────────────┘                              │ │
│  │                                                                       │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└────────────────────────────┬───────────────────────────────────────────────┘
                             │
                             │ Execution Requests
                             │
┌────────────────────────────▼───────────────────────────────────────────────┐
│                        SIMULATION LAYER                                   │
│                    (backend/simulation/)                                    │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   FakeKafka  │  │    FakeS3    │  │  FakeSpark   │  │   FakeSQL    │ │
│  │              │  │              │  │              │  │              │ │
│  │ - Streaming  │  │ - Object     │  │ - Distributed │  │ - Relational │ │
│  │ - Topics     │  │   Storage    │  │   Processing  │  │   Database   │ │
│  │ - Consumers  │  │ - Buckets    │  │ - Jobs       │  │ - Queries    │ │
│  │ - Producers  │  │ - Objects    │  │ - Operations │  │ - Transactions│ │
│  │              │  │              │  │              │  │              │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                  │                  │                  │         │
│         └──────────────────┼──────────────────┼──────────────────┘         │
│                            │                  │                           │
│                  ┌─────────▼──────────────────▼─────────┐                │
│                  │     SimulationMetrics                 │                │
│                  │  - latency_ms                         │                │
│                  │  - cost_units                         │                │
│                  │  - throughput                         │                │
│                  │  - warnings                           │                │
│                  └───────────────────────────────────────┘                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  1. User builds pipeline on Canvas                                           │
│     ↓                                                                         │
│  2. PipelineEngine validates structure                                       │
│     ↓                                                                         │
│  3. PipelineEngine creates PipelineGraph                                     │
│     ↓                                                                         │
│  4. Engines analyze pipeline:                                                │
│     - CostEngine calculates costs                                            │
│     - ThroughputEngine calculates throughput                                 │
│     - QualityEngine calculates quality metrics                               │
│     - LatencyEngine calculates latency                                       │
│     ↓                                                                         │
│  5. Simulation layer executes pipeline blocks                                │
│     ↓                                                                         │
│  6. Results aggregated and displayed in UI                                    │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Engine Design

### Overview

The engine layer is the core computational component of ETL Builder Tycoon. It consists of multiple specialized engines that analyze different aspects of pipeline performance. All engines operate on a normalized `PipelineGraph` representation, ensuring consistency and enabling parallel analysis.

### Pipeline Engine

**Purpose**: Core pipeline representation and validation

**Key Components**:

```
PipelineEngine
├── PipelineGraph
│   ├── nodes: dict[str, PipelineNode]
│   ├── edges: list[Connection]
│   └── metadata: dict
│
├── PipelineNode
│   ├── node_id: str
│   ├── block_type: BlockType
│   ├── block: BuildingBlock
│   ├── position: (x, y)
│   └── configuration: dict
│
├── BuildingBlock
│   ├── name: str
│   ├── category: BlockCategory (INGESTION, STORAGE, TRANSFORM, ORCHESTRATION)
│   ├── capabilities: list[str]
│   └── cost_profile: dict
│
└── Connection
    ├── source_id: str
    ├── target_id: str
    ├── connection_type: ConnectionType
    └── metadata: dict
```

**Responsibilities**:
- Graph construction from user-defined blocks
- Structural validation (cycles, connectivity, endpoints)
- Schema validation and compatibility checking
- Graph normalization and optimization
- Topological sorting for execution order

**Design Patterns**:
- **Graph Representation**: Uses adjacency list for efficient traversal
- **Visitor Pattern**: Engines visit nodes to collect metrics
- **Strategy Pattern**: Different validation strategies per block type

### Cost Engine

**Purpose**: Calculate and optimize pipeline operational costs

**Architecture**:

```
CostEngine
├── Configuration
│   ├── compute_rate_per_ms: float
│   ├── storage_rate_per_gb: float
│   ├── network_rate_per_gb: float
│   └── runs_per_hour: float
│
├── CostCalculation
│   ├── calculate(graph) → CostResult
│   ├── estimate_scaling_cost(graph, factor) → CostResult
│   └── project_monthly_cost(graph, runs, volume) → CostBreakdown
│
└── CostResult
    ├── total_cost_per_run: float
    ├── total_cost_per_month: float
    ├── node_costs: dict[str, float]
    ├── breakdown: CostBreakdown
    └── optimization_suggestions: list[str]
```

**Cost Categories**:
1. **Compute**: Processing time × compute rate
2. **Storage**: Data volume × storage rate × retention period
3. **Network**: Data transfer volume × network rate
4. **Licensing**: Software license costs per block
5. **Maintenance**: Ongoing operational overhead

**Calculation Flow**:
```
For each node in graph:
  1. Estimate processing time (latency × parallelism)
  2. Calculate compute cost = time × compute_rate
  3. Estimate data volume (input + output)
  4. Calculate storage cost = volume × storage_rate
  5. Calculate network cost = transfer × network_rate
  6. Sum licensing costs for premium blocks
  7. Add maintenance overhead
  8. Aggregate per-node costs
```

### Throughput Engine

**Purpose**: Analyze pipeline throughput and identify bottlenecks

**Architecture**:

```
ThroughputEngine
├── Configuration
│   ├── default_record_size_bytes: int
│   ├── parallelism_factor: float
│   └── backpressure_enabled: bool
│
├── ThroughputAnalysis
│   ├── calculate(graph) → ThroughputResult
│   ├── simulate(graph, input_rate, duration) → ThroughputResult
│   ├── find_bottleneck(graph) → str | None
│   └── calculate_saturation_point(graph) → float
│
└── ThroughputResult
    ├── overall_throughput_rps: float
    ├── overall_throughput_bps: float
    ├── node_metrics: dict[str, ThroughputMetrics]
    ├── bottleneck_node_id: str | None
    └── efficiency: float
```

**Throughput Metrics**:
- **Records Per Second (RPS)**: Number of records processed per second
- **Bytes Per Second (BPS)**: Data volume processed per second
- **Utilization**: Node capacity utilization (0.0-1.0)
- **Queue Depth**: Pending records in node queue
- **Bottleneck Detection**: Identifies slowest node limiting overall throughput

**Calculation Algorithm**:
```
1. Topological sort of pipeline graph
2. For each node in execution order:
   a. Calculate input rate (from upstream nodes)
   b. Apply node processing capacity
   c. Account for parallelism
   d. Calculate output rate
   e. Track utilization and queue depth
3. Identify bottleneck (lowest throughput node)
4. Calculate overall pipeline throughput
5. Compute efficiency (actual / theoretical max)
```

### Quality Engine

**Purpose**: Measure and simulate data quality metrics

**Architecture**:

```
QualityEngine
├── Configuration
│   ├── quality_thresholds: dict[str, float]  # A: 0.95, B: 0.85, etc.
│   └── metric_weights: dict[QualityMetricType, float]
│
├── QualityAnalysis
│   ├── calculate(graph) → QualityResult
│   ├── simulate_error_propagation(graph, initial_rate) → dict[str, float]
│   ├── validate_schema(graph, schemas) → list[dict]
│   └── identify_weak_points(graph) → list[str]
│
└── QualityResult
    ├── overall_score: float (0.0-1.0)
    ├── quality_grade: str (A-F)
    ├── node_scores: dict[str, float]
    ├── metric_scores: dict[str, QualityScore]
    └── error_rate: float
```

**Quality Metrics** (Weighted):
1. **Completeness** (20%): Percentage of expected data present
2. **Accuracy** (25%): Correctness of data values
3. **Consistency** (15%): Uniformity across datasets
4. **Timeliness** (15%): Data freshness and latency
5. **Validity** (15%): Conformance to schema/rules
6. **Uniqueness** (10%): Absence of duplicates

**Quality Calculation**:
```
For each quality metric:
  1. Calculate metric score per node
  2. Weight by metric importance
  3. Aggregate across pipeline
  4. Apply error propagation model
  5. Calculate overall weighted score
  6. Assign letter grade (A-F)
```

### Latency Engine

**Purpose**: Calculate end-to-end and per-node latency

**Architecture**:

```
LatencyEngine
├── LatencyCalculation
│   ├── calculate(graph) → LatencyResult
│   ├── find_critical_path(graph) → list[str]
│   └── estimate_scaling_impact(graph, node_id, factor) → LatencyResult
│
└── LatencyResult
    ├── total_latency_ms: float
    ├── node_latencies: dict[str, float]
    ├── critical_path: list[str]
    └── parallelization_opportunities: list[str]
```

**Latency Components**:
- **Processing Latency**: Time to process data at each node
- **Network Latency**: Data transfer time between nodes
- **Queue Latency**: Time spent waiting in queues
- **Synchronization Latency**: Time waiting for parallel branches

**Calculation Method**:
```
1. Build dependency graph
2. Calculate earliest start time for each node
3. Calculate latest finish time (reverse traversal)
4. Identify critical path (nodes with zero slack)
5. Sum latencies along critical path
6. Account for parallel branches (max, not sum)
```

### Engine Coordination

**Execution Flow**:

```
┌─────────────────────────────────────────────────────────┐
│              Pipeline Analysis Orchestration             │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────┐
        │   PipelineEngine.normalize()    │
        │   Creates PipelineGraph         │
        └──────────────┬──────────────────┘
                       │
        ┌──────────────▼──────────────────┐
        │   Parallel Engine Execution     │
        │   (Independent calculations)    │
        └──────────────┬──────────────────┘
                       │
        ┌──────────────┼──────────────────┐
        │              │                  │
        ▼              ▼                  ▼
  ┌─────────┐   ┌──────────┐      ┌──────────┐
  │  Cost   │   │Throughput│      │ Quality  │
  │ Engine  │   │  Engine  │      │  Engine  │
  └────┬────┘   └────┬─────┘      └────┬─────┘
       │             │                  │
       └─────────────┼──────────────────┘
                     │
        ┌────────────▼──────────────────┐
        │   LatencyEngine (depends on   │
        │   throughput for queue calc)  │
        └────────────┬──────────────────┘
                     │
        ┌────────────▼──────────────────┐
        │   Aggregate Results            │
        │   - CostResult                 │
        │   - ThroughputResult           │
        │   - QualityResult              │
        │   - LatencyResult              │
        └────────────┬───────────────────┘
                     │
        ┌────────────▼───────────────────┐
        │   Return Combined Metrics      │
        └────────────────────────────────┘
```

**Design Principles**:
1. **Separation of Concerns**: Each engine focuses on one metric domain
2. **Dependency Minimization**: Engines can run in parallel where possible
3. **Normalized Input**: All engines operate on the same PipelineGraph
4. **Extensibility**: New engines can be added without modifying existing ones

---

## Simulation Flow

### Overview

The simulation layer provides mock implementations of real-world data infrastructure components. These simulations execute pipeline operations and return realistic metrics without requiring actual infrastructure.

### Simulation Components

#### FakeKafka (Streaming)

**Purpose**: Simulate Kafka streaming data ingestion

**Key Features**:
- Topic creation and management
- Producer/consumer simulation
- Consumer lag tracking
- Throughput throttling
- Backpressure simulation

**Metrics Returned**:
```python
IngestionMetrics:
  - latency_ms: float
  - cost_units: float
  - throughput: float
  - total_events: int
  - warnings: list[str]
```

**Simulation Flow**:
```
1. Create topic with partitions
2. Producer sends events to topic
3. Consumer reads events (with lag simulation)
4. Calculate throughput based on partition count
5. Apply backpressure if consumer is slow
6. Return metrics with latency and cost
```

#### FakeS3 (Object Storage)

**Purpose**: Simulate S3 object storage operations

**Key Features**:
- Bucket operations (create, list, delete)
- Object operations (put, get, delete)
- Transfer rate simulation
- Storage cost calculation
- Network latency simulation

**Metrics Returned**:
```python
S3Metrics:
  - latency_ms: float
  - cost_units: float
  - throughput: float
  - bytes_transferred: int
  - warnings: list[str]
```

**Simulation Flow**:
```
1. Create/get bucket
2. Upload/download object
3. Calculate transfer time (size / transfer_rate)
4. Add network latency
5. Calculate storage cost (size × rate × duration)
6. Return metrics
```

#### FakeSpark (Distributed Processing)

**Purpose**: Simulate Apache Spark distributed processing

**Key Features**:
- Job submission and execution
- Operation types (map, filter, join, aggregate)
- Parallelism simulation
- Resource utilization
- Shuffle operation simulation

**Metrics Returned**:
```python
SparkMetrics:
  - latency_ms: float
  - cost_units: float
  - throughput: float
  - rows_processed: int
  - warnings: list[str]
```

**Simulation Flow**:
```
1. Create Spark job with operations
2. Estimate processing time per operation
3. Account for parallelism (workers × cores)
4. Simulate shuffle operations (network overhead)
5. Calculate compute cost (time × compute_rate)
6. Return metrics
```

#### FakeSQL (Relational Database)

**Purpose**: Simulate SQL database operations

**Key Features**:
- Query execution (SELECT, INSERT, UPDATE, DELETE)
- Transaction support
- Index utilization simulation
- Connection pooling
- Query optimization hints

**Metrics Returned**:
```python
QueryMetrics:
  - latency_ms: float
  - cost_units: float
  - throughput: float
  - rows_affected: int
  - warnings: list[str]
```

**Simulation Flow**:
```
1. Parse SQL query
2. Estimate execution time (complexity × data_size)
3. Apply index benefits if applicable
4. Simulate network round-trip
5. Calculate storage I/O cost
6. Return metrics
```

### Pipeline Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Pipeline Execution                         │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────┐
        │  User clicks "Run Pipeline"      │
        └──────────────┬──────────────────┘
                       │
        ┌──────────────▼──────────────────┐
        │  PipelineEngine.validate()       │
        │  - Check structure              │
        │  - Validate connections         │
        │  - Check schema compatibility   │
        └──────────────┬──────────────────┘
                       │
                       │ Valid?
                       ▼
        ┌─────────────────────────────────┐
        │  Topological sort of nodes      │
        │  Determine execution order      │
        └──────────────┬──────────────────┘
                       │
        ┌──────────────▼──────────────────┐
        │  For each node in order:        │
        │                                 │
        │  1. Identify block type         │
        │  2. Select simulation service   │
        │  3. Execute operation           │
        │  4. Collect metrics             │
        │  5. Pass data to next node      │
        └──────────────┬──────────────────┘
                       │
        ┌──────────────▼──────────────────┐
        │  Aggregate execution metrics    │
        │  - Total execution time         │
        │  - Total cost                   │
        │  - Records processed            │
        │  - Errors encountered           │
        └──────────────┬──────────────────┘
                       │
        ┌──────────────▼──────────────────┐
        │  Pass metrics to engines        │
        │  - CostEngine                   │
        │  - ThroughputEngine             │
        │  - QualityEngine                │
        │  - LatencyEngine                │
        └──────────────┬──────────────────┘
                       │
        ┌──────────────▼──────────────────┐
        │  Display results in UI          │
        │  - Metrics dashboard           │
        │  - Visual feedback              │
        │  - Optimization suggestions     │
        └─────────────────────────────────┘
```

### Simulation Metrics Standardization

All simulation classes return metrics following a standard interface:

```python
class SimulationMetrics:
    """Base class for all simulation metrics."""
    latency_ms: float      # Operation latency in milliseconds
    cost_units: float      # Simulated cost units
    throughput: float      # Operations/rows/bytes per second
    warnings: list[str]    # Warning messages
```

This standardization enables:
- **Consistent metric collection** across all blocks
- **Easy aggregation** of pipeline-wide metrics
- **Engine compatibility** with all simulation types
- **Extensibility** for new simulation types

### Error Handling and Edge Cases

**Error Propagation**:
```
Source Error → Transform Error → Destination Error
     │              │                  │
     └──────────────┼──────────────────┘
                    │
         ┌──────────▼──────────┐
         │  QualityEngine      │
         │  tracks error rates │
         └─────────────────────┘
```

**Backpressure Handling**:
```
High Input Rate → Queue Fills → Backpressure Signal
     │                              │
     └──────────► Slow Down ────────┘
```

**Resource Limits**:
```
Resource Exhaustion → Pipeline Failure → Error Metrics
```

### Performance Considerations

1. **Lazy Evaluation**: Metrics calculated only when needed
2. **Caching**: Cache simulation results for repeated operations
3. **Parallel Simulation**: Execute independent operations in parallel
4. **Sampling**: Use statistical sampling for large datasets
5. **Early Termination**: Stop simulation on critical errors

---

## Data Flow Summary

```
User Interface
    │
    │ User Actions (drag, drop, connect)
    ▼
Frontend Components (Canvas, Block Library)
    │
    │ Pipeline Definition
    ▼
Application Layer (app.py)
    │
    │ Pipeline Graph
    ▼
Pipeline Engine
    │
    │ Normalized Graph
    ├──► Cost Engine ────────┐
    ├──► Throughput Engine ───┤
    ├──► Quality Engine ──────┤
    └──► Latency Engine ──────┤
                              │
                              │ Metrics
                              ▼
                    Simulation Layer
                              │
                              │ Execution
                              ▼
                    Mock Services (Kafka, S3, Spark, SQL)
                              │
                              │ Results
                              ▼
                    Aggregated Metrics
                              │
                              ▼
                    UI Display
```

---

## Extension Points

### Adding New Engines

1. Create engine class inheriting from base pattern
2. Implement `calculate(graph: PipelineGraph)` method
3. Return standardized result object
4. Register in `backend/engine/__init__.py`
5. Add UI visualization component

### Adding New Simulation Services

1. Create simulation class with standard interface
2. Implement operations returning `SimulationMetrics`
3. Register in `backend/simulation/__init__.py`
4. Map to block types in PipelineEngine
5. Add configuration options

### Adding New Block Types

1. Define `BuildingBlock` with capabilities
2. Add to `BlockType` enum
3. Create UI component in `block_library.py`
4. Implement simulation logic
5. Update validation rules

---

*Architecture designed for extensibility, maintainability, and performance.* 🏗️



