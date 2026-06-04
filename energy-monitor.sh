#!/bin/bash

PLUG=plug4.klotz.me

echo timestamp,plug,power_w,voltage_v,current_a,energy_kwh

while true; do
  ts=$(date -Is)
  # Updated endpoints to use Entity Names instead of Object IDs
  p=$(curl -s "$PLUG/sensor/Power" | jq -r .value)
  v=$(curl -s "$PLUG/sensor/Voltage" | jq -r .value)
  c=$(curl -s "$PLUG/sensor/Current" | jq -r .value)
  e=$(curl -s "$PLUG/sensor/Total%20Daily%20Energy" | jq -r .value)
  
  printf '%s,%s,%s,%s,%s,%s\n' "$ts" "$PLUG" "$p" "$v" "$c" "$e"
  sleep 10
done
