import psutil
import time
import os
while True:
    os.system("cls")
    print("===SysPulse===\n")
    cpu=psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu}%")
    ram=psutil.virtual_memory()
    print(f"RAM Usage:{ram.percent}%")
    battery=psutil.sensors_battery()
    if battery:
        print(f"Battery: {battery.percent}%")   
    else:
        print("Battery not Detected")
    print("\n-- Storage---")
    c_drive=psutil.disk_usage("C:\\")
    print(f"C Drive:{round(c_drive.free/(1024**3),1)}GB Free of {round(c_drive.total/(1024**3),1)}GB")  
    try:
        d_drive=psutil.disk_usage("D:\\")
        print(f"D Drive:{round(d_drive.free/(1024**3),1)}GB Free of {round(d_drive.total/(1024**3),1)}GB")
    except:
        pass
    time.sleep(1)
