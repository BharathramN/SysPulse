import psutil
import time
import os

boot_time = psutil.boot_time()

old = psutil.net_io_counters()
old_recv = old.bytes_recv
old_sent = old.bytes_sent

while True:
    os.system("cls")

    print("=" * 40)
    print("         SYSPULSE V7")
    print("=" * 40)

    # Time
    current_time = time.strftime("%H:%M:%S")
    print(f"\nTime: {current_time}")

    # Uptime
    uptime_seconds = time.time() - boot_time
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)

    print(f"System Uptime: {hours}h {minutes}m")

    # CPU
    cpu = psutil.cpu_percent(interval=0.1)
    print(f"\nCPU Usage: {cpu}%")

    # RAM
    ram = psutil.virtual_memory()
    print(f"RAM Usage: {ram.percent}%")

    # Battery
    battery = psutil.sensors_battery()

    if battery:
        print(f"Battery: {battery.percent}%")
    else:
        print("Battery: Not Detected")

    # Storage
    print("\n--- Storage ---")

    c_drive = psutil.disk_usage("C:\\")
    print(
        f"C Drive: {c_drive.percent}% Used | "
        f"{round(c_drive.free / (1024**3), 1)} GB Free"
    )

    try:
        d_drive = psutil.disk_usage("D:\\")
        print(
            f"D Drive: {d_drive.percent}% Used | "
            f"{round(d_drive.free / (1024**3), 1)} GB Free"
        )
    except:
        pass

    # Network
    print("\n--- Network ---")

    new = psutil.net_io_counters()

    download_speed = (new.bytes_recv - old_recv) / 1024 / 1024
    upload_speed = (new.bytes_sent - old_sent) / 1024 / 1024

    print(f"Download: {download_speed:.2f} MB/s")
    print(f"Upload:   {upload_speed:.2f} MB/s")

    old_recv = new.bytes_recv
    old_sent = new.bytes_sent

    # Top Process
    print("\n--- Top Process ---")

    top_process = None
    top_cpu = 0

    for proc in psutil.process_iter(['name', 'cpu_percent']):
        try:
            process_name = proc.info['name']

            if process_name in [
                "System Idle Process",
                "Idle",
                "System"
            ]:
                continue

            cpu_usage = proc.info['cpu_percent']

            if cpu_usage > top_cpu:
                top_cpu = cpu_usage
                top_process = process_name

        except:
            pass

    if top_process:
        print(f"{top_process} ({top_cpu:.1f}% CPU)")
    else:
        print("No active process found")

    time.sleep(1)