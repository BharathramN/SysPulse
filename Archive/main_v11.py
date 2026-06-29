import psutil
import time
import os
import platform
from datetime import datetime

def progress_bar(percent, length=20):
    filled = int(percent / 100 * length)
    return "█" * filled + "░" * (length - filled)

old = psutil.net_io_counters()
old_recv = old.bytes_recv
old_sent = old.bytes_sent

while True:
    os.system("cls")

    print("=" * 50)
    print("              SYSPULSE V11")
    print("=" * 50)

    # Time
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"\nTime: {current_time}")

    # Uptime
    uptime_seconds = time.time() - psutil.boot_time()
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)

    print(f"System Uptime: {hours}h {minutes}m")

    # System Info
    print("\n--- System Info ---")

    print(f"OS: {platform.system()} {platform.release()}")
    print(f"CPU Cores: {psutil.cpu_count(logical=False)}")
    print(f"CPU Threads: {psutil.cpu_count(logical=True)}")

    ram = psutil.virtual_memory()
    total_ram = round(ram.total / (1024**3), 1)

    print(f"Total RAM: {total_ram} GB")

    # CPU
    cpu = psutil.cpu_percent(interval=1)

    print("\n--- CPU ---")
    print(f"[{progress_bar(cpu)}] {cpu}%")

    # RAM
    print("\n--- RAM ---")
    print(f"[{progress_bar(ram.percent)}] {ram.percent}%")

    # Battery
    print("\n--- Battery ---")

    battery = psutil.sensors_battery()

    if battery:
        print(f"[{progress_bar(battery.percent)}] {battery.percent}%")

        if battery.power_plugged:
            print("⚡ Charging")
    else:
        print("Battery Not Detected")

    # Storage
    print("\n--- Storage ---")

    c_drive = psutil.disk_usage("C:\\")

    print(
        f"C Drive [{progress_bar(c_drive.percent)}] "
        f"{c_drive.percent}%"
    )
    print(
        f"Free Space: "
        f"{round(c_drive.free/(1024**3),1)} GB"
    )

    try:
        d_drive = psutil.disk_usage("D:\\")

        print(
            f"D Drive [{progress_bar(d_drive.percent)}] "
            f"{d_drive.percent}%"
        )
        print(
            f"Free Space: "
            f"{round(d_drive.free/(1024**3),1)} GB"
        )

    except:
        pass

    # Network
    print("\n--- Network ---")

    new = psutil.net_io_counters()

    download_speed = (
        (new.bytes_recv - old_recv)
        / 1024
        / 1024
    )

    upload_speed = (
        (new.bytes_sent - old_sent)
        / 1024
        / 1024
    )

    print(f"Download: {download_speed:.2f} MB/s")
    print(f"Upload:   {upload_speed:.2f} MB/s")

    old_recv = new.bytes_recv
    old_sent = new.bytes_sent

    # Top Process
    print("\n--- Top Process ---")

    top_process = None
    top_cpu = 0

    for proc in psutil.process_iter(
        ['name', 'cpu_percent']
    ):
        try:
            process_name = proc.info['name']

            if process_name == "System Idle Process":
                continue

            cpu_usage = proc.info['cpu_percent']

            if cpu_usage > top_cpu:
                top_cpu = cpu_usage
                top_process = process_name

        except:
            pass

    if top_process:
        print(
            f"🔥 {top_process} "
            f"({top_cpu:.1f}% CPU)"
        )
    else:
        print("No active process found")

    time.sleep(1)