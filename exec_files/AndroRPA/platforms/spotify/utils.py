import random
from time import sleep

import uiautomator2

# authentication
def is_logout(device_serial, package_name):
    try:
        device = uiautomator2.connect(device_serial)
        if device(resourceId=f'{package_name}:id/value_proposition_textview').exists:
            print('device is logout')
            return True
        else:
            print('device is not logout')
            return False

    except Exception as e:
        print(f"Error in check: {e}")
        return False

def google_save_password_alert_exists(device_serial):
    try:
        device = uiautomator2.connect(device_serial)
        if device(resourceId='android:id/autofill_save').exists:
            print('Google Save Password Alert exists')

            device(resourceId='android:id/autofill_save_no').click()
            return True
        else:
            print('Google Save Password Alert does not exist')
            return False
    except Exception as e:
        print(f"Error in check: {e}")
        return False


# spotify_alert
def spotify_alert(device_serial, package_name):
    try:
        device = uiautomator2.connect(device_serial)
        if device(resourceId=f'{package_name}:id/dismiss_text').exists:
            print('Spotify Alert exists')
            device(resourceId=f'{package_name}:id/close').click()
            return True
        else:
            print('Spotify Alert does not exist')
            return False
    except Exception as e:
        print(f"Error in check spotify alert: {e}")
        return False

def artist_select(device_serial, package_name):
    try:
        device = uiautomator2.connect(device_serial)
        if device(resourceId=f'{package_name}:id/expanded_title', className='android.widget.TextView', index=0).exists:

            device = device
            for i in range(random.randint(15, 20)):
                try:
                    device(resourceId=f'{package_name}:id/picker_recycler_view').child(index=random.randint(0, 6)).click()
                    sleep(1)
                except Exception as e:
                    print(f"Error selecting artist: {e}")
                    continue

            sleep(3)
            device.xpath('//android.widget.Button[@text="Done"]').click()
            sleep(3)
            device.xpath('//android.widget.Button[@text="Start Listening"]').click()
            sleep(3)
            print("Artist selected and started listening")
            return True
        else:
            print('Artist selection does not exist')
            return False

    except Exception as e:
        print(f"Error in check artists select: {e}")
        return False

def use_profile_without_country_alert(device_serial, package_name):
    try:
        device = uiautomator2.connect(device_serial)
        if device(resourceId=f'{package_name}:id/button_positive', index=1, text='OK').exists:
            print('Use Profile Without Country Alert exists')
            device.xpath('//*[@text="OK"]').click()
            sleep(5)
            device(resourceId=f'{package_name}:id/login_button').click_exists()
            return True
        else:
            print('Use Profile Without Country Alert does not exist')
            return False
    except Exception as e:
        print(f"Error in check: {e}")
        return False