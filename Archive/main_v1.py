import psutil
print("===SysPulse===")
cpu=psutil.cpu_percent(interval=1)
print(f"CPU Usage: {cpu}%")
ram=psutil.virtual_memory()
print(f"RAM Usage:{ram.percent}%")
battery=psutil.sensors_battery()
if battery:
    print(f"Battery: {battery.percent}%")   
else:
    print("Battery not Detected")