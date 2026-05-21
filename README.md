# Reactive and Predictive Container Migration

> **Research Project** — Supporting code repository for the published research paper on autonomous container migration orchestration using telemetry, monitoring, and LSTM-based predictive intelligence.

---

## Table of Contents

- [What is This Project?](#what-is-this-project)
- [Research Background](#research-background)
- [System Architecture Overview](#system-architecture-overview)
- [Repository Structure — Build It Part by Part](#repository-structure--build-it-part-by-part)
  - [Part 1 — Telemetry Application](#part-1--telemetry-application-this-repo)
  - [Part 2 — Docker API Wrapper](#part-2--docker-api-wrapper)
  - [Part 3 — Monitoring Application](#part-3--monitoring-application)
  - [Part 4 — LSTM Prediction Model](#part-4--lstm-prediction-model)
  - [Part 5 — Predict Migration Orchestrator](#part-5--predict-migration-orchestrator)
- [How to Work with This Repository](#how-to-work-with-this-repository)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Full System](#running-the-full-system)
- [Component Interaction Flow](#component-interaction-flow)
- [Technologies Used](#technologies-used)
- [Citation](#citation)

---

## What is This Project?

**MigrationOrchesTelemetry** is a distributed system that enables **autonomous, intelligent container migration** across a network of hosts. It combines two migration strategies:

- **Reactive Migration** — Triggers container migration when a host's resource utilisation breaches a predefined threshold (CPU, memory, network).
- **Predictive Migration** — Uses an LSTM (Long Short-Term Memory) neural network trained on historical telemetry data to *forecast* resource exhaustion before it happens, enabling proactive migration decisions.

The system continuously collects telemetry from all hosts in the network, stores it in a time-series database, analyses resource usage trends, and orchestrates live Docker container migration from over-utilised hosts to available ones — all without manual intervention.

---

## Research Background

This codebase was developed to support and validate the findings of the following research paper:

> **[Add your paper title here]**
> *[Author names] — Published in [Journal/Conference, Year]*
> DOI / Link: [Add DOI or link here]

The paper proposes a dual-strategy migration framework that outperforms purely reactive approaches by reducing service disruption through early predictive action. The code in these repositories implements the full pipeline described in the paper, from raw telemetry collection through to live container migration.

---

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Host Network                            │
│                                                                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐    │
│  │  Host A  │   │  Host B  │   │  Host C  │   │  Host N  │    │
│  │Telemetry │   │Telemetry │   │Telemetry │   │Telemetry │    │
│  │   App    │   │   App    │   │   App    │   │   App    │    │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘    │
│       └──────────────┴──────────────┴──────────────┘           │
│                              │                                  │
│                   ┌──────────▼──────────┐                       │
│                   │  Monitoring App     │                       │
│                   │  (AIOhttp + InfluxDB│                       │
│                   │   + Grafana)        │                       │
│                   └──────────┬──────────┘                       │
│                              │                                  │
│              ┌───────────────┴───────────────┐                  │
│              │                               │                  │
│   ┌──────────▼──────────┐     ┌─────────────▼──────────┐       │
│   │  Reactive Migration │     │  LSTM Prediction Model │       │
│   │  (Threshold-based)  │     │  (predictmigration)    │       │
│   └──────────┬──────────┘     └─────────────┬──────────┘       │
│              └───────────────┬───────────────┘                  │
│                   ┌──────────▼──────────┐                       │
│                   │  Migration          │                       │
│                   │  Orchestrator       │                       │
│                   │  (Docker API)       │                       │
│                   └─────────────────────┘                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Repository Structure — Build It Part by Part

The full system is split across five repositories, each representing a self-contained, incrementally buildable component. You can develop, test, and deploy each part independently before integrating the full pipeline.

---

### Part 1 — Telemetry Application *(This Repo)*

**Repository:** [`reactiveAndPredictiveMigration`](https://github.com/daisyLsbu/reactiveAndPredictiveMigration)

This is the **data collection layer**. A lightweight Python agent deployed on every host you want to monitor. It exposes an HTTP endpoint that the Monitoring Application polls to collect resource metrics.

**What it collects:**
- CPU, memory, disk, and network utilisation via `psutil`
- Per-container resource metrics via the Docker Stats API
- Round-Trip Time (RTT) to all other hosts in the network (used for migration destination selection)

**Key technologies:**
- Python
- `psutil` — system resource footprinting
- Docker Stats API — container-level resource data
- HTTP server (lightweight, designed for async polling)

**Deploy this on:** every host node in your network.

---

### Part 2 — Docker API Wrapper

**Repository:** [`dockerAPI`](https://github.com/daisyLsbu/dockerAPI)

A Python wrapper around the Docker Engine API that abstracts the low-level calls needed for container inspection and live migration. This module is used by the Migration Orchestrator to perform the actual container move between hosts.

**What it does:**
- Queries running containers and their resource snapshots
- Identifies containers eligible for migration based on resource thresholds
- Initiates container checkpoint, transfer, and restore across hosts
- Handles Docker API authentication and connection management

**Key technologies:**
- Python
- Docker SDK / Docker Engine REST API

---

### Part 3 — Monitoring Application

**Repository:** [`monitoringapplication`](https://github.com/daisyLsbu/monitoringapplication)

The **central data aggregation and storage layer**. This application runs continuously, polling the Telemetry Application on each host and persisting all metrics into a time-series database. The stored data feeds both the reactive migration logic and the LSTM model training/inference.

**What it does:**
- Reads a CSV file listing all hosts in the network
- Asynchronously polls each host's Telemetry App endpoint using `aiohttp`
- Writes all incoming data to InfluxDB (time-series format)
- Exposes data for visualisation via Grafana dashboards

**Key technologies:**
- Python
- `aiohttp` — asynchronous HTTP client for concurrent host polling
- InfluxDB — time-series storage
- Grafana — visualisation and dashboarding (optional but recommended)

**Configuration:** provide a `hosts.csv` file listing the IP/hostname of every node to monitor.

---

### Part 4 — LSTM Prediction Model

**Repository:** [`LSTM`](https://github.com/daisyLsbu/LSTM)

The **machine learning component**. Trains and runs an LSTM neural network on the historical time-series telemetry data collected by the Monitoring Application to predict future resource utilisation.

**What it does:**
- Reads historical resource data from InfluxDB
- Trains a sequential LSTM model to forecast CPU/memory utilisation over a future time window
- Outputs predictions used by the Predictive Migration Orchestrator to make proactive migration decisions
- Can be retrained periodically as new telemetry data accumulates

**Key technologies:**
- Python
- TensorFlow / Keras (LSTM model)
- InfluxDB client (data ingestion for training)
- NumPy / Pandas (data preprocessing)

---

### Part 5 — Predict Migration Orchestrator

**Repository:** [`predictmigration`](https://github.com/daisyLsbu/predictmigration)

The **decision and execution layer** — the brain of the system. Combines reactive threshold monitoring with LSTM-based forecasts to decide *when* and *where* to migrate containers, then executes the migration.

**What it does:**
- Reads a rolling moving average of host metrics from InfluxDB
- Converts multi-dimensional resource utilisation into a scalar score
- Compares against preset thresholds for reactive triggers
- Reads LSTM forecasts for predictive triggers
- Identifies source containers to migrate (based on Docker stats)
- Identifies destination hosts (based on available resources + RTT)
- Selects the best destination using transmission time from the Telemetry App RTT data
- Invokes the Docker API wrapper to perform the live migration

**Key technologies:**
- Python
- InfluxDB client
- Docker API (via `dockerAPI` module)

---

## How to Work with This Repository

### Prerequisites

Ensure the following are installed on all nodes:

- **Python 3.8+**
- **Docker Engine** (with API access enabled)
- **InfluxDB** (accessible from the Monitoring Application node)
- **Grafana** *(optional, for dashboards)*

---

### Installation

Clone this repository (Telemetry Application) on **each host** you want to monitor:

```bash
git clone https://github.com/daisyLsbu/reactiveAndPredictiveMigration.git
cd reactiveAndPredictiveMigration
pip install -r requirements.txt
```

For the other components, clone each sub-repository on the **central monitoring/orchestration node**:

```bash
git clone https://github.com/daisyLsbu/dockerAPI.git
git clone https://github.com/daisyLsbu/monitoringapplication.git
git clone https://github.com/daisyLsbu/LSTM.git
git clone https://github.com/daisyLsbu/predictmigration.git
```

---

### Configuration

**1. Hosts file** (Monitoring Application)

Create a `hosts.csv` in the `monitoringapplication` directory listing all monitored hosts:

```csv
hostname,ip_address
host-a,192.168.1.10
host-b,192.168.1.11
host-c,192.168.1.12
```

**2. InfluxDB connection**

Set your InfluxDB connection details in the monitoring and prediction config files (refer to each repository for the specific config file format).

**3. Thresholds**

Edit the threshold values in the `predictmigration` configuration to define what constitutes an over-utilised host (e.g. CPU > 80%, memory > 85%).

---

### Running the Full System

Follow this order when starting up:

**Step 1 — Start the Telemetry Application on each host:**
```bash
# On every host node
cd reactiveAndPredictiveMigration
python telemetry_app.py
```

**Step 2 — Start the Monitoring Application on the central node:**
```bash
cd monitoringapplication
python monitoring_app.py
```
This will begin polling all hosts and writing to InfluxDB.

**Step 3 — Train the LSTM model** *(run once, then periodically retrain):*
```bash
cd LSTM
python train.py
```

**Step 4 — Start the Migration Orchestrator:**
```bash
cd predictmigration
python orchestrator.py
```

The orchestrator will now continuously evaluate host utilisation and trigger reactive or predictive migration as needed.

---

## Component Interaction Flow

```
Hosts (Telemetry App)
        │
        │  HTTP polling (aiohttp)
        ▼
Monitoring App  ──────────►  InfluxDB
                                │
                ┌───────────────┤
                │               │
                ▼               ▼
          Reactive          LSTM Model
          Threshold         (predictmigration)
          Check
                │               │
                └───────┬───────┘
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

| Component | Language | Key Libraries / Tools |
|---|---|---|
| Telemetry App | Python | `psutil`, Docker Stats API |
| Docker API Wrapper | Python | Docker SDK |
| Monitoring App | Python | `aiohttp`, InfluxDB, Grafana |
| LSTM Model | Python | TensorFlow/Keras, Pandas, NumPy |
| Migration Orchestrator | Python | InfluxDB client, Docker API |

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

*For questions or issues, please open a GitHub issue in the relevant repository.*
