#!/usr/bin/env python3
import csv
import sys
from datetime import datetime, timedelta
from statistics import mean

def analyze_energy(file_path):
    data = []
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    power_val = float(row['power_w'])
                except (ValueError, TypeError):
                    continue

                ts_raw = row['timestamp'].replace('Z', '+00:00')
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
                            ts = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
                        except ValueError:
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

    data.sort(key=lambda x: x['timestamp'])
    
    last_time = data[-1]['timestamp']
    one_hour_ago = last_time - timedelta(hours=1)
    ten_mins_ago = last_time - timedelta(minutes=10)

    all_power = [d['power_w'] for d in data]
    hour_power = [d['power_w'] for d in data if d['timestamp'] >= one_hour_ago]
    ten_min_power = [d['power_w'] for d in data if d['timestamp'] >= ten_mins_ago]

    avg_all = mean(all_power)
    avg_hour = mean(hour_power) if hour_power else 0.0
    avg_10m = mean(ten_min_power) if ten_min_power else 0.0

    print(f"--- {file_path} ---")
    print(f"Average Power (All Time):   {avg_all:.2f} W")
    print(f"Average Power (Last Hour):  {avg_hour:.2f} W")
    print(f"Average Power (Last 10 Min): {avg_10m:.2f} W\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 power-avg.py <file1> [file2 ...]")
        sys.exit(1)

    for arg in sys.argv[1:]:
        analyze_energy(arg)
