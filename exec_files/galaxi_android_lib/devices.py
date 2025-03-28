import uiautomator2
import os

from time import sleep


class Device:
    def __init__(self, device_serial):
        self.device_serial = device_serial
        self.device = uiautomator2.connect(device_serial)



        # path to the tools
        self.base_path = os.path.abspath('C:\\galaxi_tools\\assets\\')

        # setup
        self.setup_tools()
        self.unlock()

    # references
    reference_app = 'net.typeblog.socks'


    # basic methods
    def setup_tools(self):
        app_exist = self.device.app_list('net.typeblog')
        if not app_exist:
            self.device.app_install(os.path.join(self.base_path, 'socksdroid.apk'))
            self.device.app_install(os.path.join(self.base_path, 'wifi.apk'))
            self.device.app_install(os.path.join(self.base_path, 'fast.apk'))

        print("Setup app installed")
        return True

    def unlock(self):
        self.device.app_start(self.reference_app)
        sleep(3)
        if self.device(packageName=self.reference_app).exists:
            self.device.press('home')
            print("Device unlocked")
            return True

        while True:
            self.device.screen_off()
            sleep(3)
            self.device.unlock()
            sleep(3)
            self.device.app_start(self.reference_app)
            sleep(3)
            if self.device(packageName=self.reference_app).exists:
                self.device.press('home')
                print("Device unlocked")
                return True

    # url methods
    def open_url(self, url, package=None, activity=None):
        if package and activity:
            command = f'am start -n {package}/{activity} -a android.intent.action.VIEW -d {url}'
            self.device.shell(command)
        else:
            self.device.open_url(url)

        return

    def audio_focus(self, package):
        self.device.shell(f'appops set {package} TAKE_AUDIO_FOCUS ignore')

    def app_permissions(self, package):
        self.device.shell(f'pm grant {package} android.permission.POST_NOTIFICATIONS')



if __name__ == "__main__":
    from galaxi_android_lib.utils import list_devices
    d_list = list_devices()
    device = Device(d_list[0])
    #device.unlock()
