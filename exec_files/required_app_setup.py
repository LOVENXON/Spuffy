from galaxi_android_lib.utils import list_devices
from threading import Thread
from pymsgbox import alert
import os

from AndroRPA.core import actions, device, settings
from AndroRPA.platforms.spotify import config
import json

data_path = "C:/AndroRPA/data"

with open(f"{data_path}/user_data.json", "r", encoding="utf-8") as f:
    user_data = json.load(f)

subscription_type = user_data.get('subscription')

def main(serial):
    try:
        d = device.Device(serial)
        d = d.device
        action = actions.Actions(serial)
        #d.shell('settings put system accelerometer_rotation 0')
        #d.shell('settings put system user_rotation 0')

        if not settings.if_device_config(serial):
            settings.device_config(serial)

        config.install_required_apps(serial, subscription_type)
        action.unlock()
        d.shell('settings put system accelerometer_rotation 0')

    except Exception as e:
        print(f"Error initializing device: {str(e)}")


if __name__ == '__main__':
    try:
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


        thread_list = []
        for serial in list_devices():
            thread = Thread(target=main, args=(serial,))
            thread.start()
            thread_list.append(thread)

        for thread in thread_list:
            thread.join()

        alert(title="Installation", text="Installation successfully")

    except Exception as e:
        print(f"Error installing apps: {str(e)}")
        alert(title="Installation", text="Installation failed")



