import random
from time import sleep
from exec_files.AndroRPA.platforms.spotify import playback, connection
from exec_files.AndroRPA.platforms.spotify.auth import Authentication
from spotify_android_lib.spotify import Spotify
from galaxi_android_lib.utils import list_devices
import json
from pymsgbox import alert

data_path = 'C:/AndroRPA/data'
def main(serial, subscription='basic'):
    while True:
        try:
            spotify = playback.Playback(serial)
            device = spotify.device
            apps_list = Authentication(serial, subscription)
            apps_list = apps_list.spotify_apps_package_list

            with open(f"{data_path}/playlists_file.json", 'r', encoding='utf-8') as f:
                playlists_data = json.load(f)
                playlists_data_text_file = playlists_data['playlists_file']

            with open(playlists_data_text_file, 'r') as f:
                playlists = [line.strip() for line in f.readlines()]

            while True:
                for app in apps_list:
                    random_playlist = random.choice(playlists)
                    spotify.play_playlist_by_url(app, random_playlist)
                    sleep(random.randint(5, 10))

                sleep(random.randint(600, 800))

        except Exception as e:
            print(f"Error {e}")


if __name__ == "__main__":
    try:
        # validation -------------------------
        from utils.utils_methods import get_system_uuid
        from token__ import validate_jwt
        import json

        data_path = "c:/AndroRPA/data"
        with open(f"{data_path}/token.json", 'r', encoding="utf-8") as f:
            token_data = json.load(f)
            jwt_token = token_data.get('token')

        with open(f"{data_path}/user_data.json", 'r', encoding="utf-8") as f:
            user_data = json.load(f)
            user_subscription = user_data.get('subscription')

        system_uuid = get_system_uuid()
        r = validate_jwt(jwt_token, system_uuid)
        if not r['is_valid']:
            alert(title="Invalid token", text="Invalid token")
            exit(1)
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
        alert(title='Error', text='Failed to start the application')

