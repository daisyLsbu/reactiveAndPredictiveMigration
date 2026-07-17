## Installation and Testing

---

### Step 1 — Monitor Application (Windows Server)

Set up the monitoring server with the application, InfluxDB, and Grafana.

**1a. Install Git**

```cmd
winget install --id Git.Git -e --source winget
```

**1b. Clone the repository**

```bash
git clone -b monitor https://github.com/daisyLsbu/MigrationOrchesTelemtry.git
cd Monitor
```

**1c. Install Python**

Open VS Code → Extensions → search and install **Python**.

**1d. Set up the Python environment**

```bash
pip install virtualenv
pip install -r requirement.txt
```

If `activate` is blocked in PowerShell, run the following first:

```powershell
Set-ExecutionPolicy Unrestricted
cd venv/Scripts
./activate
pip install --upgrade pip
```

---

### Step 2 — InfluxDB Setup (Windows)

**Install InfluxDB**, then start it with:

```powershell
cd 'C:\Program Files\InfluxData\influxdb'
./influxd
```

Access the InfluxDB UI at `http://localhost:8086`.

---

### Step 3 — Network Setup using GNS3

#### Windows

**a. Install VMware Workstation**

Download and install VMware Workstation.

**b. Install GNS3 VM**

- Download GNS3 VM and extract it
- Open VMware → **File → Open** → select the extracted GNS3 VM path → set name to `gns3 vm` → Import
- Configure VM settings: Memory = 8 GB, Processors = 1, Cores = 4, VT-x = enabled
- Upgrade if prompted

**c. Install GNS3 UI**

Run the installer: Next → Agree → select **Desktop and UI** → set path → install Nmap → Agree → Next → install Wireshark → enter email → Next → install PuTTY → Finish

**d. Configure GNS3 UI to connect to VM**

Setup Wizard → Run on Virtual Machine → select path → set `localhost` and port `3080` → select VM name created → Processors = 4, Memory = 8192 → OK

**e. VMware network settings**

Set network adapters to **Host-only** and **NAT**.

**f. Security configuration**

VMware → VM → Settings → Security → Username: `gns3`, Password: `gns3` → OK

**g. Install PC images in GNS3**

Download from GNS3 Marketplace → Appliances:

- **Ubuntu Cloud Guest** — download `amd64` image (initdata and actual image)
- **Ubuntu Desktop Guest** — download Ubuntu Desktop Guest image

Import: **File → Import Appliance** → select image → Install in GNS3 VM → OK

Repeat for both the Docker image and Ubuntu Cloud image.

**h. Create topology**

- Drag and drop 3 × Ubuntu Cloud nodes, 1 × Switch, and 1 × NAT onto the canvas
- Connect all nodes to the switch using Ethernet
- Start all hosts and open a console for each
- Run `ping` to confirm all hosts are reachable and accessible to each other

---

#### Linux

```bash
# Update and upgrade the system
sudo apt -y update && sudo apt -y upgrade

# Install GNS3
sudo add-apt-repository ppa:gns3/ppa
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install gns3-iou
sudo apt update
sudo apt install gns3-gui gns3-server

# Install drivers for internet adapter
sudo apt install git dkms
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
sudo dkms status
```

---

### Step 4 — Telemetry Application Setup (each host node)

See [`TelemetryApplication`](https://github.com/daisyLsbu/TelemetryApplication) for full details.

- Open GNS3 → start each host → open console → note the IP address
- Run `setup.sh` to install dependencies
- Run `build.sh` to clone the repository

**Linux hosts — additional steps:**

```bash
sudo apt install python3.10-venv
pip install -r requirements.txt
```

- Run `run.sh` with the port number as an argument:

```bash
bash run.sh 5000
```

Also run `dockerSetup.sh` from [`ContainerCreationMigration`](https://github.com/daisyLsbu/ContainerCreationMigration) on each host to set up Docker and containers.

---

### Step 5 — Test the Application

See [`MonitoringApplication`](https://github.com/daisyLsbu/MonitoringApplication) for full details.

**5a. Verify host connectivity**

```bash
ping <host-ip>
```

Confirm all hosts in the network are reachable from the monitoring server.

**5b. Quick display test**

- Open `test.html` with Live Server in VS Code
- Update `node.sh` with the correct IPs and ports of each host
- Run:

```bash
python3 collectDisplaytable.py
```

- Open browser at `http://127.0.0.1:5501` to view the collected data table
- Press `Ctrl+C` to stop, then verify directly via `http://<host-ip>:<port>`

**5c. Start async collection and InfluxDB ingestion**

Update InfluxDB credentials in `influxdbsuite.py`, then run:

```bash
python3 collectorAsync.py
```

Verify data is flowing in InfluxDB at `http://localhost:8086`.

---

### Step 6 — Start the Migration Orchestrator

See [`MigrationOrchestrator`](https://github.com/daisyLsbu/MigrationOrchestrator) for full details.

```bash
python3 migrationAgent.py
```

The orchestrator will continuously evaluate host resource utilisation and trigger reactive migration when thresholds are breached.

---

### Step 7 — Predictive Migration using LSTM *(optional)*

The LSTM model in [`LSTMSetup`](https://github.com/daisyLsbu/LSTMSetup) can be trained on historical telemetry data collected by the Monitoring Application. Once trained, the model is loaded in `migrationAgent.py` to forecast future resource utilisation and inform proactive migration decisions.

Refer to the [LSTMSetup](https://github.com/daisyLsbu/LSTMSetup) repository for training instructions.

---

### Step 8 — MAMD Decision Logic *(optional)*

As an alternative or complement to LSTM-based prediction, the **MAMD (Moving Average Migration Decision)** logic can be used to smooth telemetry signals before threshold comparison.

The implementation is in `MAMD.py`. Enable it in `migrationAgent.py` by configuring the MAMD decision path.
