import psutil
import time
import os
import datetime

old = psutil.net_io_counters()
old_sent = old.bytes_sent
old_recv = old.bytes_recv

while True:
    os.system("cls")
    print("="*40)
    print("        SysPulse v0.5       ")
    print("="*40)
    print(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()


    print("=== SysPulse v0.5 ===\n")

    # CPU
    cpu = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu}%")

    # RAM
    ram = psutil.virtual_memory()
    print(f"RAM Usage: {ram.percent}%")

    # Battery
    battery = psutil.sensors_battery()

    if battery:
        print(f"Battery: {battery.percent}%")
    else:
        print("Battery not detected")

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
    print("\n"+ "-" *15 + " Network " + "-" *15)

    new = psutil.net_io_counters()

    download_speed = (new.bytes_recv - old_recv) / 1024 / 1024
    upload_speed = (new.bytes_sent - old_sent) / 1024 / 1024

    print(f"Download: {download_speed:.2f} MB/s")
    print(f"Upload: {upload_speed:.2f} MB/s")

    old_recv = new.bytes_recv
    old_sent = new.bytes_sent

    time.sleep(1)