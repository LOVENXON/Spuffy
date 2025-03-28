from time import sleep

import uiautomator2
import adbutils
from exec_files.AndroRPA.core.utils import download, delete_file
from exec_files.AndroRPA.core.actions import Actions

# path lists
app_path = 'c:/AndroRPA/apps'

class Device:
    def __init__(self, serial_number):
        self.serial_number = serial_number
        self.actions = Actions(serial_number)
        self.device = uiautomator2.connect(serial_number)

    # class methods
    @classmethod
    def get_all_devices(cls):
        devices = []

        for device in adbutils.adb.device_list():
            devices.append(device.serial)

        return devices

    # device information
    def device_info(self):
        my_device = self.device

        info_a = my_device.info
        info_b = my_device.device_info

        my_device_info = info_a | info_b

        return my_device_info

    def device_application(self, filter_name: str = '') -> list:
        applications = self.device.app_list(filter_name)

        return applications

    # device specific methods
    def open_url(self, url, package_name, activity):
        if package_name and activity:
            command = f'am start -n {package_name}/{activity} -a android.intent.action.VIEW -d {url}'
            self.device.shell(command)
            self.actions.lock_screen_rotation()
        else:
            self.device.open_url(url)
            self.actions.lock_screen_rotation()

    def device_start_apps(self, package_name, activity=None):
        try:
            if activity is not None:
                self.device.app_start(package_name, activity)
                self.actions.lock_screen_rotation()
            else:
                self.device.app_start(package_name)
                self.actions.lock_screen_rotation()

            print("app starting")
        except Exception as e:
            print(f'Error starting apps: {str(e)}')

    def install_apk_online(self, url):
        apk_name = url.split('/')[-1]
        if download(url, app_path):
            try:
                self.device.app_install(f'{app_path}/{apk_name}')
                delete_file(f'{app_path}/{apk_name}') # Delete file after installation

                print(f'App {apk_name} installed successfully.')
                return True
            except Exception as e:
                print(f'Error installing app: {str(e)}')
                return False
        else:
            print('Failed to download the app.')
            return False

    def grand_permissions(self, app_package):
        try:
            permissions = [
                'ACCEPT_HANDOVER',
                'ACCESS_BACKGROUND_LOCATION',
                'ACCESS_COARSE_LOCATION',
                'ACCESS_FINE_LOCATION',
                'ACCESS_MEDIA_LOCATION',
                'ACCESS_NETWORK_STATE',
                'ACCESS_WIFI_STATE',
                'BLUETOOTH',
                'BLUETOOTH_ADMIN',
                'BLUETOOTH_CONNECT',
                'BLUETOOTH_SCAN',
                'BODY_SENSORS',
                'CALL_PHONE',
                'CAMERA',
                'FOREGROUND_SERVICE',
                'INTERNET',
                'MANAGE_EXTERNAL_STORAGE',
                'NFC',
                'POST_NOTIFICATIONS',
                'READ_CALENDAR',
                'READ_CALL_LOG',
                'READ_CONTACTS',
                'READ_EXTERNAL_STORAGE',
                'READ_PHONE_STATE',
                'RECEIVE_BOOT_COMPLETED',
                'RECORD_AUDIO',
                'SEND_SMS',
                'USE_FINGERPRINT',
                'VIBRATE',
                'WAKE_LOCK',
                'WRITE_CALENDAR',
                'WRITE_CONTACTS',
                'WRITE_EXTERNAL_STORAGE'
            ]

            for permission in permissions:
                self.device.shell(f'pm grant {app_package} android.permission.{permission}')
                print(f'Permission granted: {permission}')

            return True

        except Exception as e:
            print(f'Error granding permissions: {str(e)}')
            return False

    def audio_focus(self, app_package):
        try:
            self.device.shell(f'appops set {app_package} TAKE_AUDIO_FOCUS ignore')
            print('Audio focus granted.')
            return True
        except Exception as e:
            print(f'Error granting audio focus: {str(e)}')
            return False


if __name__ == "__main__":
    device_class = Device('VCO7MFXWCIN7NVQW')
    print(device_class.device_application('spotify'))
    apps = device_class.device_application('spotify')
    for app in apps:
        device_class.device.app_start(app)
        sleep(15)
