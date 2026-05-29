# Reactive and Predictive Container Migration

> **Research Project** — Supporting code for the published research paper on autonomous container migration orchestration using telemetry, monitoring, and LSTM-based predictive intelligence.

---

## Table of Contents

- [What is This Project?](#what-is-this-project)
- [Research Background](#research-background)
- [System Architecture Overview](#system-architecture-overview)
- [How This Work Was Built — Incremental Development](#how-this-work-was-built--incremental-development)
- [Repository Branches](#repository-branches)
  - [Branch: `telemetry`](#branch-telemetry)
  - [Branch: `main`](#branch-monitor)
- [How to Run the Project](#how-to-run-the-project)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Running the `telemetry` Branch](#running-the-telemetry-branch)
  - [Running the `monitor` Branch](#running-the-main-branch)
- [Component Interaction Flow](#component-interaction-flow)
- [Technologies Used](#technologies-used)
- [Citation](#citation)

---

## What is This Project?

**reactiveAndPredictiveMigration** is a distributed system that enables **autonomous, intelligent container migration** across a network of hosts. It combines two complementary migration strategies:

- **Reactive Migration** — Triggers container relocation when a host's resource utilisation breaches a predefined threshold (CPU, memory, network).
- **Predictive Migration** — Uses an LSTM (Long Short-Term Memory) neural network trained on historical telemetry to *forecast* resource exhaustion before it happens, enabling proactive migration decisions.

The system continuously collects telemetry from all hosts in the network, stores it in a time-series database, analyses resource usage trends, and orchestrates live Docker container migration from over-utilised hosts to available ones — all without manual intervention.

---

## Research Background

This codebase was developed to support and validate the findings of the following research paper:

> **Reactive vs Predictive Live Migration in Edge Cloud**
> *Daisy Rani — Published in ICC 2024 - IEEE International, 2024*
> DOI: 10.1109/ICC51166.2024.10622687
> Link: [IEEE paper link](https://ieeexplore.ieee.org/document/10622687) 

The paper proposes a dual-strategy migration framework that outperforms purely reactive approaches by reducing service disruption through early predictive action. The code in this repository implements the full pipeline described in the paper — from raw telemetry collection through to live container migration.

---

## System Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                          Host Network                            │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │  Host A  │  │  Host B  │  │  Host C  │  │  Host N  │          │
│  │Telemetry │  │Telemetry │  │Telemetry │  │Telemetry │          │
│  │   App    │  │   App    │  │   App    │  │   App    │          │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│       └─────────────┴─────────────┴─────────────┘                │
│  ── branch: telemetry ──────────  │  ──────────────────────────  │
│                                   │  HTTP polling (aiohttp)      │
│  ── branch: main ─────────────────┼────────────────────────────  │
│                        ┌──────────▼──────────┐                   │
│                        │  Monitoring App     │                   │
│                        │  (aiohttp + InfluxDB│                   │
│                        │   + Grafana)        │                   │
│                        └──────────┬──────────┘                   │
│                                   │                              │
│               ┌───────────────────┴──────────────┐               │
│               │                                  │               │
│  ┌────────────▼────────────┐   ┌─────────────────▼──────────┐    │
│  │  Reactive Threshold     │   │  LSTM Prediction Model     │    │
│  │  Check                  │   │                            │    │
│  └────────────┬────────────┘   └─────────────────┬──────────┘    │
│               └──────────────┬───────────────────┘               │
│                    ┌─────────▼──────────┐                        │
│                    │  Migration         │                        │
│                    │  Orchestrator      │                        │
│                    │  (Docker API)      │                        │
│                    └────────────────────┘                        │
└──────────────────────────────────────────────────────────────────┘
```

---

## How This Work Was Built — Incremental Development

This project was developed incrementally, with each functional component built and validated independently before being integrated into the two branches of this repository. If you are interested in understanding or extending any individual component in isolation, standalone repositories exist for each one under the same GitHub account:

| Component | Standalone Repository | What it explores |
|---|---|---|
| Telemetry collection | [`TelemetryApplication`](https://github.com/daisyLsbu/TelemetryApplication) | Host footprinting |
| Docker stats | [`DockerAPI`](https://github.com/daisyLsbu/dockerAPIs) | Docker Stats API, RTT measurement |
| Time-series monitoring + storage | [`monitoringapplication`](https://github.com/daisyLsbu/monitoringapplication) | Async polling, InfluxDB ingestion, Grafana dashboards |
| LSTM model for resource forecasting | [`LSTM`](https://github.com/daisyLsbu/LSTM) | Model training, time-series preprocessing, forecasting |
| Reactive migration logic | [`Reactive Migration logic`](https://github.com/daisyLsbu/MigrationOrchestrator) | Threshold evaluation, destination selection, orchestration |

These repositories represent the research and development progression described in the paper. The consolidated, deployable version of the full system is what lives in the two branches of this repository.

---

## Repository Branches

This repository is organised into **two branches**, each deployable on a different class of node in the network.

```
reactiveAndPredictiveMigration/
│
├── branch: telemetry  ──  deployed on every monitored host node
│
└── branch: monitor      ──  deployed on the central orchestration node
```

---

### Branch: `telemetry`

**Deploy on:** every host node you want to monitor and migrate containers from/to.

```bash
git checkout telemetry
```

This branch contains the **data collection layer** of the system. It runs two components together:

**Telemetry Application** — a lightweight HTTP server that continuously collects and exposes resource metrics for this host. It reports:
- CPU, memory, disk, and network utilisation (via `psutil`)
- Per-container resource usage (via Docker Stats API)
- Round-Trip Time (RTT) to all other nodes in the network

**Docker API Wrapper** — a Python module that abstracts Docker Engine API calls for container inspection and live migration operations. It is used by the orchestrator in the `main` branch to execute migrations remotely.

> *Standalone development repositories for these components: [`dockerAPI`](https://github.com/daisyLsbu/dockerAPI)*

---

### Branch: `monitor`

**Deploy on:** the central orchestration node (one instance per network).

```bash
git checkout monitor
```

This branch contains the **monitoring, intelligence, and orchestration layer** — three components that work together as a single cohesive system:

**Monitoring Application** — runs continuously, asynchronously polling every host's Telemetry App and writing all metrics into InfluxDB for time-series storage and optional Grafana visualisation.

**Migration Orchestrator** — the decision engine. It reads a rolling moving average of resource metrics from InfluxDB, converts them to a comparable scalar, and evaluates two triggers:
- **Reactive:** current utilisation exceeds the configured threshold → migrate now
- **Predictive:** LSTM forecast indicates an upcoming breach → migrate before it occurs

Once a migration is triggered, the orchestrator selects the source container (by Docker resource usage) and the best destination host (by available resources and RTT), then invokes the Docker API Wrapper on the `telemetry` branch to execute the live migration.

> *Standalone development repositories for these components: Refer above

---

## How to Run the Project

### Prerequisites

| Requirement | Where needed |
|---|---|
| Python 3.8+ | All nodes |
| Docker Engine (API enabled) | All nodes |
| InfluxDB | Orchestration node |
| Grafana *(optional)* | Orchestration node |

---

### Clone the Repository

```bash
git clone https://github.com/daisyLsbu/reactiveAndPredictiveMigration.git
cd reactiveAndPredictiveMigration
```

---

### Running the `telemetry` Branch

Run this on **every host node** you want to monitor:

```bash
git checkout telemetry
bash scripts/launch.sh
```

`launch.sh` runs the following scripts in order:

```
scripts/
├── setup.sh   — installs dependencies and configures the environment
├── build.sh   — builds and prepares the application
└── run.sh     — starts the telemetry server and Docker API wrapper
```

Once running, this node will be reachable by the Monitoring Application for data collection, and by the Orchestrator for migration operations.

---

### Running the `main` Branch

Run this on your **central orchestration node**:

```bash
git checkout main
bash scripts/launch.sh
```

`launch.sh` runs the following scripts in order:

```
scripts/
├── setup.sh   — installs dependencies, sets up InfluxDB connection and host list
├── build.sh   — prepares the LSTM model environment and builds required components
└── run.sh     — starts the Monitoring Application, trains/loads the LSTM model,
                 and launches the Migration Orchestrator
```

**Start the `telemetry` branch on all host nodes before starting this branch**, so data collection is active when the Monitoring Application begins polling.

---

### Configuration

Before running either branch, review the configuration in each:

**Hosts file** — provide a `hosts.csv` listing every node to monitor:
```csv
hostname,ip_address
host-a,192.168.1.10
host-b,192.168.1.11
host-c,192.168.1.12
```

**InfluxDB** — set your InfluxDB host, port, and database name in the config file (see `setup.sh` for the expected variables).

**Thresholds** — edit the migration threshold values in the orchestrator config to suit your environment (e.g. trigger migration when CPU > 80% or memory > 85%).

---

## Component Interaction Flow

```
[branch: telemetry — runs on each host]

   Telemetry App  +  Docker API Wrapper
          │
          │  HTTP polling (aiohttp)
          ▼

[branch: main — runs on orchestration node]

   Monitoring App  ──────────────►  InfluxDB
                                        │
                      ┌─────────────────┤
                      │                 │
                      ▼                 ▼
                Reactive            LSTM Forecast
                Threshold
                      │                 │
                      └────────┬────────┘
                               │
                               ▼
                     Migration Decision
                               │
                               ▼
              Docker API Wrapper (telemetry branch)
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
| LSTM Prediction Model | `main` | Python | TensorFlow / Keras, Pandas, NumPy |
| Migration Orchestrator | `main` | Python | InfluxDB client, Docker API |

---

## Citation

If you use this code in your research, please cite the original paper:

```bibtex
@article{[citation_key],
  title   = {Reactive vs Predictive Live Migration in Edge Cloud},
  author  = {Daisy Rani, Saptarshi Ghosh, Tasos Dagiuklas},
  journal = {ICC 2024 - IEEE International Conference on Communications},
  year    = {2024},
  doi     = {10.1109/ICC51166.2024.10622687}
}
```

---

*For questions or issues, please open a GitHub issue on this repository.*
