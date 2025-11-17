import psutil
import time
import csv
from datetime import datetime
import os

# Имя файла лога
LOG_FILE = "log.csv"


def get_battery_level():
    """Возвращает заряд батареи или -1 если батареи нет."""
    try:
        batt = psutil.sensors_battery()
        if batt is None:
            return -1
        return batt.percent
    except:
        return -1


def init_csv():
    """Создаёт CSV файл с заголовками, если он еще не создан."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(["timestamp", "cpu", "ram", "battery", "processes"])


def collect_metrics():
    """Собирает показатели системы."""
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    battery = get_battery_level()
    processes = len(psutil.pids())
    return cpu, ram, battery, processes


def write_row(cpu, ram, battery, processes):
    """Записывает строку в CSV."""
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            cpu,
            ram,
            battery,
            processes
        ])


def main():
    print("Мониторинг запущен. Данные пишутся в log.csv. Нажми CTRL + C чтобы остановить.")
    init_csv()

    while True:
        cpu, ram, battery, processes = collect_metrics()
        write_row(cpu, ram, battery, processes)
        time.sleep(2)  # интервал записи в секунду


if __name__ == "__main__":
    main()
