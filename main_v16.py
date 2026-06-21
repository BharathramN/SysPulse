import psutil
import time
import os
import platform
from datetime import datetime
import cpuinfo
from colorama import Fore, Style, init

init(autoreset=True)

old = psutil.net_io_counters()
old_recv = old.bytes_recv
old_sent = old.bytes_sent

cpu_history = []
ram_history = []


def bar(percent, length=20):
    filled = int(percent / 100 * length)

    if percent < 50:
        color = Fore.GREEN
    elif percent < 80:
        color = Fore.YELLOW
    else:
        color = Fore.RED

    return (
        color
        + "█" * filled
        + Style.RESET_ALL
        + "░" * (length - filled)
    )


def sparkline(data):
    chars = "▁▂▃▄▅▆▇█"

    if not data:
        return ""

    result = ""

    for value in data:
        index = int((value / 100) * (len(chars) - 1))
        result += chars[index]

    return result
def status_icon(percent):
    if percent < 50:
        return "🟢"
    elif percent < 80:
        return "🟡"
    else:
        return "🔴"


def box_title(title):
    print(f"\n┌─ {title} " + "─" * (50 - len(title)) + "┐")


while True:
    os.system("cls")
    print(Fore.CYAN + "╔══════════════════════════════════════════════════════╗")
    print(Fore.CYAN + "║                    SYSPULSE V16                    ║")
    print(Fore.CYAN + "╚══════════════════════════════════════════════════════╝")

    # Time
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"\nTime: {current_time}")

    # Uptime
    uptime_seconds = time.time() - psutil.boot_time()

    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)

    print(f"System Uptime: {hours}h {minutes}m")

    # System Info
    box_title("SYSTEM")

    print(f"OS: {platform.system()} {platform.release()}")

    print(
        f"CPU Cores: "
        f"{psutil.cpu_count(logical=False)}"
    )

    print(
        f"CPU Threads: "
        f"{psutil.cpu_count(logical=True)}"
    )

    total_ram = round(
        psutil.virtual_memory().total / (1024**3),
        1
    )

    print(f"Total RAM: {total_ram} GB")

    # CPU Details
    box_title("CPU DETAILS")

    cpu_info = cpuinfo.get_cpu_info()

    print(
        f"CPU Name: "
        f"{cpu_info['brand_raw']}"
    )

    freq = psutil.cpu_freq()

    if freq:
        print(
            f"Current Frequency: "
            f"{freq.current:.0f} MHz"
        )

        print(
            f"Max Frequency: "
            f"{freq.max:.0f} MHz"
        )

    # Performance
    cpu = psutil.cpu_percent(interval=1)

    ram = psutil.virtual_memory()

    cpu_history.append(cpu)
    ram_history.append(ram.percent)

    if len(cpu_history) > 20:
        cpu_history.pop(0)

    if len(ram_history) > 20:
        ram_history.pop(0)

    box_title("PERFORMANCE")

    print(
    f"{status_icon(cpu)} CPU "
    f"[{bar(cpu)}] "
    f"{cpu}%"
    )

    print(
    f"{status_icon(ram.percent)} RAM "
    f"[{bar(ram.percent)}] "
    f"{ram.percent}%"
    )

    used_ram = round(
        ram.used / (1024**3),
        1
    )

    free_ram = round(
        ram.available / (1024**3),
        1
    )

    print(f"Used RAM: {used_ram} GB")
    print(f"Free RAM: {free_ram} GB")

    print("\n--- Usage History ---")

    print(
        f"CPU Trend: "
        f"{sparkline(cpu_history)}"
    )

    print(
        f"RAM Trend: "
        f"{sparkline(ram_history)}"
    )

    # CPU Cores
    print("\n--- CPU Core Usage ---")

    core_usage = psutil.cpu_percent(
        interval=None,
        percpu=True
    )

    for i, usage in enumerate(core_usage):
        print(
            f"Core {i+1:02d} "
            f"[{bar(usage, 12)}] "
            f"{usage}%"
        )

    # Battery
    battery = psutil.sensors_battery()

    box_title("BATTERY")
    if battery:

        charging = (
            "Charging"
            if battery.power_plugged
            else "Discharging"
        )

        print(
            f"BAT [{bar(battery.percent)}] "
            f"{battery.percent}% "
            f"({charging})"
        )

        if battery.secsleft > 0:
            hrs = battery.secsleft // 3600
            mins = (
                battery.secsleft % 3600
            ) // 60

            print(
                f"Remaining: "
                f"{hrs}h {mins}m"
            )

    else:
        print("Battery Not Detected")

    # Storage
    box_title("STORAGE")

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
    box_title("NETWORK")

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

    print(
        f"↓ Download: "
        f"{download_speed:.2f} MB/s"
    )

    print(
        f"↑ Upload:   "
        f"{upload_speed:.2f} MB/s"
    )

    old_recv = new.bytes_recv
    old_sent = new.bytes_sent

    # Top Processes
    box_title("TOP PROCESSES")

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

        for i, (
            name,
            cpu_usage
        ) in enumerate(
            processes[:5],
            start=1
        ):

            print(
                Fore.MAGENTA
                + f"{i}. "
                + f"{name:<20} "
                + f"{cpu_usage:.1f}%"
            )

    else:
        print(
            "No active process found"
        )

    time.sleep(1)