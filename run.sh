#!/bin/bash

# Default log file path
DEFAULT_LOG_FILE="/var/log/energy-monitor.log"

# Use provided argument or default
LOG_FILE="${1:-$DEFAULT_LOG_FILE}"

# Check if log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "Error: Log file '$LOG_FILE' not found."
    exit 1
fi

# Use the existing Python script for calculation
python3 "$(dirname "$0")/power-avg.py" "$LOG_FILE"
