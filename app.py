import json
from threading import Thread

from database_manager.sql_methods import data_path, exec_path
from galaxi_android_lib.utils import list_devices
from spotify_android_lib.spotify import Spotify
import uiautomator2

from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QGroupBox, QFormLayout, QLabel, QLineEdit, QTextEdit,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QFileDialog)

from utils import utils_methods
from PyQt6.uic import loadUi
import sys
import os
import jwt
import requests

from datetime import datetime

login_server_url = "http://217.15.171.93:8089/verify"
server_url = "http://217.15.171.93:8089/"
jwt_key='galaxibyte2025@'



from database_manager import sql_methods
from pymsgbox import alert
"""
class VersionAlert(QWidget):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(os.getcwd(), 'assets', 'version_alert.ui'), self)


"""
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(os.getcwd(), 'assets', 'login.ui'), self)
        self.setFixedSize(370, 600)

        '''self.setStyleSheet(f"""
                    #widget_8 {{
                        background-image: url("assets/bg.jpg");
                        background-position: center;
                        background-repeat: no-repeat;
                        background-size: cover;
                    }}
                """)'''

        self.login_btn = self.findChild(QPushButton, 'pushButton')
        #self.email_lineedit = self.findChild(QLineEdit, 'lineEdit')
        self.token_lineedit = self.findChild(QLineEdit, 'lineEdit')
        #self.password_lineedit = self.findChild(QLineEdit, 'lineEdit_2')

        self.charge_exist_credentials()
        self.login_btn.clicked.connect(self.login_user)

    def version_check(self):
        self.software_version_ = '0.1.2'

        # version alert
        version_request = requests.get(server_url + 'version')
        version_data = version_request.json().get('version')
        if version_data != self.software_version_:
            return False
        else:
            return True

    def charge_exist_credentials(self):
        try:
            credentials = sql_methods.get_credentials()
            if credentials:
                self.token_lineedit.setText(credentials['token'])
                #self.email_lineedit.setText(credentials['email'])
                #self.password_lineedit.setText(credentials['password'])
        except Exception as e:
            print(f'Error charge credentials: {str(e)}')

    def login_user(self):
        """if not self.version_check():
            alert(title='Update', text='New version available.\nPlease contact support to \nget the new version of Spuffy.')
            return"""

        #email = self.email_lineedit.text()
        #password = self.password_lineedit.text()
        token = self.token_lineedit.text()

        """if not email or not password:
            alert(title='Error', text='Isert email and password.')
            return"""
        if not token:
            alert(title='Error', text='Insert you Token.')
            return

        data = {
            #'Email': email,
            #'Password': password,
            'uuid': utils_methods.get_system_uuid(),
            'token': token
        }

        """try:
            r = requests.post(login_server_url, headers=data)
            if r.status_code == 200:
                sql_methods.update_credentials(email, password)

                # charged user date
                rqs_username = ''
                rqs_email = ''
                rqs_expired_date = ''
                rqs_plan = ''

                _request = requests.get(server_url + f'get_user/{email}')
                __request = requests.get(server_url + f'get_linked_clients/{email}')
                user_data = _request.json()
                linked_users_data = __request.json()

                #print(user_data)
                #print(linked_users_data)
                for linked_user in linked_users_data:
                    if linked_user['uuid'] == utils_methods.get_system_uuid():
                        rqs_username = linked_user['username']

                rqs_plan = user_data[0]['plan']
                rqs_expired_date = user_data[0]['expiration_date']
                rqs_email = user_data[0]['email']

                sql_methods.update_user(rqs_username, rqs_email, rqs_plan, rqs_expired_date)

                # ------------------

                alert(title='Login', text='Login successful!')
                self.close()
                self.main_window = MainWindow()
                self.main_window.show()
            else:
                alert(title='Error', text=f'Login error: {r.text}')
        except Exception as e:
            print(f'Error login: {str(e)}')"""

        try:
            from token__ import validate_jwt
            result = validate_jwt(data['token'], data['uuid'])
            user_data_json = {
               "username":result['username'],
                "email":result["email"],
                "remaining_days": result["remaining_days"],
                "subscription":result["subscription"]
            }
            if result['is_valid']:
                with open(f'{data_path}/token.json', 'w', encoding='utf-8') as file_:
                    json.dump(data, file_, ensure_ascii=False, indent=4)

                with open(f'{data_path}/user_data.json', 'w', encoding='utf-8') as user_data_json__:
                    json.dump(user_data_json, user_data_json__, ensure_ascii=False, indent=4)

                alert(title='Login', text='Login successful!')
                self.close()
                self.main_window = MainWindow()
                self.main_window.show()
            else:
                alert(title='Access denied', text='Invalid Token')

        except Exception as e:
            print(f'Error in the token validation: {e}')
            alert(title='Expired Token', text='You token Expired')



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(os.getcwd(), 'assets','home.ui'), self)
        self.setFixedSize(370, 600)
        #self.check_spuffy_path = os.path.join(os.getcwd(), 'exec_files')
        #utils_methods.open_executable(self.check_spuffy_path, 'spuffy_check.exe')

        # profile bar
        self.profile_username_label = self.findChild(QLabel, 'label_2')
        self.profile_email_label = self.findChild(QLabel, 'label_3')

        self.view_profile_info = self.findChild(QPushButton, 'pushButton')

        # profile bar manager events
        self.charge_user_info()
        self.view_profile_info.clicked.connect(self.view_profile_info_clicked)

        # views manager
        self.main_widget = self.findChild(QWidget, 'widget_5')
        self.files_widget = self.findChild(QWidget, 'widget_6')
        self.settings_widget = self.findChild(QWidget, 'widget_13')

        # switches buttons
        self.main_widget_btn = self.findChild(QPushButton, 'pushButton_2')
        self.files_widget_btn = self.findChild(QPushButton, 'pushButton_3')
        self.settings_widget_btn = self.findChild(QPushButton, 'pushButton_4')

        # switch views
        self.files_widget.hide()
        self.settings_widget.hide()

        # switch views events
        self.main_widget_btn.clicked.connect(self.switch_to_main_widget)
        self.files_widget_btn.clicked.connect(self.switch_to_files_widget)
        self.settings_widget_btn.clicked.connect(self.switch_to_settings_widget)


        # main widget views widget
        self.mode_label = self.findChild(QLabel, 'label_5')

        self.back_mode_btn = self.findChild(QPushButton, 'pushButton_10')
        self.next_mode_btn = self.findChild(QPushButton, 'pushButton_9')
        self.start_mode_btn = self.findChild(QPushButton, 'pushButton_7')
        self.stop_mode_btn = self.findChild(QPushButton, 'pushButton_8')

        # main widget views widget events
        self.get_current_mode()
        self.stop_mode_btn.hide()
        self.next_mode_btn.setEnabled(False)
        self.back_mode_btn.clicked.connect(self.change_mode_back)
        self.next_mode_btn.clicked.connect(self.change_mode_next)
        self.start_mode_btn.clicked.connect(self.start_mode)
        self.stop_mode_btn.clicked.connect(self.stop_mode)

        # files widget views widget
        self.tracks_label = self.findChild(QLabel, 'label_9')
        self.playlists_label = self.findChild(QLabel, 'label_24')
        self.artists_label = self.findChild(QLabel, 'label_30')
        self.accounts_label = self.findChild(QLabel, 'label_34')
        self.proxys_label = self.findChild(QLabel, 'label_37')

        self.add_track_file = self.findChild(QPushButton, 'pushButton_5')
        self.add_playlist_file = self.findChild(QPushButton, 'pushButton_15')
        self.add_artist_file = self.findChild(QPushButton, 'pushButton_17')
        self.add_accounts_file = self.findChild(QPushButton, 'pushButton_18')
        self.add_proxys_file = self.findChild(QPushButton, 'pushButton_19')

        # files widget views widget events
        self.charge_files_info()
        self.add_track_file.clicked.connect(self.add_track_file_clicked)
        self.add_playlist_file.clicked.connect(self.add_playlist_file_clicked)
        self.add_artist_file.clicked.connect(self.add_artist_file_clicked)
        self.add_accounts_file.clicked.connect(self.add_accounts_file_clicked)
        self.add_proxys_file.clicked.connect(self.add_proxys_file_clicked)


        # settings widget views widget
        self.devices_settings_btn = self.findChild(QPushButton, 'pushButton_6')

        # settings widget views widget events
        self.devices_settings_btn.clicked.connect(self.devices_settings_btn_clicked)

    # close event handlers
    def closeEvent(self, event):
        #utils_methods.kill_task_async('spuffy_check.exe')
        self.kill_all_executables()
        exit()

    # profile bar event methods
    def charge_files_info(self):
        try:

            with open(f"{data_path}/tracks_file.json", 'r', encoding='utf-8') as f:
                tracks_file = json.load(f)
            with open(f"{data_path}/playlists_file.json", 'r', encoding='utf-8') as f:
                playlists_file = json.load(f)
            with open(f"{data_path}/artists_file.json", 'r', encoding='utf-8') as f:
                artists_file = json.load(f)
            with open(f"{data_path}/accounts_file.json", 'r', encoding='utf-8') as f:
                accounts_file = json.load(f)
            with open(f"{data_path}/proxys_file.json", 'r', encoding='utf-8') as f:
                proxys_file = json.load(f)


            track_file_path = tracks_file['tracks_file']
            playlist_file_path = playlists_file['playlists_file']
            artist_file_path = artists_file['artists_file']
            accounts_file_path = accounts_file['accounts_file']
            proxies_file_path = proxys_file['proxys_file']

            self.tracks_label.setText(f'Track file: {track_file_path}')
            self.playlists_label.setText(f'Playlist file: {playlist_file_path}')
            self.artists_label.setText(f'Artist file: {artist_file_path}')
            self.accounts_label.setText(f'Accounts file: {accounts_file_path}')
            self.proxys_label.setText(f'Proxies file: {proxies_file_path}')

        except Exception as e:
            print(f'Error getting user info: {str(e)}')

    def devices_settings_btn_clicked(self):
        try:
            self.devices_settings_window = DeviceSettingsWindow()
            self.devices_settings_window.show()
        except Exception as e:
            print(f'Error opening devices settings: {str(e)}')

    # files widget views event methods
    def add_track_file_clicked(self):
        try:
            dir_, _ = QFileDialog.getOpenFileName(self, 'Open File')
            self.tracks_label.setText(f'Added: {dir_}')

            data = {
                "tracks_file": dir_
            }
            with open(f"{data_path}/tracks_file.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

        except Exception as e:
            print(f'Error adding track file: {str(e)}')

    def add_playlist_file_clicked(self):
        try:
            dir_, _ = QFileDialog.getOpenFileName(self, 'Open File')
            self.playlists_label.setText(f'Added: {dir_}')

            data = {
                "playlists_file": dir_
            }
            with open(f"{data_path}/playlists_file.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

        except Exception as e:
            print(f'Error adding playlist file: {str(e)}')

    def add_artist_file_clicked(self):
        try:
            dir_, _ = QFileDialog.getOpenFileName(self, 'Open File')
            self.artists_label.setText(f'Added: {dir_}')

            data = {
                "artists_file": dir_
            }
            with open(f"{data_path}/artists_file.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)


        except Exception as e:
            print(f'Error adding artist file: {str(e)}')

    def add_accounts_file_clicked(self):
        try:
            dir_, _ = QFileDialog.getOpenFileName(self, 'Open File')
            self.accounts_label.setText(f'Added: {dir_}')

            data = {
                "accounts_file": dir_
            }
            with open(f"{data_path}/accounts_file.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

        except Exception as e:
            print(f'Error adding accounts file: {str(e)}')

    def add_proxys_file_clicked(self):
        try:
            dir_, _ = QFileDialog.getOpenFileName(self, 'Open File')
            self.proxys_label.setText(f'Added: {dir_}')

            data = {
                "proxys_file": dir_
            }
            with open(f"{data_path}/proxys_file.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

        except Exception as e:
            print(f'Error adding proxies file: {str(e)}')


    # main widget views widget events
    def get_current_mode(self):
        mode = self.mode_label.text()
        mode_json = {
            "mode":mode
        }
        #sql_methods.update_setting('mode', mode.lower())
        with open(f'{data_path}/mode.json', 'w', encoding='utf-8') as f:
            json.dump(mode_json, f, ensure_ascii=False, indent=4)

        return mode

    def change_mode_back(self):
        if self.get_current_mode() == 'PLAY TRACKS':
            self.mode_label.setText('PLAY PLAYLISTS')
            self.get_current_mode()
            self.next_mode_btn.setEnabled(True)

        elif self.get_current_mode() == 'PLAY PLAYLISTS':
            self.mode_label.setText('PLAY ARTIST CATALOG')
            self.get_current_mode()

        elif self.get_current_mode() == 'PLAY ARTIST CATALOG':
            self.mode_label.setText('LOG IN')
            self.get_current_mode()
            self.back_mode_btn.setEnabled(False)

    def change_mode_next(self):
        if self.get_current_mode() == 'LOG IN':
            self.mode_label.setText('PLAY ARTIST CATALOG')
            self.get_current_mode()
            self.back_mode_btn.setEnabled(True)

        elif self.get_current_mode() == 'PLAY ARTIST CATALOG':
            self.mode_label.setText('PLAY PLAYLISTS')
            self.get_current_mode()

        elif self.get_current_mode() == 'PLAY PLAYLISTS':
            self.mode_label.setText('PLAY TRACKS')
            self.get_current_mode()
            self.next_mode_btn.setEnabled(False)

    def start_mode(self):
        exec_files_dir = os.path.join(exec_path)

        self.back_mode_btn.setEnabled(False)
        self.next_mode_btn.setEnabled(False)
        self.stop_mode_btn.show()
        self.start_mode_btn.hide()

        mode = self.get_current_mode().lower()
        if mode == 'play tracks':
            print('Playing tracks...')
            utils_methods.open_executable(exec_files_dir, 'track_player.exe')

        elif mode == 'play playlists':
            print('Playing playlists...')
            utils_methods.open_executable(exec_files_dir, 'playlists_player.exe')

        elif mode == 'play artist catalog':
            print('Playing artist catalog...')
            utils_methods.open_executable(exec_files_dir, 'artist_catalog_player.exe')

        elif mode == 'log in':
            print('Logging in...')
            utils_methods.open_executable(exec_files_dir, 'login.exe')

        else:
            alert(title='Error', text='Mode not found.')

            self.back_mode_btn.setEnabled(True)
            self.next_mode_btn.setEnabled(True)
            self.stop_mode_btn.hide()
            self.start_mode_btn.show()

    def stop_mode(self):
        self.back_mode_btn.setEnabled(True)
        self.next_mode_btn.setEnabled(True)
        self.stop_mode_btn.hide()
        self.start_mode_btn.show()

        self.kill_all_executables()

        # close all app process
        def stop_activity(serial):
            d = uiautomator2.connect(serial)
            apps = d.app_list('com.spotify')
            for app_ in apps:
                d.app_stop(app_)

        for serial in list_devices():
            Thread(target=stop_activity, args=(serial,)).start()
        # --------------------------

    def kill_all_executables(self):
        # TODO: kill all running executables
        utils_methods.kill_task_async('track_player.exe')
        utils_methods.kill_task_async('playlists_player.exe')
        utils_methods.kill_task_async('artist_catalog_player.exe')
        utils_methods.kill_task_async('login.exe')

        utils_methods.kill_task_async('set_proxy.exe')
        utils_methods.kill_task_async('required_app_setup.exe')
        #utils_methods.kill_task_async('spuffy_check.exe')

    # switch views events methods
    def switch_to_main_widget(self):
        self.main_widget.show()
        self.files_widget.hide()
        self.settings_widget.hide()

    def switch_to_files_widget(self):
        self.main_widget.hide()
        self.files_widget.show()
        self.settings_widget.hide()

    def switch_to_settings_widget(self):
        self.main_widget.hide()
        self.files_widget.hide()
        self.settings_widget.show()

    # profile bar events
    def charge_user_info(self):
        with open(f'{data_path}/user_data.json', 'r', encoding='utf-8') as file___:
            data = json.load(file___)
        if data:
            self.profile_username_label.setText(data['username'])
            self.profile_email_label.setText(data['email'])

    def view_profile_info_clicked(self):
        try:
            with open(f'{data_path}/user_data.json', 'r', encoding='utf-8') as file___:
                data = json.load(file___)
            print(data)
            date__ = data['remaining_days']

            alert(title='Profile Information', text=f"""
                    Hello {data['username']}!\n
                    You have a {data['subscription']} plan.
                    Your account expires on {date__} days.
                    """)
        except Exception as e:
            print(f'Error view profile info: {str(e)}')

class DeviceSettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(os.getcwd(), 'assets', 'devices_settings.ui'), self)
        self.setFixedSize(370, 600)

        self.killer_task_btn = self.findChild(QPushButton, 'pushButton')
        self.killer_task_btn.clicked.connect(self.kill_all_executables)

        # proxy settings widget
        self.start_proxy_btn = self.findChild(QPushButton, 'pushButton_2')
        self.proxy_option_combo = self.findChild(QComboBox, 'comboBox')

        self.proxy_option_combo.currentIndexChanged.connect(self.proxy_option_combo_changed)
        self.start_proxy_btn.clicked.connect(self.start_proxy_clicked)

        # required app setup widget
        self.start_required_app_btn = self.findChild(QPushButton, 'pushButton_4')
        self.start_required_app_btn.clicked.connect(self.start_required_app_clicked)

    # required app setup event methods
    def start_required_app_clicked(self):
        executable_path = os.path.join(os.getcwd(), 'exec_files')
        alert(title='Required App Setup', text='Starting required app setup...')
        utils_methods.open_executable(executable_path,'required_app_setup.exe')


    # proxy settings event methods
    def proxy_option_combo_changed(self, index):
        country = self.proxy_option_combo.currentText()
        sql_methods.update_setting('proxy_country', country)

    def start_proxy_clicked(self):
        executable_path = os.path.join(os.getcwd(), 'exec_files')
        alert(title='Proxy Settings', text=f'Starting proxy for {self.proxy_option_combo.currentText()}...')
        utils_methods.open_executable(executable_path,'set_proxy.exe')



    def kill_all_executables(self):
        # TODO: kill all running executables
        utils_methods.kill_task_async('track_player.exe')
        utils_methods.kill_task_async('playlists_player.exe')
        utils_methods.kill_task_async('artist_catalog_player.exe')
        utils_methods.kill_task_async('login.exe')

        utils_methods.kill_task_async('set_proxy.exe')
        utils_methods.kill_task_async('required_app_setup.exe')
        #utils_methods.kill_task_async('spuffy_check.exe')


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = LoginWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f'Error occurred: {str(e)}')
        alert(text='Sorry error occurred', title='Error occurred')

