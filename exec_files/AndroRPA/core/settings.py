import shutil

from markdown_it.rules_block import reference

from exec_files.AndroRPA.core.utils import download, delete_file, add_environment_value
import os
import uiautomator2


# files paths
src_path = 'C:/AndroRPA'
assets_path = 'C:/AndroRPA/assets'
cache_path = 'C:/AndroRPA/cache'
apps_path = 'C:/AndroRPA/apps'
databases_path = 'C:/AndroRPA/data'
platform_tools_path = 'C:/AndroRPA/platform-tools'

# urls
platform_tools_zip_url = 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip'
assets_zip_url = ''



def config():
    try:
        # create directory
        os.mkdir(src_path)
        os.mkdir(apps_path)
        os.mkdir(databases_path)

        # download files
        download(platform_tools_zip_url, cache_path)
        download(assets_zip_url, cache_path)

        # extract files
        shutil.unpack_archive(f'{cache_path}/platform-tools-latest-windows.zip', src_path)
        shutil.unpack_archive(f'{cache_path}/assets.zip', src_path)

        # delete downloaded files
        delete_file(f'{src_path}/platform-tools-latest-windows.zip')
        delete_file(f'{src_path}/assets.zip')

        # add required environment
        add_environment_value('Path', platform_tools_path)

        return True

    except Exception as e:
        print(f'Error: {e}')
        return False

def if_config():
    if os.path.exists(src_path):
        return True
    else:
        return False


def device_config(device):
    try:
        device = uiautomator2.connect(device)

        # disable playstore
        device.shell('pm disable-user --user 0 com.android.vending')

        # install required apps
        device.app_install(os.path.join(assets_path, 'fast.apk'))  # network speed test apk
        device.app_install(os.path.join(assets_path, 'socksdroid.apk'))  # proxy apk
        device.app_install(os.path.join(apps_path, 'wifi.apk'))  # wifi apk

        # grand permissions
        app_package_list = [
            'com.netflix.Speedtest',
            'com.steinwurf.adbjoinwifi',
            'net.typeblog.socks'
        ]

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

        for app in app_package_list:
            for permission in permissions:
                device.shell(f'pm grant {app} android.permission.{permission}')
                print(f'Granded permission: {permission} to {app}')

        return True

    except Exception as e:
        print(f'Error: {e}')
        return False

def if_device_config(device):
    try:
        device = uiautomator2.connect(device)
        reference_app_package = 'com.netflix.Speedtest'

        if device.app_list(reference_app_package):
            return True
        else:
            return False

    except Exception as e:
        print(f'Error: {e}')
        return False















