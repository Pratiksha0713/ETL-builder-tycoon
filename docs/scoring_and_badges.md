# ETL Builder Tycoon - Scoring Formulas & Badge Criteria

## Table of Contents
1. [Scoring System Overview](#scoring-system-overview)
2. [Scoring Formulas](#scoring-formulas)
3. [Badge Categories](#badge-categories)
4. [Badge Criteria](#badge-criteria)
5. [Leaderboard Rankings](#leaderboard-rankings)

---

## Scoring System Overview

ETL Builder Tycoon uses a multi-dimensional scoring system that evaluates pipelines across four key dimensions:

1. **Quality Score** (0.0 - 1.0): Data quality metrics
2. **Performance Score** (0.0 - 1.0): Throughput and latency efficiency
3. **Cost Efficiency Score** (0.0 - 1.0): Cost optimization relative to baseline
4. **Complexity Score** (0.0 - 1.0): Pipeline sophistication and design quality

These scores combine into an **Overall Pipeline Score** and contribute to **Experience Points (XP)** and **Badge** achievements.

---

## Scoring Formulas

### Quality Score

**Formula**:
```
Quality_Score = Σ(metric_score_i × weight_i) × (1 - error_penalty) × (1 - data_loss_penalty)

Where:
  metric_score_i = Individual metric score (0.0-1.0)
  weight_i = Metric weight (sums to 1.0)
  error_penalty = min(error_rate × 0.5, 0.3)  # Max 30% penalty
  data_loss_penalty = min(data_loss_rate × 0.3, 0.2)  # Max 20% penalty
```

**Metric Weights**:
- Completeness: 20% (0.20)
- Accuracy: 25% (0.25)
- Consistency: 15% (0.15)
- Timeliness: 15% (0.15)
- Validity: 15% (0.15)
- Uniqueness: 10% (0.10)

**Quality Grade Mapping**:
```
A: Quality_Score ≥ 0.95
B: Quality_Score ≥ 0.85
C: Quality_Score ≥ 0.70
D: Quality_Score ≥ 0.50
F: Quality_Score < 0.50
```

**Example Calculation**:
```
Completeness: 0.95 × 0.20 = 0.19
Accuracy: 0.90 × 0.25 = 0.225
Consistency: 0.88 × 0.15 = 0.132
Timeliness: 0.92 × 0.15 = 0.138
Validity: 0.96 × 0.15 = 0.144
Uniqueness: 0.98 × 0.10 = 0.098
─────────────────────────────────────
Weighted Sum: 0.927

Error Rate: 0.02 → Penalty: 0.02 × 0.5 = 0.01
Data Loss: 0.01 → Penalty: 0.01 × 0.3 = 0.003

Quality_Score = 0.927 × (1 - 0.01) × (1 - 0.003)
              = 0.927 × 0.99 × 0.997
              = 0.914 → Grade B
```

---

### Performance Score

**Formula**:
```
Performance_Score = (throughput_score × 0.5) + (latency_score × 0.3) + (efficiency_score × 0.2)

Where:
  throughput_score = min(actual_rps / target_rps, 1.0)  # Capped at 1.0
  latency_score = min(target_latency_ms / actual_latency_ms, 1.0)  # Lower is better
  efficiency_score = actual_throughput / theoretical_max_throughput
```

**Throughput Score**:
```
throughput_score = min(actual_rps / target_rps, 1.0)

If actual_rps ≥ target_rps: throughput_score = 1.0
If actual_rps < target_rps: throughput_score = actual_rps / target_rps
```

**Latency Score**:
```
latency_score = min(target_latency_ms / actual_latency_ms, 1.0)

If actual_latency ≤ target_latency: latency_score = 1.0
If actual_latency > target_latency: latency_score = target / actual
```

**Efficiency Score**:
```
efficiency_score = actual_throughput / theoretical_max_throughput

theoretical_max_throughput = min(node_capacity_i) for all nodes
actual_throughput = measured pipeline throughput
```

**Example Calculation**:
```
Target RPS: 5000
Actual RPS: 4500
throughput_score = 4500 / 5000 = 0.90

Target Latency: 1000ms
Actual Latency: 800ms
latency_score = 1000 / 800 = 1.0 (capped)

Theoretical Max: 6000 RPS
Actual: 4500 RPS
efficiency_score = 4500 / 6000 = 0.75

Performance_Score = (0.90 × 0.5) + (1.0 × 0.3) + (0.75 × 0.2)
                  = 0.45 + 0.30 + 0.15
                  = 0.90
```

---

### Cost Efficiency Score

**Formula**:
```
Cost_Efficiency_Score = min(baseline_cost / actual_cost, 1.0) × cost_breakdown_bonus

Where:
  baseline_cost = Expected cost for similar pipeline
  actual_cost = Actual pipeline cost
  cost_breakdown_bonus = 1.0 + (optimization_bonus × 0.1)  # Max 10% bonus
```

**Cost Breakdown**:
```
Total_Cost = Compute_Cost + Storage_Cost + Network_Cost + Licensing_Cost + Maintenance_Cost

Compute_Cost = Σ(processing_time_ms × compute_rate_per_ms) for all nodes
Storage_Cost = data_volume_gb × storage_rate_per_gb_per_month × retention_months
Network_Cost = data_transfer_gb × network_rate_per_gb
Licensing_Cost = Σ(license_cost) for premium blocks
Maintenance_Cost = total_cost × maintenance_overhead_rate
```

**Optimization Bonus**:
```
optimization_bonus = count of optimization techniques used:
  - Caching: +1
  - Parallel processing: +1
  - Early filtering: +1
  - Efficient storage tier: +1
  - Cost-effective block selection: +1
```

**Example Calculation**:
```
Baseline Cost: $10.00 per run
Actual Cost: $7.50 per run
cost_efficiency_ratio = 10.00 / 7.50 = 1.333 → capped at 1.0

Optimizations used: Caching, Parallel processing, Early filtering
optimization_bonus = 3
cost_breakdown_bonus = 1.0 + (3 × 0.1) = 1.3 → capped at 1.1

Cost_Efficiency_Score = 1.0 × 1.1 = 1.1 → capped at 1.0
```

---

### Complexity Score

**Formula**:
```
Complexity_Score = (block_diversity × 0.3) + (orchestration_score × 0.3) + (design_quality × 0.4)

Where:
  block_diversity = unique_block_types / total_block_types_available
  orchestration_score = orchestration_blocks_used / max_orchestration_blocks
  design_quality = (modularity + reusability + maintainability) / 3
```

**Block Diversity**:
```
block_diversity = count(unique_block_types) / total_available_block_types

Total available: 26 block types
Used unique types: 12
block_diversity = 12 / 26 = 0.462
```

**Orchestration Score**:
```
orchestration_score = min(orchestration_blocks_used / 6, 1.0)

Orchestration blocks: Scheduler, Loop, Conditional, Branch, Trigger, Parallel
Used: 3 blocks
orchestration_score = 3 / 6 = 0.50
```

**Design Quality** (Subjective metrics):
```
modularity = 1.0 - (avg_blocks_per_path / max_recommended_blocks)
reusability = reusable_components / total_components
maintainability = 1.0 - (complexity_penalties / max_penalties)

design_quality = (modularity + reusability + maintainability) / 3
```

**Example Calculation**:
```
Block Diversity: 12/26 = 0.462
Orchestration: 3/6 = 0.50
Design Quality: (0.80 + 0.70 + 0.85) / 3 = 0.783

Complexity_Score = (0.462 × 0.3) + (0.50 × 0.3) + (0.783 × 0.4)
                 = 0.139 + 0.15 + 0.313
                 = 0.602
```

---

### Overall Pipeline Score

**Formula**:
```
Overall_Score = (Quality_Score × 0.35) + 
                (Performance_Score × 0.30) + 
                (Cost_Efficiency_Score × 0.20) + 
                (Complexity_Score × 0.15)

Score Range: 0.0 - 1.0 (displayed as 0 - 1000 points)
```

**Example Calculation**:
```
Quality_Score: 0.914
Performance_Score: 0.90
Cost_Efficiency_Score: 1.0
Complexity_Score: 0.602

Overall_Score = (0.914 × 0.35) + (0.90 × 0.30) + (1.0 × 0.20) + (0.602 × 0.15)
              = 0.320 + 0.270 + 0.200 + 0.090
              = 0.880
              = 880 points (out of 1000)
```

---

### Experience Points (XP) Calculation

**Base XP Formula**:
```
Base_XP = Overall_Score × level_multiplier × completion_bonus

Where:
  level_multiplier = current_level × 10
  completion_bonus = 1.0 (base) + (quality_bonus + performance_bonus + cost_bonus)
```

**XP Bonuses**:
```
Quality Bonus:
  Grade A: +0.5
  Grade B: +0.3
  Grade C: +0.1
  Grade D: 0.0
  Grade F: -0.2

Performance Bonus:
  Throughput ≥ target: +0.3
  Latency ≤ target: +0.2
  Efficiency ≥ 0.9: +0.2

Cost Bonus:
  Cost reduction ≥ 30%: +0.3
  Cost reduction ≥ 20%: +0.2
  Cost reduction ≥ 10%: +0.1
```

**XP Calculation Example**:
```
Overall_Score: 0.880
Level: 3
Level Multiplier: 3 × 10 = 30

Quality: Grade B → +0.3
Performance: All targets met → +0.7
Cost: 25% reduction → +0.2
Completion Bonus: 1.0 + 0.3 + 0.7 + 0.2 = 2.2

Base_XP = 0.880 × 30 × 2.2 = 58.08 XP
```

**XP Milestones**:
- Level 1: 0-100 XP
- Level 2: 100-300 XP
- Level 3: 300-600 XP
- Level 4: 600-1000 XP
- Level 5: 1000-1500 XP
- Level 6: 1500+ XP

---

## Badge Categories

Badges are organized into six categories:

1. **Quality Badges** 🏆: Excellence in data quality
2. **Performance Badges** ⚡: Speed and throughput achievements
3. **Cost Badges** 💰: Cost optimization mastery
4. **Innovation Badges** 🚀: Creative and advanced solutions
5. **Efficiency Badges** 📊: Overall efficiency achievements
6. **Specialty Badges** 🎯: Domain-specific expertise

---

## Badge Criteria

### Quality Badges 🏆

#### 🥇 Perfect Quality
**Criteria**: Achieve Quality Score ≥ 0.99
**Tier**: Legendary
**XP Reward**: +50 XP
**Description**: Maintain near-perfect data quality across all metrics

#### 🥈 Quality Master
**Criteria**: Achieve Quality Grade A (≥0.95) in 10 consecutive runs
**Tier**: Epic
**XP Reward**: +30 XP
**Description**: Consistently deliver excellent data quality

#### 🥉 Data Guardian
**Criteria**: Zero data loss and error rate < 0.01% in a pipeline run
**Tier**: Rare
**XP Reward**: +20 XP
**Description**: Protect data integrity throughout the pipeline

#### 📋 Schema Validator
**Criteria**: Zero schema violations across 5 different pipeline types
**Tier**: Rare
**XP Reward**: +15 XP
**Description**: Master schema compatibility across diverse data sources

#### 🧹 Clean Data Expert
**Criteria**: Use Data Cleaner blocks effectively to improve quality by ≥20%
**Tier**: Common
**XP Reward**: +10 XP
**Description**: Expertly clean and validate data

---

### Performance Badges ⚡

#### 🥇 Speed Demon
**Criteria**: Achieve throughput ≥ 50,000 RPS
**Tier**: Legendary
**XP Reward**: +50 XP
**Description**: Process massive data volumes at incredible speed

#### 🥈 Throughput Champion
**Criteria**: Achieve throughput ≥ 10,000 RPS
**Tier**: Epic
**XP Reward**: +30 XP
**Description**: Handle high-volume data processing

#### 🥉 Latency Slayer
**Criteria**: Achieve latency < 100ms for end-to-end pipeline
**Tier**: Rare
**XP Reward**: +20 XP
**Description**: Minimize processing delays

#### 🔄 Parallel Master
**Criteria**: Use Parallel blocks to achieve ≥3x throughput improvement
**Tier**: Rare
**XP Reward**: +15 XP
**Description**: Master parallel processing techniques

#### ⚡ Bottleneck Breaker
**Criteria**: Identify and resolve 5 bottlenecks in different pipelines
**Tier**: Common
**XP Reward**: +10 XP
**Description**: Expert at finding and fixing performance issues

#### 🌊 Streaming Pro
**Criteria**: Process streaming data with zero lag and zero data loss
**Tier**: Epic
**XP Reward**: +30 XP
**Description**: Master real-time data processing

---

### Cost Badges 💰

#### 🥇 Cost Optimizer Supreme
**Criteria**: Reduce pipeline cost by ≥50% from baseline
**Tier**: Legendary
**XP Reward**: +50 XP
**Description**: Achieve exceptional cost savings

#### 🥈 Budget Master
**Criteria**: Complete level with cost per run < $1.00
**Tier**: Epic
**XP Reward**: +30 XP
**Description**: Maintain extremely low operational costs

#### 🥉 Frugal Engineer
**Criteria**: Reduce cost by ≥30% in 5 different pipelines
**Tier**: Rare
**XP Reward**: +20 XP
**Description**: Consistently optimize costs

#### 💾 Cache Wizard
**Criteria**: Use caching to reduce compute cost by ≥40%
**Tier**: Rare
**XP Reward**: +15 XP
**Description**: Master caching strategies

#### 📊 Cost Analyst
**Criteria**: Achieve Cost Efficiency Score ≥ 0.95
**Tier**: Common
**XP Reward**: +10 XP
**Description**: Deep understanding of cost factors

#### 🎯 Smart Spender
**Criteria**: Complete 3 levels spending < $5.00 total
**Tier**: Epic
**XP Reward**: +30 XP
**Description**: Maximize value with minimal spending

---

### Innovation Badges 🚀

#### 🥇 Architect
**Criteria**: Build pipeline using all 26 block types
**Tier**: Legendary
**XP Reward**: +50 XP
**Description**: Master all available tools

#### 🥈 Innovation Leader
**Criteria**: Create pipeline with Complexity Score ≥ 0.90
**Tier**: Epic
**XP Reward**: +30 XP
**Description**: Design sophisticated, elegant solutions

#### 🥉 Creative Builder
**Criteria**: Use 3+ orchestration blocks in a single pipeline
**Tier**: Rare
**XP Reward**: +20 XP
**Description**: Build complex, orchestrated workflows

#### 🔀 Branch Master
**Criteria**: Create pipeline with 5+ parallel branches
**Tier**: Rare
**XP Reward**: +15 XP
**Description**: Master parallel pipeline architecture

#### 🎨 Design Excellence
**Criteria**: Achieve Complexity Score ≥ 0.80
**Tier**: Common
**XP Reward**: +10 XP
**Description**: Create well-designed pipelines

#### 🧩 Puzzle Solver
**Criteria**: Complete level using minimum required blocks
**Tier**: Rare
**XP Reward**: +15 XP
**Description**: Find elegant, minimal solutions

---

### Efficiency Badges 📊

#### 🥇 Efficiency Master
**Criteria**: Achieve Overall Score ≥ 0.95
**Tier**: Legendary
**XP Reward**: +50 XP
**Description**: Excel across all dimensions

#### 🥈 Balanced Performer
**Criteria**: Achieve all scores (Quality, Performance, Cost, Complexity) ≥ 0.85
**Tier**: Epic
**XP Reward**: +30 XP
**Description**: Maintain excellence across all metrics

#### 🥉 Efficiency Expert
**Criteria**: Achieve Overall Score ≥ 0.90
**Tier**: Rare
**XP Reward**: +20 XP
**Description**: Consistently high performance

#### 📈 Steady Improver
**Criteria**: Improve Overall Score by ≥0.20 across 3 consecutive runs
**Tier**: Rare
**XP Reward**: +15 XP
**Description**: Continuous improvement mindset

#### 🎯 Target Achiever
**Criteria**: Meet all level success criteria on first attempt
**Tier**: Common
**XP Reward**: +10 XP
**Description**: Plan and execute perfectly

#### ⚖️ Perfect Balance
**Criteria**: Achieve Quality, Performance, and Cost scores within 0.05 of each other
**Tier**: Epic
**XP Reward**: +30 XP
**Description**: Master the art of balance

---

### Specialty Badges 🎯

#### 🗄️ Database Expert
**Criteria**: Use Database Reader/Writer in 10 successful pipelines
**Tier**: Rare
**XP Reward**: +15 XP
**Description**: Master relational database operations

#### 🌐 API Integration Pro
**Criteria**: Successfully integrate 5 different API sources
**Tier**: Rare
**XP Reward**: +15 XP
**Description**: Expert at external API integration

#### 📊 Analytics Master
**Criteria**: Use Aggregate blocks to create 10 analytical pipelines
**Tier**: Rare
**XP Reward**: +15 XP
**Description**: Master data aggregation and analytics

#### 🔗 Join Specialist
**Criteria**: Successfully join 20+ datasets across different pipelines
**Tier**: Common
**XP Reward**: +10 XP
**Description**: Expert at data joining operations

#### 📅 Scheduler Pro
**Criteria**: Create 5 scheduled pipelines running successfully
**Tier**: Common
**XP Reward**: +10 XP
**Description**: Master automated pipeline scheduling

#### 🎲 Conditional Logic Expert
**Criteria**: Use Conditional blocks to handle 10+ different scenarios
**Tier**: Common
**XP Reward**: +10 XP
**Description**: Expert at conditional data routing

#### 🏭 Multi-Source Master
**Criteria**: Integrate 5+ data sources in a single pipeline
**Tier**: Epic
**XP Reward**: +30 XP
**Description**: Handle complex multi-source scenarios

#### 🔄 Transform Chain Master
**Criteria**: Chain 10+ transform blocks successfully
**Tier**: Rare
**XP Reward**: +20 XP
**Description**: Master complex transformation sequences

---

### Milestone Badges 🏅

#### 🌟 First Steps
**Criteria**: Complete your first pipeline
**Tier**: Common
**XP Reward**: +5 XP
**Description**: Welcome to ETL Builder Tycoon!

#### 🎓 Level Master
**Criteria**: Complete all 6 levels
**Tier**: Epic
**XP Reward**: +50 XP
**Description**: Complete mastery of all levels

#### 💯 Perfect Run
**Criteria**: Achieve Overall Score = 1.0
**Tier**: Legendary
**XP Reward**: +100 XP
**Description**: The ultimate achievement - perfect pipeline!

#### 🔥 Streak Master
**Criteria**: Complete 10 levels in a row without failure
**Tier**: Epic
**XP Reward**: +40 XP
**Description**: Maintain consistent excellence

#### 🎯 Precision Engineer
**Criteria**: Complete level with zero errors and perfect quality
**Tier**: Legendary
**XP Reward**: +75 XP
**Description**: Flawless execution

---

## Leaderboard Rankings

### Ranking Categories

1. **Overall Score Leaderboard**: Ranked by highest Overall Score
2. **Quality Leaderboard**: Ranked by highest Quality Score
3. **Performance Leaderboard**: Ranked by highest Performance Score
4. **Cost Efficiency Leaderboard**: Ranked by highest Cost Efficiency Score
5. **XP Leaderboard**: Ranked by total accumulated XP
6. **Badge Leaderboard**: Ranked by total badges earned

### Ranking Formula

**Overall Ranking**:
```
Rank_Score = (Overall_Score × 0.4) + 
              (Total_XP / 1000 × 0.3) + 
              (Badge_Count / 50 × 0.2) + 
              (Completion_Rate × 0.1)

Where:
  Completion_Rate = levels_completed / total_levels
```

### Leaderboard Tiers

- **🥇 Top 1%**: Legendary tier
- **🥈 Top 5%**: Epic tier
- **🥉 Top 10%**: Rare tier
- **⭐ Top 25%**: Common tier
- **📊 All Others**: Participant tier

---

## Badge Display

Badges are displayed with:
- **Icon**: Visual representation
- **Name**: Badge title
- **Tier Color**: 
  - Legendary: Gold 🥇
  - Epic: Purple 🥈
  - Rare: Blue 🥉
  - Common: Gray ⭐
- **Description**: What was achieved
- **Date Earned**: When the badge was unlocked
- **XP Reward**: Experience points awarded

---

## Scoring Tips

1. **Balance is Key**: Focus on all four dimensions, not just one
2. **Quality First**: High quality enables better performance scores
3. **Optimize Early**: Address bottlenecks before scaling
4. **Cost Awareness**: Monitor costs throughout development
5. **Experiment**: Try different approaches to find optimal solutions
6. **Learn from Metrics**: Use detailed metrics to guide improvements

---

*Master the scoring system to climb the leaderboards and earn prestigious badges! 🏆*

