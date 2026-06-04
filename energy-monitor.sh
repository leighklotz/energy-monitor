#!/bin/bash

PLUG=plug4.klotz.me

echo timestamp,plug,power_w,voltage_v,current_a,energy_kwh

while true; do
  ts=$(date -Is)
  p=$(curl -s "$PLUG/sensor/power" | jq -r .value)
  v=$(curl -s "$PLUG/sensor/voltage" | jq -r .value)
  c=$(curl -s "$PLUG/sensor/current" | jq -r .value)
  e=$(curl -s "$PLUG/sensor/total_daily_energy" | jq -r .value)
  printf '%s,%s,%s,%s,%s,%s\n' "$ts" "$PLUG" "$p" "$v" "$c" "$e"
  sleep 10
done

