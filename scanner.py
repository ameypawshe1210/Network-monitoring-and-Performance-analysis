import os

network = "192.168.1."

active_devices = []

for i in range(1,255):
    ip = network + str(i)

    response = os.system("ping -n 1 -w 100 " + ip)

    if response == 0:
        active_devices.append(ip)
        print(ip,"is active")

print("Active devices:",active_devices)
