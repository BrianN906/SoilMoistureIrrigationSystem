import serial
import csv
import os
from datetime import datetime, timedelta

os.chdir(os.path.dirname(os.path.abspath(__file__)))

PORT = "COM3"
BAUD = 9600
CSV_FILE = "moisture_log.csv"

READ_INTERVAL  = 20   # minutes between regular reads
PUMP_THRESHOLD = 30   # pump when moisture drops below this percentage

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "time", "raw", "moisture_pct", "type"])

ser = serial.Serial(PORT, BAUD, timeout=1)
print(f"Program started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Listening on {PORT}...")
print(f"Read every {READ_INTERVAL} min | Pump when moisture < {PUMP_THRESHOLD}%")

def log(date, time, raw, moisture, entry_type):
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, time, raw, moisture, entry_type])
    print(f"  >> Logged to CSV: {date}, {time}, raw={raw}, moisture={moisture}%, type={entry_type}")

now = datetime.now()
next_read = now + timedelta(minutes=READ_INTERVAL)

while True:
    now = datetime.now()

    if now >= next_read:
        next_read = now + timedelta(minutes=READ_INTERVAL)
        ser.write(b"READ\n")

    line = ser.readline().decode("utf-8").strip()
    if not line:
        continue

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    if line.startswith("READ,"):
        parts = line.split(",")
        raw, moisture = parts[1], int(parts[2])
        print(f"[READ]   {date} {time} | Raw: {raw} | Moisture: {moisture}%")
        log(date, time, raw, moisture, "READ")

        if moisture < PUMP_THRESHOLD:
            print(f"  >> Moisture {moisture}% is below {PUMP_THRESHOLD}% — pumping...")
            ser.write(b"PUMP\n")

    elif line.startswith("PUMP,"):
        parts = line.split(",")
        raw, moisture = parts[1], parts[2]
        print(f"[PUMP]   {date} {time} | Raw: {raw} | Moisture: {moisture}%")
        log(date, time, raw, moisture, "PUMP")
        next_read = datetime.now() + timedelta(minutes=READ_INTERVAL)

    elif line.startswith("MANUAL,"):
        parts = line.split(",")
        raw, moisture = parts[1], parts[2]
        print(f"[MANUAL] {date} {time} | Raw: {raw} | Moisture: {moisture}%")
        log(date, time, raw, moisture, "MANUAL")
        next_read = datetime.now() + timedelta(minutes=READ_INTERVAL)