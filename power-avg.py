#!/usr/bin/env python3
import csv
import sys
from datetime import datetime, timedelta
from statistics import mean

# Default file path if no arguments are provided
DEFAULT_FILE = "/var/log/energy-monitor/energy-monitor.log"

def analyze_energy(file_path):
    data = []
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or len(row) < 3:
                    continue
                try:
                    # Index 0 is timestamp, index 2 is power_w based on provided log format
                    ts_raw = row[0].replace('Z', '+00:00')
                    power_val = float(row[2])
                except (ValueError, TypeError, IndexError):
                    continue

                # Timestamp parsing logic
                try:
                    ts = datetime.fromisoformat(ts_raw)
                except ValueError:
                    ts_str = ts_raw.replace('T', ' ')
                    if len(ts_str) > 19 and ts_str[-6] == ':':
                        ts_str = ts_str[:-3] + ts_str[-2:]
                    try:
                        ts = datetime.fromisoformat(ts_str)
                    except ValueError:
                        try:
                            ts = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                        except (ValueError, IndexError):
                            continue

                data.append({
                    'timestamp': ts,
                    'power_w': power_val
                })
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    if not data:
        print(f"--- {file_path} ---")
        print("No valid data available.")
        return

    # Ensure chronological order for time-range logic
    data.sort(key=lambda x: x['timestamp'])
    last_time = data[-1]['timestamp']
    first_ts = data[0]['timestamp']
    
    # Define the metrics to calculate and their relative starting timestamps
    metrics = [
        ("Average Power (Last 10 Min)", last_time - timedelta(minutes=10)),
        ("Average Power (Last Hour)",   last_time - timedelta(hours=1)),
        ("Average Power (Last Day)",    last_time - timedelta(days=1)),
        ("Average Power (Last Week)",   last_time - timedelta(weeks=1)),
        ("Average Power (MTD)",         last_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)),
        ("Average Power (YTD)",         last_time.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0))
    ]

    def safe_mean(lst):
        return mean(lst) if lst else 0.0

    print(f"--- {file_path} ---")
    # Always show All Time as the primary baseline
    avg_all = safe_mean([d['power_w'] for d in data])
    print(f"Average Power (All Time):   {avg_all:.2f} W")

    for label, threshold in metrics:
        # ELIDE LOGIC: 
        # If the timeframe's start is older than or equal to our earliest recorded log entry,
        # that period contains no unique data relative to "All Time" (it would just be a duplicate).
        if threshold <= first_ts:
            continue

        period_power = [d['power_w'] for d in data if d['timestamp'] >= threshold]
        
        if period_power:
            avg_val = safe_mean(period_power)
            print(f"{label:<28} {avg_val:.2f} W")

    print() # Spacer
    print(f"Data Range: {data[0]['timestamp']} to {data[-1]['timestamp']}")
    print(f"Total Records: {len(data)}")

if __name__ == "__main__":
   files_to_process = sys.argv[1:] if len(sys.argv) > 1 else [DEFAULT_FILE]

   for arg in files_to_process:
       analyze_energy(arg)
