import os
import adbutils
import uiautomator2
import subprocess

from time import sleep


# adb methods
# -- List all connected devices
def list_devices():
    list_devices = []
    for device in adbutils.adb.device_list():
        list_devices.append(device.serial)

    return list_devices


# -- connect all devices to tcp port
def connect_devices_to_tcp_port(devices_serial_list=None, port=5555, timeout=10):
    try:
        if devices_serial_list is None:
            devices_serial_list = list_devices()

        try:
            for device_serial in devices_serial_list:  # loop through each device
                command = f'adb -s {device_serial} tcpip {port}'
                subprocess.Popen(command, shell=True)

            sleep(timeout)  # wait for adb to connect to devices
        except Exception as e:
            print(f'Error: {e}')

        devices_ip_list = []
        for device_serial in devices_serial_list:  # loop for get all devices ip
            d = uiautomator2.connect(device_serial)
            device_ip = d.wlan_ip
            devices_ip_list.append(device_ip)

        print(devices_ip_list)

        # connect all devices to tcp port
        for ip in devices_ip_list:
            command = f'adb connect {ip}:{port}'
            subprocess.Popen(command, shell=True)

        # created ip and port list for return
        devices_ip_port_list = []
        for ip in devices_ip_list:
            devices_ip_port_list.append(f'{ip}:{port}')

        return devices_ip_port_list

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    connect_devices_to_tcp_port()






