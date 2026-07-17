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

## Running the Full System

The system runs across two branches. The telemetry branch must be running on every host node before starting the monitor branch on the central orchestration node.


# Before You Start

Ensure the following are in place across your network:


InfluxDB is installed and running on the orchestration node
Grafana is installed on the orchestration node (optional but recommended)
SSH access is configured from the orchestration node to all host nodes (required for container image transfer during migration)
All host nodes are reachable over the network (the orchestration node will poll them via HTTP)
Trained LSTM model file is available from LSTMSetup and placed in the predictive migration directory


Step 1 — Configure and launch the Telemetry Application on every host node

(Branch: telemetry — run this on each machine you want to monitor)

1a. Update the host list

In the Telemetry/ directory, ensure the host list file includes the IP addresses of all other nodes in the network. This is used by the RTT measurement component.

1b. Run via the launch script

git checkout telemetry
cd Telemetry/scripts
bash launch.sh

launch.sh runs the following three scripts in order:

ScriptWhat it doessetup.shInstalls dependencies (psutil, ping, Docker SDK) and configures the environmentbuild.shPrepares the applicationrun.shStarts the telemetry server with python app.py <port> (default port: 5000)

1c. Verify it is running

Once started, the Telemetry Application exposes the following HTTP endpoints on each host:

EndpointReturns/devicedetailsHost-level CPU, memory, disk, network metrics/containersPer-container Docker resource metrics/combinedCombined host and container metrics/rttRound-trip time to other hosts (pass host list in request body)

Open http://<host-ip>:5000/devicedetails in a browser to confirm the application is live before proceeding.

1d. Setup Docker and containers

Run dockersetup.sh to set up containers. Repeat the container creation commands to create multiple containers.


Repeat this step on every host node in the network.


Step 2 — Configure and launch the Monitoring Application and Migration Orchestrator on the orchestration node

(Branch: monitor — run this once on the central node)

2a. Update the host list

Edit Monitor/data/host.csv to list every host node in your network:

hostname,ip_address
host-a,192.168.1.10
host-b,192.168.1.11
host-c,192.168.1.12

2b. Update InfluxDB credentials

Open Monitor/influxdbsuite.py and set your InfluxDB connection details (host, port, database name, and credentials).

2c. Run via the launch script

git checkout monitor
cd Monitor/scripts
bash launch.sh

launch.sh runs the following three scripts in order:

ScriptWhat it doessetup.shInstalls dependencies (aiohttp, InfluxDB client, Docker SDK) and validates the InfluxDB connectionbuild.shPrepares the monitoring environment and validates the host listrun.shStarts the Monitoring Application (begins polling all hosts and writing to InfluxDB), then starts the Migration Orchestrator (migrationAgent.py) which continuously evaluates resource utilisation and triggers migration when thresholds are breached

Step 3 — Train and deploy the LSTM model (predictive migration)

Follow the full setup and training steps in LSTMSetup to generate the trained model file. Once trained, place the model file in the predictive migration directory as instructed in that repository, then start the predictive orchestrator:

cd predictmigration
python orchestrator.py

Step 4 — Verify the system is running end to end

Once all components are running:

InfluxDB should be receiving time-series data for all hosts. Query your InfluxDB instance or open Grafana to confirm data is flowing.
Orchestration logs from migrationAgent.py will show threshold evaluations and any migration decisions being made.
When a migration is triggered, connectRemote.py handles the SSH-based transfer of the container image from the source host to the destination host, followed by container restore on the destination.

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
