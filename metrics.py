import psutil

def get_cpu_usage():
    """Returns the current CPU usage percentage."""
    return psutil.cpu_percent(interval=0.1)

def get_memory_usage():
    """Returns the current memory usage percentage."""
    return psutil.virtual_memory().percent

def get_disk_usage():
    """Returns the current memory usage percentage."""
    return psutil.disk_usage('/').percent

def get_net_connections():
    psutil.net_connections(kind='all')

def get_sensors_temperatures():
    return psutil.sensors_temperatures(fahrenheit=False)

def get_sensors_fans():
    return psutil.sensors_fans()
