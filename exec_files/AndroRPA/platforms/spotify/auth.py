from operator import index
from pydoc import classname
from time import sleep

import uiautomator2
from exec_files.AndroRPA.core import device, utils, actions
from exec_files.AndroRPA.core.utils import delete_directory
from exec_files.AndroRPA.platforms.spotify import connection
from exec_files.AndroRPA.platforms.spotify.utils import is_logout, google_save_password_alert_exists, spotify_alert, artist_select, use_profile_without_country_alert
from exec_files.AndroRPA.platforms.spotify.config import plans

class Authentication:
    def __init__(self, device_serial, plan, accounts_type='free'):
        self.device_serial = device_serial
        self.accounts_type = accounts_type
        self.device_from_core = device.Device(device_serial)
        self.connection = connection.Connection(device_serial)
        self.plan = plan
        self.spotify_apps_package_list = self.__app_package_list()
        self.__close_apps()

    # hide class methods
    def __close_apps(self):
        for app_package in self.spotify_apps_package_list:
            self.device_from_core.device.app_stop(app_package)
        self.device_from_core.device.app_stop('com.android.chrome')

    def __app_package_list(self):
        try:
            total_app_package_list = self.device_from_core.device.app_list('spotify')
            available_apps_package_list = []

            if self.plan == 'basic':
                for app in range(plans[self.plan]):
                    available_apps_package_list.append(total_app_package_list[app])
            elif self.plan == 'premium':
                for app in range(plans[self.plan]):
                    try:
                        available_apps_package_list.append(total_app_package_list[app])
                    except Exception as e:
                        print(f'Error: {str(e)}')
                        continue

            elif self.plan == 'pro':
                for app in range(plans[self.plan]):
                    try:
                        available_apps_package_list.append(total_app_package_list[app])
                    except Exception as e:
                        print(f'Error: {str(e)}')
                        continue

            elif self.plan == 'unlimited':
                for app in range(plans[self.plan]):
                    try:
                        available_apps_package_list.append(total_app_package_list[app])
                    except Exception as e:
                        print(f'Error: {str(e)}')
                        continue

            elif self.plan == 'admin':
                for app in range(plans[self.plan]):
                    try:
                        available_apps_package_list.append(total_app_package_list[app])
                    except Exception as e:
                        print(f'Error: {str(e)}')
                        continue

            return available_apps_package_list

        except Exception as e:
            print(f'Error: {str(e)}')
            return False


    def logout(self, package_name):
        """
        Logout Spotify app
        :param package_name:
        :return: Boolean and out email or None
        """
        try:
            # check if app is already logout
            self.connection.start_spotify(package_name)
            sleep(5) # wait for ui charged
            if is_logout(self.device_serial, package_name):
                return True, None

            # logout app
            device_ = self.device_from_core.device
            device_.xpath(f'//*[@resource-id="{package_name}:id/home_tab"]').click()
            device_(resourceId=f'{package_name}:id/faceheader_image', className='android.view.ViewGroup').click()

            (device_(resourceId=f'{package_name}:id/sidedrawer_compose_view')
             .child(index=1)
             .child(index=3)
             ).click()

            if self.accounts_type == 'free':
                # get the account details
                (device_(resourceId=f'{package_name}:id/compose_view')
                 .child(index=0)
                 .child(index=0)
                 .child(index=0)
                 .child(index=2)
                 ).click()

                current_email = (device_(resourceId=f'{package_name}:id/compose_view') # find the email
                 .child(index=0)
                 .child(index=0)
                 .child(index=0)
                 .child(index=2)
                 .child(index=1)
                 ).get_text()

                device_.press('back')


                print(f'Current email: {current_email}')



                while True:
                    device_(resourceId=f'{package_name}:id/compose_view').swipe('up')
                    if (device_(resourceId=f'{package_name}:id/compose_view')
                        .child(index=0)
                        .child(index=0)
                        .child(index=0)
                        .child(index=8)
                    ).exists:
                        print('Yes, is exists')
                        if (device_(resourceId=f'{package_name}:id/compose_view')
                            .child(index=0)
                            .child(index=0)
                            .child(index=0)
                            .child(index=9)
                            ).exists:
                            device_(resourceId=f'{package_name}:id/compose_view').swipe('up', 2)
                            (device_(resourceId=f'{package_name}:id/compose_view')
                             .child(index=0)
                             .child(index=0)
                             .child(index=0)
                             .child(index=9)
                             ).click()
                            sleep(5)
                            if is_logout(self.device_serial, package_name):
                                return True, current_email


                        else:
                            device_(resourceId=f'{package_name}:id/compose_view').swipe('up', 2)
                            (device_(resourceId=f'{package_name}:id/compose_view')
                            .child(index=0)
                            .child(index=0)
                            .child(index=0)
                            .child(index=8)
                            ).click()

                        sleep(5)
                        if is_logout(self.device_serial, package_name):
                            return True, current_email

        except Exception as e:
            print(f'Error logout: {str(e)}')
            return False, None

    def login(self, package_name, email, password):
        """
        :param package_name:
        :param email:
        :param password:
        :return: a tuple with boolean value in first position and email or None value in second position.
        example: (True, email@example.com)
        """
        try:
            self.connection.stop_spotify(package_name)

            # logout check
            logout_ = self.logout(package_name)
            out_email = logout_[1]

            if logout_[0]:
                # wait for page charged
                sleep(5)
                # login logic
                device_ = self.device_from_core.device
                device_(className='android.widget.Button', index=1).click() # log in first button clicked
                device_(className='android.widget.Button', index=0).click() # email option clicked

                ###
                # enter email and password
                device_(resourceId=f'{package_name}:id/username_text').set_text(email)
                device_(resourceId=f'{package_name}:id/password_text').set_text(password)
                device_(resourceId=f'{package_name}:id/login_button').click()
                ###

                # wait for login success
                sleep(10)

                # check login success
                while True:
                    spotify_alert(self.device_serial, package_name)
                    google_save_password_alert_exists(self.device_serial)
                    artist_select(self.device_serial, package_name)
                    use_profile_without_country_alert(self.device_serial, package_name)

                    if device_(resourceId=f'{package_name}:id/home_tab').exists:
                        return True, out_email

                    if device_(resourceId=f'{package_name}:id/button_negative').exists:
                        return None, None

                    if device_(resourceId=f'{package_name}:id/button_positive').exists:
                        return False, None
            else:
                # login failed
                return False, None

        except Exception as e:
            print(f'Error login: {str(e)}')
            return False, None

if __name__ == '__main__':
    a = Authentication('VCO7MFXWCIN7NVQW', 'basic')
    app_lists = a.spotify_apps_package_list
    print(app_lists)
    b = device.Device('VCO7MFXWCIN7NVQW')

    """for app in app_lists:
        b.grand_permissions(app)
        b.audio_focus(app)"""
    """for app in app_lists:
        print(a.login(app, 'asusats3223@mailto.plus', 'asusats3223@mailto.plus1'))"""


