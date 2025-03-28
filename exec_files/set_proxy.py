import random


from galaxi_android_lib.networks import Network
from galaxi_android_lib import utils
from database_manager import sql_methods
from time import sleep
from utils import utils_methods

import os
from threading import Thread
from pymsgbox import alert
import requests




def main(serial, proxy_data:dict):
    while True:
        try:
            #auth_server = 'http://217.15.171.93:8089'
            #proxy_server = 'http://217.15.171.93:8092'
            #webshare_api_key = requests.get(auth_server + '/wsp').json().get('code')

            #country = sql_methods.get_setting('proxy_country')
            #credentials = sql_methods.get_credentials()
            #uuid_ = utils_methods.get_system_uuid()

            """proxies = requests.get(proxy_server + f'/get_proxy_by_country/{country}', headers={
                'Email':credentials['email'],
                "Password":credentials['password'],
                "uuid":uuid_

            }).json().get('proxies')"""

            while True:
                my_proxy = random.choice(proxy_data)
                print(my_proxy)

                network = Network(serial)
                if network.proxy_connect(
                    my_proxy.get('ip'),
                    my_proxy.get('port'),
                    my_proxy.get('username'),
                    my_proxy.get('password')
                    ):
                    break

            sleep(5)
            print("Device connected")
            return True

        except Exception as e:
            print(f"Error: {e}")
            #alert(title='Proxy error', text=f"Error connecting to proxy: {e}")
            sleep(5)




if __name__ == '__main__':
    # validation -------------------------
    from utils.utils_methods import get_system_uuid
    from token__ import validate_jwt
    import json

    data_path = "c:/AndroRPA/data"
    with open(f"{data_path}/token.json", 'r', encoding="utf-8") as f:
        token_data = json.load(f)
        jwt_token = token_data.get('token')

    system_uuid = get_system_uuid()
    r = validate_jwt(jwt_token, system_uuid)
    if not r['is_valid']:
        alert(title="Invalid token", text="Invalid token")
        exit(1)

    # -------------------------------------
    try:
        """data = [{
            "ip": "46.232.4.0",
            "port": 50101,
            "username": "spuffyproxy",
            "password": "spuffy"
        }]"""

        data_path = 'c:/AndroRPA/data'
        with open(f"{data_path}/proxys_file.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
            text_file_path = data['proxys_file']

        with open(text_file_path, "r") as f:
            proxy_data = [line.strip().split(':') for line in f]
            proxy_data = [{'ip': ip, 'port': int(port), 'username': username, 'password': password} for ip, port, username, password in proxy_data]

        print(proxy_data)


        threads = []
        for serial in utils.list_devices():
            t = Thread(target=main, args=(serial,proxy_data))
            threads.append(t)
            t.start()

        for thread in threads:
            thread.join()

        alert(title='Proxy connected', text='Connected successfully in all devices')
    except Exception as e:
        print(f"Error: {e}")
        alert(title='Error', text=f"Error connecting to proxy: {e}")
