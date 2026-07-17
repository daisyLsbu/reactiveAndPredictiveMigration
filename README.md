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
- [Components](#components)
- [How to Run the Project](#how-to-run-the-project)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Before You Start](#before-you-start)
  - [Step 1 — Telemetry Application](#step-1--configure-and-launch-the-telemetry-application-on-every-host-node)
  - [Step 2 — Monitoring Application & Orchestrator](#step-2--configure-and-launch-the-monitoring-application-and-migration-orchestrator-on-the-orchestration-node)
  - [Step 3 — LSTM Model](#step-3--train-and-deploy-the-lstm-model-predictive-migration)
  - [Step 4 — Verify End to End](#step-4--verify-the-system-is-running-end-to-end)
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
└── branch: main       ──  deployed on the central orchestration node
```

---

## Components

### TelemetryApplication

Application to get the telemetry information, developed in Python.

- `psutil` library for system resource information for foot-printing application
- Docker Stats API for the resources related to all the containers
- RTT data between the application host and the list of other hosts in the network

> **Deploy this on:** every node in your network.

---

### MonitoringApplication

The application runs continuously monitoring and storing data related to the hosts in the network.

- Collects telemetry data from all the hosts in the network and stores in InfluxDB
- Developed in Python; list of hosts is provided in a CSV file
- AIOhttp for Asynchronous HTTP Client/Server communication with the hosts
- Timeseries InfluxDB is used to store the data for all hosts, which can be used to plot and analyse using Grafana

---

### MigrationOrchestrator

Orchestrates the migration of containers from the over-utilised host to a resource available host in the network.

- The data stored in time-series InfluxDB is read continuously in a moving average for each of the hosts in the network
- The resource utilisation is converted to scalar and compared to the preset threshold
- For the over-utilised hosts, its docker data is checked to identify the container/s to be migrated
- The available resources in the network is checked to identify the destination host/s
- The transmission time from the source host to destination hosts are checked to select the destination host
- Docker is used to host the containers; Docker APIs are used to aid migration from source to destination host

---

### MAMD — Moving Average Migration Decision

- Applies a rolling moving average over historical telemetry data before comparing against thresholds
- Smooths short-term resource spikes to prevent unnecessary migrations caused by transient load bursts
- Configurable moving average window size to tune sensitivity
- Feeds the smoothed utilisation value into the reactive threshold comparison in the Migration Orchestrator

---

### Predictive Migration (LSTM)

- Uses an LSTM neural network trained in [LSTMSetup](https://github.com/daisyLsbu/LSTMSetup) to forecast future CPU and memory utilisation
- Triggers proactive container migration when predicted utilisation is forecast to exceed a threshold within the forecast horizon — before the threshold is actually breached
- Reads historical time-series data from InfluxDB for model input
- The trained model file must be obtained from [LSTMSetup](https://github.com/daisyLsbu/LSTMSetup) before running this component

**Key technologies:** Python, TensorFlow / Keras, InfluxDB client, Docker API

---

## How to Run the Project

### Prerequisites

Ensure the following are installed on all relevant nodes:

- **Python 3.8+**
- **Docker Engine** (with API access enabled)
- **InfluxDB** (accessible from the Monitoring Application node)
- **Grafana** *(optional, for dashboards)*
- **TensorFlow / Keras** *(required on the orchestration node for predictive migration)*
- Trained LSTM model from [LSTMSetup](https://github.com/daisyLsbu/LSTMSetup) *(required for predictive migration)*

---

### Installation

Clone the repository on **each host** you want to monitor (telemetry branch):

```bash
git clone https://github.com/daisyLsbu/reactiveAndPredictiveMigration.git
cd reactiveAndPredictiveMigration
pip install -r requirements.txt
```

Clone the repository on the **central monitoring/orchestration node** (main branch):

```bash
git clone https://github.com/daisyLsbu/reactiveAndPredictiveMigration.git
cd reactiveAndPredictiveMigration
pip install -r requirements.txt
```

---

### Before You Start

Ensure the following are in place across your network:

- InfluxDB is installed and running on the orchestration node
- Grafana is installed on the orchestration node *(optional but recommended)*
- SSH access is configured from the orchestration node to all host nodes (required for container image transfer during migration)
- All host nodes are reachable over the network (the orchestration node will poll them via HTTP)
- Trained LSTM model file is available from [LSTMSetup](https://github.com/daisyLsbu/LSTMSetup) and placed in the predictive migration directory

---

### Step 1 — Configure and launch the Telemetry Application on every host node

*(Branch: `telemetry` — run this on each machine you want to monitor)*

**1a. Update the host list**

In the `Telemetry/` directory, ensure the host list file includes the IP addresses of all other nodes in the network. This is used by the RTT measurement component.

**1b. Run via the launch script**

```bash
git checkout telemetry
cd Telemetry/scripts
bash launch.sh
```

`launch.sh` runs the following three scripts in order:

| Script | What it does |
|---|---|
| `setup.sh` | Installs dependencies (`psutil`, `ping`, Docker SDK) and configures the environment |
| `build.sh` | Prepares the application |
| `run.sh` | Starts the telemetry server with `python app.py <port>` (default port: `5000`) |

**1c. Verify it is running**

Once started, the Telemetry Application exposes the following HTTP endpoints on each host:

| Endpoint | Returns |
|---|---|
| `/devicedetails` | Host-level CPU, memory, disk, network metrics |
| `/containers` | Per-container Docker resource metrics |
| `/combined` | Combined host and container metrics |
| `/rtt` | Round-trip time to other hosts (pass host list in request body) |

Open `http://<host-ip>:5000/devicedetails` in a browser to confirm the application is live before proceeding.

**1d. Setup Docker and containers**

Run `dockersetup.sh` to set up containers. Repeat the container creation commands to create multiple containers.

> Repeat this step on every host node in the network.

---

### Step 2 — Configure and launch the Monitoring Application and Migration Orchestrator on the orchestration node

*(Branch: `main` — run this once on the central node)*

**2a. Update the host list**

Edit `Monitor/data/host.csv` to list every host node in your network:

```csv
hostname,ip_address
host-a,192.168.1.10
host-b,192.168.1.11
host-c,192.168.1.12
```

**2b. Update InfluxDB credentials**

Open `Monitor/influxdbsuite.py` and set your InfluxDB connection details (host, port, database name, and credentials).

**2c. Run via the launch script**

```bash
git checkout main
cd Monitor/scripts
bash launch.sh
```

`launch.sh` runs the following three scripts in order:

| Script | What it does |
|---|---|
| `setup.sh` | Installs dependencies (`aiohttp`, InfluxDB client, Docker SDK) and validates the InfluxDB connection |
| `build.sh` | Prepares the monitoring environment and validates the host list |
| `run.sh` | Starts the Monitoring Application (begins polling all hosts and writing to InfluxDB), then starts the Migration Orchestrator (`migrationAgent.py`) which continuously evaluates resource utilisation and triggers migration when thresholds are breached |

---

### Step 3 — Train and deploy the LSTM model (predictive migration)

Follow the full setup and training steps in [LSTMSetup](https://github.com/daisyLsbu/LSTMSetup) to generate the trained model file. Once trained, place the model file in the predictive migration directory as instructed in that repository, then start the predictive orchestrator:

```bash
cd predictmigration
python orchestrator.py
```

---

### Step 4 — Verify the system is running end to end

Once all components are running:

- **InfluxDB** should be receiving time-series data for all hosts. Query your InfluxDB instance or open Grafana to confirm data is flowing.
- **Orchestration logs** from `migrationAgent.py` will show threshold evaluations and any migration decisions being made.
- When a migration is triggered, `connectRemote.py` handles the SSH-based transfer of the container image from the source host to the destination host, followed by container restore on the destination.

### Startup Order Summary

```
1. [ All host nodes ]     git checkout telemetry  →  bash Telemetry/scripts/launch.sh
2. [ Orchestration node ] git checkout main        →  bash Monitor/scripts/launch.sh
3. [ Orchestration node ] cd predictmigration      →  python orchestrator.py
```

> **⚠️ Important:** If the Monitoring Application starts before the Telemetry Applications are running, it will fail to poll the hosts. Always start Step 1 first.

Check the individual repository for each section and the troubleshoot section for each one of them in case you cannot make it work.

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
