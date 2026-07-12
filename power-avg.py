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
    one_day_ago = last_time - timedelta(days=1)
    one_week_ago = last_time - timedelta(weeks=1)
    
    # Calculate start of current month/year for YTD
    # Note: This assumes "YTD" means since Jan 1st of the current year, 
    # or since the start of the current month depending on interpretation. 
    # Standard YTD usually means Jan 1. If "Month to Date" is also requested, 
    # we calculate MTD from the 1st of the current month.
    
    start_of_current_month = last_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_of_current_year = last_time.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Filter data based on time windows
    all_power = [d['power_w'] for d in data]
    hour_power = [d['power_w'] for d in data if d['timestamp'] >= one_hour_ago]
    ten_min_power = [d['power_w'] for d in data if d['timestamp'] >= ten_mins_ago]
    day_power = [d['power_w'] for d in data if d['timestamp'] >= one_day_ago]
    week_power = [d['power_w'] for d in data if d['timestamp'] >= one_week_ago]
    mtd_power = [d['power_w'] for d in data if d['timestamp'] >= start_of_current_month]
    ytd_power = [d['power_w'] for d in data if d['timestamp'] >= start_of_current_year]

    def safe_mean(lst):
        return mean(lst) if lst else 0.0

    avg_all = safe_mean(all_power)
    avg_hour = safe_mean(hour_power)
    avg_10m = safe_mean(ten_min_power)
    avg_day = safe_mean(day_power)
    avg_week = safe_mean(week_power)
    avg_mtd = safe_mean(mtd_power)
    avg_ytd = safe_mean(ytd_power)

    print(f"--- {file_path} ---")
    print(f"Average Power (All Time):   {avg_all:.2f} W")
    print(f"Average Power (Last Hour):  {avg_hour:.2f} W")
    print(f"Average Power (Last 10 Min): {avg_10m:.2f} W")
    print(f"Average Power (Last Day):   {avg_day:.2f} W")
    print(f"Average Power (Last Week):  {avg_week:.2f} W")
    print(f"Average Power (MTD):        {avg_mtd:.2f} W")
    print(f"Average Power (YTD):        {avg_ytd:.2f} W\n")

    print(f"Data Range: {data[0]['timestamp']} to {data[-1]['timestamp']}")
    print(f"Total Records: {len(data)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 power-avg.py <file1> [file2 ...]")
        sys.exit(1)

    for arg in sys.argv[1:]:
        analyze_energy(arg)


