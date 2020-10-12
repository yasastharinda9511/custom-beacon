import os
import time
os.system("iwconfig")
time.sleep(0.5)
os.system("sudo airmon-ng check kill")
time.sleep(10)
os.system("sudo airmon-ng start wlan1")
time.sleep(0.5)
os.system("sudo iw wlan1 interface add mon1 type monitor")
time.sleep(0.5)
os.system("sudo airmon-ng start mon1")
time.sleep(0.5)

os.system("sudo iwconfig mon1 channel 1")
time.sleep(0.5)

os.system("sudo iwconfig wlan1mon channel 1")
time.sleep(0.5)

print("Configured Successfully")



