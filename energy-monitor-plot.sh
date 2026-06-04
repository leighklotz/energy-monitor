#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <log_file>"
    exit 1
fi

FILE=$1

# Check if file exists
if [ ! -f "$FILE" ]; then
    echo "Error: File $FILE not found."
    exit 1
fi

# Extract data, remove header, and format for gnuplot (Time vs Power)
# We use tail to skip the header, awk to get columns 1 and 3.
DATA=$(tail -n +2 "$FILE" | awk -F, '{print $1 " " $3}' | sed 's/-[0-9]\{2\}:[0-9]\{2\}//')

# Create a temporary file for plotting
TMP_DATA=$(mktemp)
echo "$DATA" > "$TMP_DATA"

# Execute gnuplot correctly. 
# Removed "set datafile output" and fixed the plot command to use the temp file directly.
gnuplot -e "set xdata time; \
            set timefmt '%Y-%m-%dT%H:%M:%S'; \
            set title 'Power over Time ($FILE)'; \
            set xlabel 'Time'; \
            set ylabel 'Watts'; \
            set term dumb; \
            plot '$TMP_DATA' using 1:2 with lines title 'Power (W)'"

rm "$TMP_DATA"
