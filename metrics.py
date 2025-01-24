import psutil
import json
import time

def collect_metrics():
    metrics = {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }
    with open("/tmp/system_metrics.json", "w") as f:
        json.dump(metrics, f)

if __name__ == "__main__":
    while True:
        collect_metrics()
        time.sleep(5)  # Change the value if you wish to have a slower or faster update time

