import psutil
import time
import pandas as pd
from datetime import datetime

OUT = "monitor.xlsx"
INTERVAL = 10  # интервал в секундах

def sample():
    ts = datetime.now().isoformat(sep=" ", timespec="seconds")
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    return {"timestamp": ts, "cpu_percent": cpu, "ram_percent": ram}

def append_row(row: dict):
    try:
        df = pd.read_excel(OUT)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([row])
    df.to_excel(OUT, index=False)

def main():
    print("Monitor starting...")
    try:
        while True:
            row = sample()
            print(row)
            append_row(row)
            time.sleep(INTERVAL - 1)
    except KeyboardInterrupt:
        print("Stopped by user")

if __name__ == "__main__":
    main()
