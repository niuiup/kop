import psutil
import time
import csv
from datetime import datetime
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from loguru import logger
import orjson


LOG_FILE = "log.csv"
METRICS_PORT = 8000

# Глобальный кэш значений для /metrics
metrics_cache = {
    "cpu": 0.0,
    "ram": 0.0,
    "battery": -1,
    "processes": 0,
    "timestamp": ""
}


# ----------------------------
#   ФУНКЦИИ ДЛЯ CSV И МЕТРИК
# ----------------------------

def get_battery_level():
    """Возвращает процент заряда или -1, если батареи нет."""
    try:
        batt = psutil.sensors_battery()
        if batt is None:
            return -1
        return batt.percent
    except Exception:
        return -1


def init_csv():
    """Создаёт CSV файл с заголовком, если его нет."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(["timestamp", "cpu", "ram", "battery", "processes"])


def collect_metrics():
    """Собирает системные метрики."""
    cpu = psutil.cpu_percent(interval=0.2)
    ram = psutil.virtual_memory().percent
    battery = get_battery_level()
    processes = len(psutil.pids())
    return cpu, ram, battery, processes


def update_cache(cpu, ram, battery, processes):
    """Обновляет глобальный кэш для HTTP-эндпоинта."""
    metrics_cache["cpu"] = cpu
    metrics_cache["ram"] = ram
    metrics_cache["battery"] = battery
    metrics_cache["processes"] = processes
    metrics_cache["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write_csv(cpu, ram, battery, processes):
    """Записывает строку в CSV."""
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([
            metrics_cache["timestamp"],
            cpu,
            ram,
            battery,
            processes
        ])
        f.flush()
        os.fsync(f.fileno())


# ----------------------------
#   HTTP СЕРВЕР /metrics
# ----------------------------

class MetricsHandler(BaseHTTPRequestHandler):
    """Возвращает текущие метрики в формате Prometheus-like."""

    def do_GET(self):
        if self.path != "/metrics":
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()

        # Формат максимально простой — как у node_exporter
        output = (
            f"cpu_percent {metrics_cache['cpu']}\n"
            f"ram_percent {metrics_cache['ram']}\n"
            f"battery_percent {metrics_cache['battery']}\n"
            f"process_count {metrics_cache['processes']}\n"
        )

        self.wfile.write(output.encode("utf-8"))


def run_http_server():
    """Запуск HTTP сервера в отдельном потоке."""
    server = HTTPServer(("0.0.0.0", METRICS_PORT), MetricsHandler)
    logger.info(f"HTTP metrics server запущен на порту {METRICS_PORT}")
    server.serve_forever()


# ----------------------------
#   ОСНОВНОЙ ЦИКЛ ПРОГРАММЫ
# ----------------------------

def main():
    logger.info("Мониторинг запущен. CSV → log.csv  |  HTTP → /metrics")

    init_csv()

    # запускаем HTTP сервер в отдельном потоке
    threading.Thread(target=run_http_server, daemon=True).start()

    while True:
        try:
            cpu, ram, battery, processes = collect_metrics()

            update_cache(cpu, ram, battery, processes)
            write_csv(cpu, ram, battery, processes)

            # вывод в консоль (одна строка)
            print(
                f"CPU: {cpu}% | RAM: {ram}% | Battery: {battery}% | Proc: {processes}",
                end="\r"
            )

            time.sleep(1)

        except KeyboardInterrupt:
            logger.info("Остановка мониторинга пользователем.")
            break

        except Exception as e:
            logger.error(f"Ошибка в главном цикле: {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()
