import psutil

def get_cpu_usage():
    """Returns the current CPU usage percentage."""
    return psutil.cpu_percent(interval=0.1)

def get_memory_usage():
    """Returns the current memory usage percentage."""
    return psutil.virtual_memory().percent

