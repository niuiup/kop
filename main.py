import psutil
import time

def main():
    while True:
        cpu = psutil.cpu_percent(interval=1)
        print("CPU:", cpu, "%")
        with open("log.txt", "a") as f:
            f.write(f"{time.time()}: CPU {cpu}%\n")

if __name__ == "__main__":
    main()
