# ETL Builder Tycoon - Gameplay Flow Guide

## Table of Contents
1. [How to Play](#how-to-play)
2. [Block Types](#block-types)
3. [Pipeline Rules](#pipeline-rules)
4. [Level Progression](#level-progression)

---

## How to Play

### Getting Started

**ETL Builder Tycoon** is a simulation game where you build and manage ETL (Extract, Transform, Load) data pipelines. Your goal is to create efficient, cost-effective pipelines that process data with high quality while managing resources and meeting client requirements.

### Core Gameplay Loop

1. **Build Pipelines**: Drag and drop blocks from the library onto the canvas to create your data pipeline
2. **Connect Blocks**: Link blocks together to define the data flow from sources to destinations
3. **Run & Analyze**: Execute your pipeline and review performance metrics
4. **Optimize**: Improve throughput, reduce costs, and enhance data quality
5. **Complete Objectives**: Meet level requirements to progress and unlock new features

### Key Metrics to Monitor

- **Throughput**: Records per second (RPS) and bytes per second (BPS) - how much data your pipeline can process
- **Cost**: Operational costs including compute, storage, network, licensing, and maintenance
- **Quality**: Data quality score (0.0-1.0) with letter grades (A, B, C, D, F)
- **Latency**: Time taken for data to flow through the pipeline
- **Efficiency**: Actual throughput vs. theoretical maximum

### Game Interface

- **Block Library**: Left sidebar with categorized blocks (Ingestion, Storage, Transform, Orchestration)
- **Canvas**: Main workspace where you build your pipeline visually
- **Metrics Dashboard**: Real-time performance indicators
- **Navigation**: Sidebar with Home, Game, Tutorial, and Leaderboard options

---

## Block Types

Blocks are organized into four main categories, each serving a specific purpose in your pipeline.

### 📥 Ingestion Blocks (Data Sources)

These blocks extract data from various sources:

| Block | Description | Use Cases |
|-------|-------------|-----------|
| **🗃️🛢️ Database Reader** | Connect to relational databases (MySQL, PostgreSQL, SQL Server) | Reading structured data from databases |
| **📄📊 CSV Reader** | Read CSV files with automatic delimiter detection | Importing tabular data from files |
| **🌐🔗 API Reader** | Fetch data from REST APIs with authentication | Integrating with external services |
| **📊🌊 Streaming Reader** | Process real-time streaming data (Kafka, Kinesis) | Handling live data feeds |
| **📋📈 Excel Reader** | Read Excel files (.xlsx, .xls) with multiple sheets | Processing spreadsheet data |
| **🗂️💿 File System Reader** | Read files from local or cloud storage (S3, GCS, Azure) | Accessing files with pattern matching |

**Rules**: 
- Every pipeline must have at least one Ingestion block
- Multiple sources can feed into the same pipeline
- Streaming sources require special handling for backpressure

### 💾 Storage Blocks (Data Destinations)

These blocks load data into various storage systems:

| Block | Description | Use Cases |
|-------|-------------|-----------|
| **🗃️ Database Writer** | Write to relational databases with transactions | Storing structured data |
| **📄 CSV Writer** | Export to CSV files with customizable options | Creating data exports |
| **📊 Data Lake Writer** | Write to data lakes (S3, Delta Lake) with partitioning | Storing large-scale data |
| **💾 Cache Writer** | Store in Redis, Memcached, or in-memory cache | Fast access to intermediate results |
| **📋 Excel Writer** | Export to Excel with formatting and charts | Creating formatted reports |
| **🗂️ File System Writer** | Write files to local or cloud storage | Archiving and backup |

**Rules**:
- Every pipeline must have at least one Storage block
- Multiple destinations can receive data from the same pipeline
- Storage blocks affect cost based on data volume

### 🔄 Transform Blocks (Data Processing)

These blocks modify and process data as it flows through the pipeline:

| Block | Description | Use Cases |
|-------|-------------|-----------|
| **🔍🎯 Filter** | Filter rows based on conditions, remove duplicates | Data cleaning and subsetting |
| **🔀🔗 Join** | Combine datasets using inner/left/right/full joins | Merging related data |
| **📈🧮 Aggregate** | Group data and calculate aggregations (sum, count, avg) | Summarizing data |
| **➕🔗 Union** | Combine multiple datasets with same schema | Merging similar datasets |
| **🏷️ Rename Columns** | Rename column headers and standardize naming | Data standardization |
| **➗ Split** | Split datasets based on conditions or columns | Dividing data streams |
| **🔢 Type Converter** | Convert data types (string to number, date parsing) | Data type normalization |
| **🧹 Data Cleaner** | Handle missing values, outliers, data quality issues | Improving data quality |

**Rules**:
- Transform blocks can be chained together
- Each transform operation adds latency and processing cost
- Complex transforms may reduce throughput

### 🎯 Orchestration Blocks (Flow Control)

These blocks control when and how pipeline components execute:

| Block | Description | Use Cases |
|-------|-------------|-----------|
| **⏰📅 Scheduler** | Schedule execution at specific times/intervals | Automated pipeline runs |
| **🔄🔁 Loop** | Iterate over datasets or repeat operations | Processing collections |
| **🔀❓ Conditional** | Execute different paths based on conditions | Branching logic |
| **📊🌿 Branch** | Split execution into parallel branches | Concurrent processing |
| **🔔⚡ Trigger** | Wait for external events or file arrivals | Event-driven pipelines |
| **⚡🔀 Parallel** | Execute multiple operations simultaneously | Performance optimization |

**Rules**:
- Orchestration blocks enable complex workflows
- Parallel processing can improve throughput but increases cost
- Conditional logic affects data quality based on path taken

---

## Pipeline Rules

### Basic Pipeline Structure

1. **Minimum Requirements**:
   - At least **one Ingestion block** (source)
   - At least **one Storage block** (destination)
   - Valid connections between blocks

2. **Connection Rules**:
   - Data flows from Ingestion → Transform → Storage
   - Transform blocks can be chained: `Source → Transform1 → Transform2 → Destination`
   - Multiple sources can feed into a single transform
   - A single source can feed multiple destinations (branching)
   - Storage blocks cannot connect to other blocks (endpoints)

3. **Valid Pipeline Patterns**:
   ```
   Simple:     Source → Transform → Destination
   Parallel:   Source → Branch → [Transform1, Transform2] → Union → Destination
   Conditional: Source → Conditional → [Path A, Path B] → Destination
   Multi-source: [Source1, Source2] → Join → Transform → Destination
   ```

### Performance Constraints

1. **Throughput Bottlenecks**:
   - The slowest block in your pipeline determines overall throughput
   - Complex transforms reduce records per second
   - Network transfers add latency
   - Identify bottlenecks using the Throughput Engine

2. **Cost Factors**:
   - **Compute**: Processing time (milliseconds × compute rate)
   - **Storage**: Data volume (GB × storage rate per month)
   - **Network**: Data transfer (GB × network rate)
   - **Licensing**: Software licenses for premium blocks
   - **Maintenance**: Ongoing operational overhead

3. **Quality Metrics**:
   - **Completeness** (20% weight): Percentage of expected data present
   - **Accuracy** (25% weight): Correctness of data values
   - **Consistency** (15% weight): Uniformity across datasets
   - **Timeliness** (15% weight): Data freshness and latency
   - **Validity** (15% weight): Conformance to schema/rules
   - **Uniqueness** (10% weight): Absence of duplicates

4. **Quality Grades**:
   - **A**: Score ≥ 0.95 (Excellent)
   - **B**: Score ≥ 0.85 (Good)
   - **C**: Score ≥ 0.70 (Acceptable)
   - **D**: Score ≥ 0.50 (Poor)
   - **F**: Score < 0.50 (Failing)

### Validation Rules

1. **Schema Compatibility**: 
   - Blocks must have compatible data schemas when connected
   - Type converters help resolve mismatches
   - Schema violations reduce quality scores

2. **Error Propagation**:
   - Errors at source blocks propagate through the pipeline
   - Transform blocks can introduce new errors
   - Quality blocks can filter or correct errors

3. **Resource Limits**:
   - Each block consumes compute resources
   - Storage blocks have capacity limits
   - Exceeding limits causes pipeline failures

4. **Backpressure**:
   - Streaming sources can overwhelm slow transforms
   - Use Parallel blocks to handle high throughput
   - Monitor queue depth to prevent data loss

### Optimization Strategies

1. **Cost Optimization**:
   - Use caching to reduce redundant processing
   - Minimize data transfers between cloud regions
   - Choose appropriate storage tiers
   - Remove unnecessary transform steps

2. **Throughput Optimization**:
   - Identify and scale bottleneck blocks
   - Use Parallel blocks for independent operations
   - Optimize join operations (use indexes when possible)
   - Reduce data volume early with filters

3. **Quality Optimization**:
   - Add Data Cleaner blocks early in the pipeline
   - Validate schemas at ingestion points
   - Use Type Converters to normalize data
   - Monitor error rates and add error handling

---

## Level Progression

### Level System Overview

Levels introduce progressively complex challenges, unlocking new blocks and features as you advance. Each level has specific objectives that must be met to progress.

### Level 1: Getting Started 🎯

**Objective**: Build your first simple pipeline

**Requirements**:
- Create a pipeline with 1 source and 1 destination
- Achieve quality grade C or better
- Complete pipeline run successfully

**Unlocked Blocks**:
- CSV Reader
- CSV Writer
- Filter
- Data Cleaner

**Learning Goals**:
- Understand basic pipeline structure
- Learn to connect blocks
- Monitor quality metrics

**Success Criteria**:
- Pipeline executes without errors
- Quality score ≥ 0.70
- Cost per run < $1.00

---

### Level 2: Data Transformation 🔄

**Objective**: Process and transform data

**Requirements**:
- Use at least 2 transform blocks
- Join data from 2 sources
- Achieve quality grade B or better

**Unlocked Blocks**:
- Database Reader
- Database Writer
- Join
- Aggregate
- Type Converter

**Learning Goals**:
- Master data transformation
- Understand join operations
- Optimize transform chains

**Success Criteria**:
- Throughput ≥ 1000 records/second
- Quality score ≥ 0.85
- Complete join operation successfully

---

### Level 3: Performance Optimization ⚡

**Objective**: Optimize pipeline throughput and cost

**Requirements**:
- Achieve throughput ≥ 5000 RPS
- Reduce cost by 30% from baseline
- Identify and resolve bottlenecks

**Unlocked Blocks**:
- Parallel
- Branch
- Cache Writer
- Streaming Reader

**Learning Goals**:
- Identify performance bottlenecks
- Use parallel processing effectively
- Optimize costs

**Success Criteria**:
- Throughput ≥ 5000 RPS
- Cost reduction ≥ 30%
- No bottlenecks detected

---

### Level 4: Real-time Processing 🌊

**Objective**: Handle streaming data

**Requirements**:
- Process streaming data source
- Handle backpressure
- Maintain quality grade A

**Unlocked Blocks**:
- Streaming Reader
- Trigger
- Conditional
- Data Lake Writer

**Learning Goals**:
- Work with streaming data
- Handle real-time processing challenges
- Maintain quality under load

**Success Criteria**:
- Process streaming data continuously
- Quality score ≥ 0.95
- Zero data loss

---

### Level 5: Enterprise Scale 🏢

**Objective**: Build complex, multi-source pipelines

**Requirements**:
- Integrate 3+ data sources
- Use orchestration blocks
- Achieve quality grade A with cost efficiency

**Unlocked Blocks**:
- All blocks unlocked
- Scheduler
- Loop
- API Reader
- Excel Reader/Writer

**Learning Goals**:
- Design complex pipelines
- Use orchestration effectively
- Balance quality, cost, and performance

**Success Criteria**:
- Quality score ≥ 0.95
- Cost per run < $5.00
- Throughput ≥ 10000 RPS
- Handle 3+ sources simultaneously

---

### Level 6: Advanced Optimization 🚀

**Objective**: Master all aspects of pipeline engineering

**Requirements**:
- Build a pipeline with all block types
- Achieve maximum efficiency score
- Complete within time limit

**Unlocked Blocks**:
- All blocks available
- Advanced configuration options

**Learning Goals**:
- Master advanced techniques
- Optimize all metrics simultaneously
- Handle edge cases

**Success Criteria**:
- Efficiency score ≥ 0.90
- Quality grade A
- Cost optimized
- All block types used

---

### Progression Mechanics

1. **XP System**: Earn experience points for:
   - Completing pipelines
   - Achieving quality milestones
   - Cost optimizations
   - Performance improvements

2. **Unlock Requirements**:
   - Complete level objectives
   - Achieve minimum quality thresholds
   - Meet performance benchmarks

3. **Leaderboard**:
   - Compete with other players
   - Rankings by efficiency, quality, and innovation
   - Special achievements for unique solutions

4. **Replayability**:
   - Replay levels to improve scores
   - Try different optimization strategies
   - Experiment with block combinations

---

## Tips for Success

1. **Start Simple**: Begin with basic pipelines and gradually add complexity
2. **Monitor Metrics**: Keep an eye on all metrics, not just one
3. **Test Incrementally**: Add blocks one at a time and test
4. **Optimize Bottlenecks**: Focus on the slowest part of your pipeline
5. **Balance Trade-offs**: Quality, cost, and performance often conflict
6. **Learn from Failures**: Failed pipelines teach valuable lessons
7. **Experiment**: Try different block combinations to find optimal solutions

---

## Glossary

- **ETL**: Extract, Transform, Load - the process of moving data from sources to destinations
- **Throughput**: Rate of data processing (records/second or bytes/second)
- **Latency**: Time delay in data processing
- **Bottleneck**: The slowest component limiting overall pipeline performance
- **Backpressure**: Resistance to data flow when downstream is slower than upstream
- **Schema**: Structure and data types of a dataset
- **Quality Score**: Overall data quality metric (0.0-1.0)
- **Efficiency**: Ratio of actual performance to theoretical maximum

---

*Happy pipeline building! 🏭*

