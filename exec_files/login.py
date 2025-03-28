from exec_files.AndroRPA.core import device, actions
from exec_files.AndroRPA.platforms.spotify import connection, auth, utils, interactions

from time import sleep
from random import choice, randint

import json
import jwt

import uiautomator2

from exec_files.database_manager import sql_methods

def main(serial, subscription='basic'):
    auth_spt = auth.Authentication(serial, subscription)
    action = actions.Actions(serial)

    action.unlock()
    package_name_list = auth_spt.spotify_apps_package_list
    action.lock_screen_rotation()

    for package_name in package_name_list:
        auth_spt.device_from_core.device.app_stop(package_name)

    auth_spt.device_from_core.device.app_stop('com.android.chrome')

    for app in package_name_list:
        print(f"Current package: {app}")
        while True:
            accounts_pool = sql_methods.get_all_accounts_by_state('inactive')
            if not accounts_pool or accounts_pool is None:
                print('No inactive accounts found. Waiting for new accounts...')
                return
            account = choice(accounts_pool)
            print(f'Selected account: {account}')

            result_try = auth_spt.login(app, account['email'], account['password'])
            email_result = result_try[1]

            if email_result:
                sql_methods.update_account(email_result, state='inactive')
                print(f'Successfully update old account: {account["email"]}')

            if result_try[0]:
                sql_methods.update_account(account['email'], state='active')
                print(f'Successfully logged in with account: {account["email"]}')
                break
            else:
                print(f'Failed to login with account: {account["email"]}')
                sql_methods.update_account(account['email'], state='bad')


if __name__ == "__main__":
    from pymsgbox import alert
    from threading import Thread

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

    # -------------------------------------


    # -------------------------------------
    try:

        """threads = []
        for serial in device.Device.get_all_devices():
            t = Thread(target=main, args=(serial,))
            threads.append(t)
            t.start()

        for thread in threads:
            thread.join()"""

        for serial in device.Device.get_all_devices():
            print(f'Starting on device: {serial}')
            main(serial)

        alert(title='Auth', text='Login successfully in all devices')
    except Exception as e:
        print(f"Error: {e}")
        alert(title='Error', text=f"Error in login module: {e}")


