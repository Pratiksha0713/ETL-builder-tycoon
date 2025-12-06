# ETL Builder Tycoon 🏭

Ever wondered what it'd be like to run your own data pipeline empire? Welcome to **ETL Builder Tycoon** — a simulation game where you design, optimize, and scale ETL pipelines while managing resources, handling client demands, and trying not to let your servers catch fire (metaphorically... mostly).

## What's This All About?

You start with a tiny data warehouse and a dream. Your job? Build the most efficient data pipelines in the industry. Extract data from quirky sources, transform it without breaking everything, and load it before your clients start sending angry emails.

Think *Factorio* meets *data engineering nightmares*.

---

## Features

**Core Gameplay**
- Drag-and-drop pipeline builder with real-time data flow visualization
- Multiple data source types: APIs, databases, flat files, streaming sources
- Transform nodes: filters, aggregators, joiners, custom scripts
- Performance metrics that actually matter (throughput, latency, error rates)

**Business Simulation**
- Client contracts with SLAs — miss them and watch your reputation tank
- Hire and train data engineers (they have moods, sorry)
- Budget management: hardware costs, cloud bills, coffee expenses
- Tech debt system — cut corners now, pay for it later

**Progression**
- Unlock advanced connectors and transformation nodes
- Scale from single pipelines to distributed architectures
- Prestige system: sell your company and start fresh with bonuses
- Achievements for the completionists out there

**Chaos Events**
- Schema changes at 3 AM
- Surprise data volume spikes
- That one legacy system nobody wants to touch
- Compliance audits (fun!)

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend Engine | Python 3.11+ |
| Game Simulation | Custom event-driven engine |
| Frontend | Pygame / Web UI (TBD) |
| Data Storage | SQLite (local saves), JSON configs |
| Testing | pytest |
| Build & Package | Poetry |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND LAYER                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   Pages     │  │ Components  │  │   Static Assets         │  │
│  │  - Main     │  │  - Pipeline │  │  - Icons                │  │
│  │  - Build    │  │  - Nodes    │  │  - Animations           │  │
│  │  - Stats    │  │  - HUD      │  │  - Sprites              │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND LAYER                            │
│  ┌──────────────────────┐  ┌──────────────────────────────────┐ │
│  │       ENGINE         │  │          SIMULATION              │ │
│  │  ├─ Game Loop        │  │  ├─ Economy System               │ │
│  │  ├─ State Manager    │  │  ├─ Pipeline Simulator           │ │
│  │  ├─ Event System     │  │  ├─ Client/Contract Manager      │ │
│  │  └─ Save/Load        │  │  ├─ Employee Manager             │ │
│  │                      │  │  └─ Random Events                │ │
│  └──────────────────────┘  └──────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                        UTILS                              │   │
│  │  ├─ Config Loader    ├─ Logger    ├─ Math Helpers        │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Game Configs  │  │   Save Files    │  │  Level Data     │  │
│  │   (JSON/YAML)   │  │   (SQLite)      │  │  (JSON)         │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip or Poetry for dependency management
- A sense of humor about data pipelines

### Installation

```bash
# Clone the repo
git clone https://github.com/Pratiksha0713/ETL-builder-tycoon.git
cd ETL-builder-tycoon

# Set up virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run with debug mode
python main.py --debug
```

---

## Roadmap

### Phase 1 — Foundation (Current)
- [x] Project structure setup
- [ ] Core game loop implementation
- [ ] Basic pipeline node system
- [ ] Simple economy model
- [ ] Local save/load functionality

### Phase 2 — Playable Alpha
- [ ] Drag-and-drop pipeline builder
- [ ] 5+ data source types
- [ ] 10+ transformation nodes
- [ ] Client contract system
- [ ] Basic tutorial

### Phase 3 — Beta Features
- [ ] Employee management
- [ ] Tech debt mechanics
- [ ] Random event system
- [ ] Achievement system
- [ ] Sound effects & music

### Phase 4 — Polish & Release
- [ ] Full tutorial & onboarding
- [ ] Balance pass on economy
- [ ] Localization support
- [ ] Steam integration (maybe?)
- [ ] Mod support

---

## Project Structure

```
ETL-builder-tycoon/
├── backend/
│   ├── engine/        # Core game loop, state management
│   ├── simulation/    # Game mechanics, economy, events
│   └── utils/         # Helper functions, configs
├── frontend/
│   ├── components/    # Reusable UI elements
│   ├── pages/         # Game screens
│   └── static/
│       ├── icons/     # UI icons
│       └── animations/# Sprite animations
├── data/              # Game configs, level data
├── docs/              # Design docs, API specs
├── tests/             # Unit and integration tests
└── README.md
```

---

## Contributing

Contributions are welcome! Here's how to get involved:

### Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/cool-new-thing`)
3. Make your changes
4. Write tests if applicable
5. Run the test suite to make sure nothing broke
6. Commit with clear messages (`git commit -m "Add cool new thing"`)
7. Push and open a Pull Request

### Guidelines

- Keep PRs focused — one feature or fix per PR
- Follow existing code style (we'll add a linter config soon)
- Update docs if you're changing behavior
- Be nice in code reviews

### What We're Looking For

- Bug fixes (always appreciated)
- New pipeline node types
- UI/UX improvements
- Balance suggestions (the economy is probably broken)
- Documentation improvements
- Test coverage

### Not Sure Where to Start?

Check out issues labeled `good-first-issue` or `help-wanted`. Or just play the game and tell us what feels off.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Inspired by countless hours lost to Factorio and Shapez
- Built out of love (and mild frustration) for ETL pipelines
- Thanks to everyone who's ever debugged a production pipeline at 2 AM

---

*"Your data. Your pipelines. Your empire."*

