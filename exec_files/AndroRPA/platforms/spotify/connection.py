from time import sleep

from exec_files.AndroRPA.core import device, settings, utils, actions
from exec_files.AndroRPA.platforms.spotify.utils import spotify_alert
import uiautomator2

class Connection:
    def __init__(self, device_serial):
        self.device_serial = device_serial
        self.device_from_core = device.Device(device_serial)
        self.device_from_uiautomator2 = uiautomator2.connect(device_serial)
        self.action = actions.Actions(self.device_serial)

    def start_spotify(self, package_name):
        try:
            self.device_from_core.device.app_start(package_name)
            self.action.lock_screen_rotation()
            while True:
                if self.device_from_uiautomator2(packageName=package_name).exists:
                    sleep(5)
                    spotify_alert(self.device_serial, package_name)
                    return True
                sleep(3)
        except Exception as e:
            print(f"Error starting Spotify: {e}")
            return False

    def stop_spotify(self, package_name):
        try:
            self.device_from_core.device.app_stop(package_name)
            return True
        except Exception as e:
            print(f"Error stopping Spotify: {e}")
            return False

    def clear_spotify_data(self, package_name):
        try:
            self.device_from_core.device.app_clear(package_name)
            return True
        except Exception as e:
            print(f"Error clearing Spotify data: {e}")
            return False

    def open_url_spotify(self, package_name, url):
        try:
            self.device_from_core.open_url(url, package_name, '.MainActivity')
            self.action.lock_screen_rotation()
            while True:
                if self.device_from_uiautomator2(packageName=package_name).exists:
                    sleep(5)
                    spotify_alert(self.device_serial, package_name)
                    return True
                sleep(3)

        except Exception as e:
            print(f"Error opening Spotify URL: {e}")
            return False






if __name__ == '__main__':
    app = Connection('VCO7MFXWCIN7NVQW')
    #app.stop_spotify('com.spotify.musia')
    app.open_url_spotify('com.spotify.musia', 'https://open.spotify.com/intl-es/track/5uUNiapLuqoaAYHCc0nwB8?si=c0aedc7c0f2043d9')