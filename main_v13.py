import psutil
import time
import os
import platform
from datetime import datetime
import cpuinfo

old = psutil.net_io_counters()
old_recv = old.bytes_recv
old_sent = old.bytes_sent


def bar(percent, length=20):
    filled = int(percent / 100 * length)
    return "█" * filled + "░" * (length - filled)


while True:
    os.system("cls")

    print("=" * 50)
    print("               SYSPULSE V13")
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

    total_ram = round(
        psutil.virtual_memory().total / (1024**3),
        1
    )

    print(f"Total RAM: {total_ram} GB")

    # CPU Details
    print("\n--- CPU Details ---")

    cpu_info = cpuinfo.get_cpu_info()

    print(f"CPU Name: {cpu_info['brand_raw']}")

    freq = psutil.cpu_freq()

    if freq:
        print(f"Current Frequency: {freq.current:.0f} MHz")
        print(f"Max Frequency: {freq.max:.0f} MHz")

    # Live Usage
    cpu = psutil.cpu_percent(interval=1)

    ram = psutil.virtual_memory()

    print("\n--- Performance ---")

    print(
        f"CPU [{bar(cpu)}] {cpu}%"
    )

    print(
        f"RAM [{bar(ram.percent)}] {ram.percent}%"
    )

    # Battery
    battery = psutil.sensors_battery()

    print("\n--- Battery ---")

    if battery:
        charging = (
            "Charging"
            if battery.power_plugged
            else "Discharging"
        )

        print(
            f"BAT [{bar(battery.percent)}] "
            f"{battery.percent}% ({charging})"
        )
    else:
        print("Battery Not Detected")

    # Storage
    print("\n--- Storage ---")

    c_drive = psutil.disk_usage("C:\\")

    print(
        f"C Drive [{bar(c_drive.percent)}] "
        f"{c_drive.percent}%"
    )

    print(
        f"Free Space: "
        f"{round(c_drive.free/(1024**3),1)} GB"
    )

    try:
        d_drive = psutil.disk_usage("D:\\")

        print(
            f"\nD Drive [{bar(d_drive.percent)}] "
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

    print(f"↓ Download: {download_speed:.2f} MB/s")
    print(f"↑ Upload:   {upload_speed:.2f} MB/s")

    old_recv = new.bytes_recv
    old_sent = new.bytes_sent

    # Top 5 Processes
    print("\n--- Top Processes ---")

    processes = []

    for proc in psutil.process_iter(
        ['name', 'cpu_percent']
    ):
        try:
            name = proc.info['name']
            cpu_usage = proc.info['cpu_percent']

            if (
                cpu_usage > 0
                and name != "System Idle Process"
            ):
                processes.append(
                    (name, cpu_usage)
                )

        except:
            pass

    processes = sorted(
        processes,
        key=lambda x: x[1],
        reverse=True
    )

    if processes:
        for i, (name, cpu_usage) in enumerate(
            processes[:5],
            start=1
        ):
            print(
                f"{i}. {name:<20} "
                f"{cpu_usage:.1f}%"
            )
    else:
        print("No active process found")

    time.sleep(1)