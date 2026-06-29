import customtkinter as ctk
import psutil
import wmi
c=wmi.WMI()
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("SysPulse Beta v1.9")
app.geometry("500x500")

title = ctk.CTkLabel(
    app,
    text="SYSPULSE Beta v1.9",
    font=("Arial", 24, "bold")
)
title.pack(pady=15)

# =========================
# SYSTEM INFO
# =========================

import platform
import wmi

c = wmi.WMI()
cpu_name = c.Win32_Processor()[0].Name
specs_title = ctk.CTkLabel(
    app,
    text="SYSTEM INFO",
    font=("Segoe UI", 20, "bold")
)
specs_title.pack(pady=(10, 5))

os_label = ctk.CTkLabel(
    app,
    text="OS: Loading...",
    font=("Segoe UI", 14)
)
os_label.pack()

cpu_name_label = ctk.CTkLabel(
    app,
    text="CPU: Loading...",
    font=("Segoe UI", 14)
)
cpu_name_label.pack()

cores_label = ctk.CTkLabel(
    app,
    text="Cores: Loading...",
    font=("Segoe UI", 14)
)
cores_label.pack()

threads_label = ctk.CTkLabel(
    app,
    text="Threads: Loading...",
    font=("Segoe UI", 14)
)
threads_label.pack()

ram_total_label = ctk.CTkLabel(
    app,
    text="RAM: Loading...",
    font=("Segoe UI", 14)
)
ram_total_label.pack()

freq_label = ctk.CTkLabel(
    app,
    text="Frequency: Loading...",
    font=("Segoe UI", 14)
)
freq_label.pack()
gpu_label = ctk.CTkLabel(
    app,
    text="GPU: Loading...",
    font=("Segoe UI", 14)
)
gpu_label.pack()

time_label = ctk.CTkLabel(app, text="")
time_label.pack()

cpu_label = ctk.CTkLabel(app, text="")
cpu_label.pack(pady=10)

cpu_bar = ctk.CTkProgressBar(app, width=300)
cpu_bar.pack()

ram_label = ctk.CTkLabel(app, text="")
ram_label.pack(pady=10)

ram_bar = ctk.CTkProgressBar(app, width=300)
ram_bar.pack()

battery_label = ctk.CTkLabel(app, text="")
battery_label.pack(pady=10)
battery_bar = ctk.CTkProgressBar(app, width=300)
battery_bar.pack()
disk_label = ctk.CTkLabel(
    app,
    text=""
)
disk_label.pack(pady=5)


network_label = ctk.CTkLabel(app, text="")
network_label.pack(pady=10)

old = psutil.net_io_counters()
old_recv = old.bytes_recv
old_sent = old.bytes_sent


 # SYSTEM INFO


def update_stats():
    global old_recv
    global old_sent

    os_label.configure(
        text=f"OS: {platform.system()} {platform.release()}"
    )

    cpu_name_label.configure(
       text=f"CPU: {cpu_name}"
    )

    cores_label.configure(
        text=f"Cores: {psutil.cpu_count(logical=False)}"
    )

    threads_label.configure(
        text=f"Threads: {psutil.cpu_count(logical=True)}"
    )

    total_ram = round(
        psutil.virtual_memory().total /
        (1024 ** 3),
        1
    )

    ram_total_label.configure(
        text=f"Total RAM: {total_ram} GB"
    )
    try:
        gpus = c.Win32_VideoController()
        gpu_names = []
        for gpu in gpus:
            if gpu.Name and gpu.Name not in gpu_names:
                            
                            gpu_names.append(gpu.Name)

        gpu_label.configure(
        text="GPU(s): " + " | ".join(gpu_names)
        )

    except Exception:
        gpu_label.configure(
            text="GPU: Not Detected"
        )


    disk = psutil.disk_usage("C:")

    disk_label.configure(
    text=f"Disk Usage: {disk.percent}%"
    )   

os_label.configure(
    text=f"OS: {platform.system()} {platform.release()}"
)

cpu_name_label.configure(
    text=f"CPU: {cpu_name}"
)

cores_label.configure(
    text=f"Cores: {psutil.cpu_count(logical=False)}"
)

threads_label.configure(
    text=f"Threads: {psutil.cpu_count(logical=True)}"
)

total_ram = round(
    psutil.virtual_memory().total /
    (1024 ** 3),
    1
)

ram_total_label.configure(
    text=f"Total RAM: {total_ram} GB"
)


freq = psutil.cpu_freq()

if freq:
    freq_label.configure(
        text=f"Frequency: {freq.current:.0f} MHz"
    )
    
    current_time = datetime.now().strftime("%H:%M:%S")

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory()

    battery = psutil.sensors_battery()

    new = psutil.net_io_counters()

    download = (
        (new.bytes_recv - old_recv)
        / 1024
        / 1024
    )

    upload = (
        (new.bytes_sent - old_sent)
        / 1024
        / 1024
    )

    old_recv = new.bytes_recv
    old_sent = new.bytes_sent

    time_label.configure(
        text=f"Time: {current_time}"
    )

    cpu_label.configure(
        text=f"CPU Usage: {cpu}%"
    )

    cpu_bar.set(cpu / 100)

    ram_label.configure(
        text=f"RAM Usage: {ram.percent}%"
    )

    ram_bar.set(ram.percent / 100)

    if battery:
        status = (
        "⚡ Charging"
        if battery.power_plugged
        else "🔋 Discharging"
    )

        battery_label.configure(
        text=f"Battery: {battery.percent}% | {status}"
        )

        battery_bar.set(
        battery.percent / 100
        )

    if battery.percent >= 70:

        battery_bar.configure(
            progress_color="green"
        )

    elif battery.percent >= 40:

        battery_bar.configure(
            progress_color="yellow"
        )

    else:

        battery_bar.configure(
            progress_color="red"
        )

else:

    battery_label.configure(
        text="Battery: Not Detected"
    )

    battery_bar.set(0)

update_stats()

app.mainloop()