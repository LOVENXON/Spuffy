from exec_files.AndroRPA.platforms.spotify import utils, connection, interactions
import uiautomator2
from time import sleep
from random import choice, randint


class Playback:
    def __init__(self, device_serial):
        self.device_serial = device_serial
        self.device = connection.Connection(self.device_serial)

    def play_track_by_url(self, package_name, url):
        try:
            self.device.open_url_spotify(package_name, url)
            # wait for ui charged
            sleep(10)
            # check session state
            if utils.is_logout(self.device_serial, package_name):
                print("Sorry but you are not logged")
                return False

            # process
            return True

        except Exception as e:
            print(f"Error: {e}")
            return False

    def play_playlist_by_url(self, package_name, url):
        try:
            self.device.open_url_spotify(package_name, url)
            # wait for ui charged
            sleep(10)
            # check session state
            if utils.is_logout(self.device_serial, package_name):
                print("Sorry but you are not logged")
                return False

            # process
            device_ = self.device.device_from_uiautomator2
            device_(resourceId=f'{package_name}:id/button_play_and_pause').click()
            sleep(randint(5, 10))
            device_.xpath(f'//*[@resource-id="{package_name}:id/now_playing_bar_layout"]').click()

            # click a shuffle button
            sleep(randint(5, 10))
            device_(description='Shuffle tracks').click_exists()
            return True

        except Exception as e:
            print(f"Error: {e}")
            return False

    def play_artist_by_url(self, package_name, url):
        try:
            self.device.open_url_spotify(package_name, url)
            # wait for ui charged
            sleep(10)
            # check session state
            if utils.is_logout(self.device_serial, package_name):
                print("Sorry but you are not logged")
                return False

            # process
            if choice([True, False, False]):
                self.follow_artist(package_name)

            device_ = self.device.device_from_uiautomator2
            device_(resourceId=f'{package_name}:id/button_play_and_pause').click()
            sleep(randint(5, 10))
            device_(description='Enable shuffle for this artist').click_exists()
            return True

        except Exception as e:
            print(f"Error: {e}")
            return False

    def follow_artist(self, package_name, url=None):
        try:
            if url:
                self.device.open_url_spotify(package_name, url)
                # wait for ui charged
                sleep(10)
                # check session state
                if utils.is_logout(self.device_serial, package_name):
                    print("Sorry but you are not logged")
                    return False

            # process
            device_ = self.device.device_from_uiautomator2
            device_(description='Follow').click_exists()
            device_(description='Seguir').click_exists()

            return True


        except Exception as e:
            print(f"Follow artist error: {e}")
            return False

    def save_playlist(self, package_name, url=None):
        try:
            if url:
                self.device.open_url_spotify(package_name, url)
                # wait for ui charged
                sleep(10)
                # check session state
                if utils.is_logout(self.device_serial, package_name):
                    print("Sorry but you are not logged")
                    return False

            # process
            device_ = self.device.device_from_uiautomator2
            device_(description='Add playlist to Your Library').click_exists()
            return True

        except Exception as e:
            print(f"Save playlist error: {e}")
            return False


    def add_track_to_library(self, package_name, url=None):
        try:
            if url:
                self.device.open_url_spotify(package_name, url)
                # wait for ui charged
                sleep(10)
                # check session state
                if utils.is_logout(self.device_serial, package_name):
                    print("Sorry but you are not logged")
                    return False

            # process
            device_ = self.device.device_from_uiautomator2
            device_(resourceId=f'{package_name}:id/header_layout').swipe('down', 5)
            sleep(3)
            device_(description='Add playlist to Your Library').click_exists()
            return True

        except Exception as e:
            print(f"Like track error: {e}")
            return False

if __name__ == '__main__':
    # VCO7MFXWCIN7NVQW
    p = Playback('VCO7MFXWCIN7NVQW')
    p.play_track_by_url('com.spotify.musia', 'https://open.spotify.com/intl-es/track/3J9Tk3bSu8SM9dCq0P3TIo')



