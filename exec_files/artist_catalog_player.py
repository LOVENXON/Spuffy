import random
from time import sleep

from spotify_android_lib.spotify import Spotify
from galaxi_android_lib.utils import list_devices
from database_manager import sql_methods
from pymsgbox import alert
import os

def main(serial):
    while True:
        try:
            device = Spotify(serial)

            # load artists catalog lists
            catalogs = []
            with open(sql_methods.get_setting('artists_file'), 'r') as f:
                for catalog in f.readlines():
                    catalogs.append(catalog.strip())

            # start listening music
            ready_apps = []
            while True:
                for app in device.app_lists:
                    try:
                        # check if app is ready to play music
                        app_is_already = True

                        device.spotify_start(app)
                        while True:
                            if device.device.xpath(f'//android.widget.Button[@text="Log in"]').exists:
                                device.spotify_close(app)
                                app_is_already = False
                                break
                            if device.device.xpath(f'//*[@content-desc="Search"]').exists:
                                app_is_already = True
                                break

                        if app_is_already:
                            device.spotify_play_artists_catalog(random.choice(catalogs), app)
                            device.device.sleep(random.randint(5, 10))
                            device.device.press('home')
                            ready_apps.append(app)

                    except Exception as e:
                        print(f"Error playing music: {e}")
                        device.spotify_close(app)
                        pass

                # second step for play catalog on device
                while True:
                    for app in ready_apps:
                        try:
                            device.spotify_play_artists_catalog(random.choice(catalogs), app)
                            device.device.sleep(random.randint(5, 10))
                            device.device.press('home')
                            break
                        except Exception as e:
                            print(f"Error playing music: {e}")
                            device.spotify_close(app)
                            pass
                    device.spotify_start(random.choice(ready_apps))
                    device.device.sleep(random.randint(10, 20))
        except Exception as e:
            print(f"Error {e}")


if __name__ == "__main__":
    try:
        from threading import Thread

        thread_list = []
        if len(list_devices()) > 0:
            for serial in list_devices():
                thread = Thread(target=main, args=(serial,))
                thread_list.append(thread)
                thread.start()

            for thread in thread_list:
                thread.join()
        else:
            alert(title='Error', text='No devices available')

    except Exception as e:
        print(f"Error: {e}")
        alert(title='Error', text='Failed to start the Mode')

