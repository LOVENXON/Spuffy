from galaxi_android_lib.devices import Device
from galaxi_android_lib.utils import list_devices
from threading import Thread

def main(serial):
    d = Device(serial)
    apps = d.device.app_list('com.spotify')
    for app in apps:
        d.device.shell(f'pm grant {app} android.permission.POST_NOTIFICATIONS')

if __name__ == '__main__':
    from pymsgbox import alert
    d_list = list_devices()
    threads = []
    for d in d_list:
        t = Thread(target=main, args=(d,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    alert(title='Uninstall', text='Spotify Access successfully in all devices')
