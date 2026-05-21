# Reactive and Predictive Container Migration

> **Research Project** — Supporting code for the published research paper on autonomous container migration orchestration using telemetry, monitoring, and LSTM-based predictive intelligence.

---

## Table of Contents

- [What is This Project?](#what-is-this-project)
- [Research Background](#research-background)
- [System Architecture Overview](#system-architecture-overview)
- [Repository Structure — Two Branches, Two Stages](#repository-structure--two-branches-two-stages)
  - [Branch 1 — `telemetry` (Data Collection Layer)](#branch-1--telemetry-data-collection-layer)
    - [Part 1 — Telemetry Application](#part-1--telemetry-application)
    - [Part 2 — Docker API Wrapper](#part-2--docker-api-wrapper)
  - [Branch 2 — `main` (Monitoring, Intelligence & Orchestration)](#branch-2--main-monitoring-intelligence--orchestration)
    - [Part 3 — Monitoring Application](#part-3--monitoring-application)
    - [Part 4 — LSTM Prediction Model](#part-4--lstm-prediction-model)
    - [Part 5 — Migration Orchestrator](#part-5--migration-orchestrator)
- [How to Work with This Repository](#how-to-work-with-this-repository)
  - [Prerequisites](#prerequisites)
  - [Setup — Telemetry Branch](#setup--telemetry-branch)
  - [Setup — Main Branch](#setup--main-branch)
  - [Configuration](#configuration)
  - [Running the Full System](#running-the-full-system)
- [Component Interaction Flow](#component-interaction-flow)
- [Technologies Used](#technologies-used)
- [Citation](#citation)

---

## What is This Project?

**MigrationOrchesTelemetry** is a distributed system that enables **autonomous, intelligent container migration** across a network of hosts. It combines two complementary migration strategies:

- **Reactive Migration** — Triggers container relocation when a host's resource utilisation breaches a predefined threshold (CPU, memory, network).
- **Predictive Migration** — Uses an LSTM (Long Short-Term Memory) neural network trained on historical telemetry to *forecast* resource exhaustion before it happens, enabling proactive migration decisions.

The system continuously collects telemetry from all hosts in the network, stores it in a time-series database, analyses resource usage trends, and orchestrates live Docker container migration from over-utilised hosts to available ones — all without manual intervention.

---

## Research Background

This codebase was developed to support and validate the findings of the following research paper:

> **[Add your paper title here]**
> *[Author names] — Published in [Journal/Conference, Year]*
> DOI / Link: [Add DOI or link here]

The paper proposes a dual-strategy migration framework that outperforms purely reactive approaches by reducing service disruption through early predictive action. The code in this repository implements the full pipeline described in the paper, from raw telemetry collection through to live container migration.

---

## System Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                          Host Network                            │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  Host A  │  │  Host B  │  │  Host C  │  │  Host N  │        │
│  │Telemetry │  │Telemetry │  │Telemetry │  │Telemetry │        │
│  │   App    │  │   App    │  │   App    │  │   App    │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       └─────────────┴─────────────┴─────────────┘               │
│  [telemetry branch]          │                                   │
│                              │  HTTP polling (aiohttp)           │
│  ════════════════════════════╪════════════════════════════════   │
│  [main branch]               │                                   │
│                   ┌──────────▼──────────┐                        │
│                   │  Monitoring App     │                        │
│                   │  (aiohttp + InfluxDB│                        │
│                   │   + Grafana)        │                        │
│                   └──────────┬──────────┘                        │
│                              │                                   │
│              ┌───────────────┴──────────────┐                    │
│              │                              │                    │
│   ┌──────────▼──────────┐    ┌─────────────▼──────────┐         │
│   │  Reactive Threshold │    │  LSTM Prediction Model │         │
│   │  Check              │    │                        │         │
│   └──────────┬──────────┘    └─────────────┬──────────┘         │
│              └──────────────┬───────────────┘                    │
│                   ┌─────────▼───────────┐                        │
│                   │  Migration          │                        │
│                   │  Orchestrator       │                        │
│                   │  (Docker API)       │                        │
│                   └─────────────────────┘                        │
└──────────────────────────────────────────────────────────────────┘
```

---

## Repository Structure — Two Branches, Two Stages

This project lives in a **single repository** organised across **two branches**, each representing a self-contained stage of the system. You develop and deploy them in order.

```
reactiveAndPredictiveMigration/
├── branch: telemetry   ← Stage 1: deploy on every host node
│   ├── Part 1 — Telemetry Application
│   └── Part 2 — Docker API Wrapper
│
└── branch: main        ← Stage 2: deploy on the central orchestration node
    ├── Part 3 — Monitoring Application
    ├── Part 4 — LSTM Prediction Model
    └── Part 5 — Migration Orchestrator
```

---

### Branch 1 — `telemetry` (Data Collection Layer)

Switch to this branch to work on the host-side data collection components:

```bash
git checkout telemetry
```

---

#### Part 1 — Telemetry Application

A lightweight Python agent deployed on **every host** you want to monitor. It exposes an HTTP endpoint that the Monitoring Application polls to collect resource metrics.

**What it collects:**
- CPU, memory, disk, and network utilisation via `psutil`
- Per-container resource metrics via the Docker Stats API
- Round-Trip Time (RTT) to all other hosts in the network (used later for migration destination selection)

**Key technologies:**
- Python, `psutil`, Docker Stats API
- Lightweight HTTP server (designed for concurrent async polling)

**Deploy this on:** every node in your network.

---

#### Part 2 — Docker API Wrapper

A Python module that wraps the Docker Engine API to abstract the low-level calls needed for container inspection and live migration. This is consumed by the Migration Orchestrator in the `main` branch.

**What it does:**
- Queries running containers and their resource snapshots
- Identifies containers eligible for migration based on resource thresholds
- Initiates container checkpoint, transfer, and restore across hosts
- Handles Docker API authentication and connection management

**Key technologies:**
- Python, Docker SDK / Docker Engine REST API

---

### Branch 2 — `main` (Monitoring, Intelligence & Orchestration)

Switch to this branch to work on the central coordination components:

```bash
git checkout main
```

This branch contains three tightly coupled components that together form the intelligence and decision layer of the system.

---

#### Part 3 — Monitoring Application

The **central data aggregation and storage layer**. Runs continuously on the orchestration node, polling all host Telemetry Apps and persisting metrics into InfluxDB.

**What it does:**
- Reads a CSV file listing all hosts in the network
- Asynchronously polls each host's Telemetry App using `aiohttp`
- Writes all incoming time-series data to InfluxDB
- Data is explorable and visualisable via Grafana dashboards

**Key technologies:**
- Python, `aiohttp`, InfluxDB, Grafana (optional)

---

#### Part 4 — LSTM Prediction Model

The **machine learning component**. Trains an LSTM neural network on historical telemetry data to forecast future resource utilisation per host.

**What it does:**
- Reads historical resource data from InfluxDB
- Trains a sequential LSTM model to predict CPU/memory utilisation over a configurable future window
- Generates forecasts consumed by the Migration Orchestrator for predictive triggers
- Supports periodic retraining as new telemetry accumulates

**Key technologies:**
- Python, TensorFlow / Keras, NumPy, Pandas, InfluxDB client

---

#### Part 5 — Migration Orchestrator

The **decision and execution layer** — the brain of the system. Combines reactive threshold monitoring with LSTM-based forecasts to decide when and where to migrate containers, then executes the migration via the Docker API.

**What it does:**
- Reads a rolling moving average of host metrics from InfluxDB
- Converts multi-dimensional resource utilisation into a comparable scalar score
- **Reactive path:** compares the scalar score against preset thresholds
- **Predictive path:** reads LSTM forecasts and triggers migration ahead of a predicted breach
- Identifies which containers on the source host should migrate
- Identifies candidate destination hosts based on available resources
- Selects the optimal destination using RTT data from the Telemetry App
- Invokes the Docker API Wrapper (from the `telemetry` branch) to perform the live migration

**Key technologies:**
- Python, InfluxDB client, Docker API wrapper

---

## How to Work with This Repository

### Prerequisites

Ensure the following are installed:

| Requirement | Where needed |
|---|---|
| Python 3.8+ | All nodes |
| Docker Engine (API enabled) | All nodes |
| InfluxDB | Orchestration node |
| Grafana *(optional)* | Orchestration node |

---

### Setup — Telemetry Branch

Clone the repository and check out the `telemetry` branch on **each host node** you want to monitor:

```bash
git clone https://github.com/daisyLsbu/reactiveAndPredictiveMigration.git
cd reactiveAndPredictiveMigration
git checkout telemetry
pip install -r requirements.txt
```

---

### Setup — Main Branch

On your **central orchestration node**, use the `main` branch:

```bash
git clone https://github.com/daisyLsbu/reactiveAndPredictiveMigration.git
cd reactiveAndPredictiveMigration
# main is the default, no checkout needed
pip install -r requirements.txt
```

---

### Configuration

**1. Hosts file** — create a `hosts.csv` in the project root listing all monitored nodes:

```csv
hostname,ip_address
host-a,192.168.1.10
host-b,192.168.1.11
host-c,192.168.1.12
```

**2. InfluxDB connection** — set your InfluxDB host, port, database name, and credentials in the monitoring config file.

**3. Thresholds** — edit the threshold values in the orchestrator config to define what constitutes an over-utilised host (e.g. CPU > 80%, memory > 85%).

---

### Running the Full System

Start components in this order:

**Step 1 — On every host node** (telemetry branch):
```bash
python telemetry_app.py
```

**Step 2 — On the orchestration node**, start the Monitoring Application (main branch):
```bash
python monitoring_app.py
```
This begins polling all hosts and writing data to InfluxDB.

**Step 3 — Train the LSTM model** *(run once initially, retrain periodically):*
```bash
python train_lstm.py
```

**Step 4 — Start the Migration Orchestrator:**
```bash
python orchestrator.py
```

The orchestrator now runs continuously, evaluating host utilisation and triggering reactive or predictive migration as needed.

---

## Component Interaction Flow

```
[telemetry branch — each host]
  Telemetry App  +  Docker API Wrapper
        │
        │  HTTP polling (aiohttp)
        ▼
[main branch — orchestration node]
  Monitoring App  ──────────────►  InfluxDB
                                       │
                     ┌─────────────────┤
                     │                 │
                     ▼                 ▼
               Reactive            LSTM Model
               Threshold           Forecast
               Check
                     │                 │
                     └────────┬────────┘
                              │
                              ▼
                    Migration Decision
                              │
                              ▼
                    Docker API Wrapper
                              │
                              ▼
                    Live Container Migration
                    (source host → destination host)
```

---

## Technologies Used

| Component | Branch | Language | Key Libraries / Tools |
|---|---|---|---|
| Telemetry Application | `telemetry` | Python | `psutil`, Docker Stats API |
| Docker API Wrapper | `telemetry` | Python | Docker SDK |
| Monitoring Application | `main` | Python | `aiohttp`, InfluxDB, Grafana |
| LSTM Prediction Model | `main` | Python | TensorFlow/Keras, Pandas, NumPy |
| Migration Orchestrator | `main` | Python | InfluxDB client, Docker API |

---

## Citation

If you use this code in your research, please cite the original paper:

```bibtex
@article{[citation_key],
  title   = {[Paper Title]},
  author  = {[Authors]},
  journal = {[Journal/Conference]},
  year    = {[Year]},
  doi     = {[DOI]}
}
```

---

*For questions or issues, please open a GitHub issue on this repository.*
