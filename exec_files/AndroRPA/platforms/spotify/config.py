from exec_files.AndroRPA.core import utils, settings, actions
from exec_files.AndroRPA.core import device as device_


import uiautomator2
import os

download_files_path = 'c:/AndroRPA/apps/spotify'

# plan list
plans = {
    'basic': 1,
    'premium': 3,
    'pro': 5,
    'unlimited': 10,
    'admin': 10

}

def install_required_apps(serial_device, plan):
    try:
        device = uiautomator2.connect(serial_device)

        # clear existing apps
        apps_list = device.app_list('spotify')
        for app in apps_list:
            device.app_uninstall(app)
            print('Removed')

        # install application by plan
        if plan == 'basic':
            try:
                device.app_install(os.path.join(download_files_path, f'{plans[plan]}.apk'))
                print(f'Basic plan installed in {serial_device} successfully.')
                return True
            except Exception as e:
                print(f'Error installing basic plan in {serial_device}: {str(e)}')
                return False

        elif plan == 'premium':
            try:
                for app in range(plans[plan]):
                    device.app_install(os.path.join(download_files_path, f'{app}.apk'))
                print(f'Premium plan installed in {serial_device} successfully.')
                return True
            except Exception as e:
                print(f'Error installing premium plan in {serial_device}: {str(e)}')
                return False

        elif plan == 'pro':
            try:
                for app in range(plans[plan]):
                    device.app_install(os.path.join(download_files_path, f'{app}.apk'))
                print(f'Pro plan installed in {serial_device} successfully.')
                return True
            except Exception as e:
                print(f'Error installing pro plan in {serial_device}: {str(e)}')
                return False

        elif plan == 'unlimited':
            try:
                for app in range(plans[plan]):
                    device.app_install(os.path.join(download_files_path, f'{app}.apk'))
                print(f'Unlimited plan installed in {serial_device} successfully.')
                return True
            except Exception as e:
                print(f'Error installing unlimited plan in {serial_device}: {str(e)}')
                return False

        elif plan == 'admin':
            try:
                for app in range(plans[plan]):
                    device.app_install(os.path.join(download_files_path, f'{app}.apk'))
                print(f'Admin plan installed in {serial_device} successfully.')
                return True
            except Exception as e:
                print(f'Error installing admin plan in {serial_device}: {str(e)}')
                return False

        # spotify app permission
        app_package_list = device.app_list('spotify')

        device_obj = device_.Device(serial_device)  # instance device class from core module

        # grant permission
        for app in app_package_list:
            device_obj.grand_permissions(app)

        # audio permission
        for app in app_package_list:
            device_obj.audio_focus(app)

        return True

    except Exception as e:
        print(f'Error occurred while installing applications: {str(e)}')
        return False




