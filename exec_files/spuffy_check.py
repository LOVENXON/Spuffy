from time import sleep

from pymsgbox import alert

from database_manager.sql_methods import get_credentials
import requests
from utils.utils_methods import get_system_uuid, kill_task_async

server_url = 'http://217.15.171.93:8089/verify'
def main():
    while True:
        try:
            credentials = get_credentials()
            uuid_ = get_system_uuid()

            while True:
                r = requests.post(server_url, headers={
                    'Email': credentials['email'],
                    'Password': credentials['password'],
                    'Uuid': uuid_
                })
                if r.status_code != 200:
                    if r.status_code == 401:
                        kill_task_async('spuffy.exe')

                        kill_task_async('track_player.exe')
                        kill_task_async('playlist_player.exe')
                        kill_task_async('artist_catalog_player.exe')
                        kill_task_async('login.exe')

                        kill_task_async('set_proxy.exe')
                        kill_task_async('required_app_setup.exe')

                        alert(title='Inactive licence', text='Inactive licence')
                    else:
                        alert(title='Error', text=f'Please check your internet connection')

                sleep(120)
        except Exception as e:
            print(f"Error: {e}")
            #alert(title='Error', text=f"Error connecting to server: {e}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error occurred: {e}")







