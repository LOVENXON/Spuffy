from time import sleep

import uiautomator2

class Actions:
    def __init__(self, serial_device):
        self.device = uiautomator2.connect(serial_device)
        self.reference_app = 'com.netflix.Speedtest'

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
                self.device.shell('settings put system accelerometer_rotation 0')
                return True


    def lock_screen_rotation(self):
        try:
            self.device.shell('settings put system accelerometer_rotation 0')
            print("Screen rotation locked")
            return True
        except Exception as e:
            print("Failed to lock screen rotation:", e)
            return False




