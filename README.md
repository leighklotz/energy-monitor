# Energy Monitor

A lightweight monitoring system to track real-time power consumption from a smart plug via an API, log the data, and provide tools for analysis and visualization.

## Features
- **Automated Logging**: Runs as a systemd service to capture power metrics every 10 seconds.
- **Visualization**: Generates ASCII plots of power over time using `gnuplot`.
- **Analysis**: Calculates average power consumption across different timeframes (All Time, Last Hour, Last 10 Minutes) using Python.

## Prerequisites
Ensure the following tools are installed on your system:
- `curl` - To fetch data from the API.
- `jq` - To parse JSON responses.
- `gnuplot` - For generating terminal plots.
- `python3` - For running analysis scripts.

## Installation

1. **Clone the repository** (or place these files in your desired directory).
2. **Configure the Service**: 
   Open `energy-monitor.service` and ensure the `ExecStart` path matches the actual location of your `energy-monitor.sh` script.
3. **Run the Install Script**:
   Make sure you have appropriate permissions (sudo) for systemd operations.
   ```bash
   ./energy-monitor-install.sh
   ```

## Usage

### 1. Monitoring
The monitoring script runs automatically as a background service. You can check the status or view live logs:
```bash
# Check service status
systemctl status energy-monitor.service

# View real-time logs
tail -f /var/log/energy-monitor.log
```

### 2. Plotting Data
To see a terminal-based line graph of the power consumption over time, run:
```bash
./energy-monitor-plot.sh /var/log/energy-monitor.log
```

### 3. Analyzing Averages
To calculate average wattage for specific windows (All Time, Last Hour, Last 10 Minutes), run:
```bash
./power-avg.sh /var/log/energy-monitor.log
```

## File Descriptions
- `energy-monitor.sh`: The core script that polls the API and writes to a CSV log.
- `energy-monitor.service`: Systemd unit file for persistence.
- `energy-monitor-install.sh`: Helper script to set up the service automatically.
- `energy-monitor-plot.sh`: Bash/Gnuplot script for visual representation in the terminal.
- `energy-monitor-power-avg.sh`: Python script for statistical analysis of the logged data.
