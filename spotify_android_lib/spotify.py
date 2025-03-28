import random
from operator import index
from time import sleep

import uiautomator2 as u2
from galaxi_android_lib.devices import Device
from galaxi_android_lib.networks import Network
from galaxi_android_lib import utils
from database_manager import sql_methods


class Spotify(Device):
    def __init__(self, device_serial):
        super().__init__(device_serial)
        self.app_lists = self.get_app_lists()
        self.setup_spotify()

    # set up
    def setup_spotify(self):
        for app in self.app_lists:
            self.audio_focus(app)
            sleep(2)

    # plays mode
    def spotify_play_tracks(self, url, package):
        self.open_url_in_spotify(url, package)
        sleep(4)
        if random.choice([True, False]):
            self.like_track()

        sleep(random.randint(3, 6))
        self.play_track()


    def spotify_play_playlists(self, url, package):
        self.open_url_in_spotify(url, package)
        sleep(4)
        if random.choice([True, False]):
            self.like_playlists(package)

        sleep(random.randint(3, 6))
        self.play_playlists(package)

    def spotify_play_artists_catalog(self, url, package):
        self.open_url_in_spotify(url, package)
        sleep(4)
        if random.choice([True, False]):
            self.follow_artists()

        sleep(random.randint(3, 6))
        self.play_artists()


    # app simple methods
    def spotify_close(self, package):
        self.device.app_stop(package)
        self.device.sleep(3)

    def spotify_start(self, package):
        self.device.app_start(package)
        self.device.sleep(3)

    # sessions methods
    def spotify_login(self, email, password, package):
        device = self.device
        self.spotify_close(package)
        self.spotify_start(package)
        sleep(15)

        device.xpath('//android.widget.Button[@text="Log in"]').click()

        device(resourceId=f'{package}:id/username_text').set_text(email)
        device(resourceId=f'{package}:id/password_text').set_text(password)
        sleep(2)
        device.press('enter')
        """try:
            device.xpath('//android.widget.Button[@text="Log in"]').click()
        except:
            self.device.press('back')
            sleep(5)
            device.xpath('//android.widget.Button[@text="Log in"]').click()"""

        sleep(5)

        while True:
            if device.xpath('//android.widget.Button[@text="Maybe later"]').exists:
                device.xpath('//android.widget.Button[@text="Maybe later"]').click()
                return True

            if device.xpath(f'//*[@resource-id="{package}:id/faceheader_image"]').exists:
                return True

            if device.xpath('//android.widget.TextView[@text="This email and password combination is incorrect."]').exists:
                return False

            if device.xpath('//android.widget.TextView[@text="Choose 3 or more artists you like."]').exists:
                self.artist_select(package)
                return True
            if device.xpath('//android.widget.Button[@text="Try again"]').exists:
                device.xpath('//android.widget.Button[@text="Try again"]').click()
                continue

            if device.xpath('//android.widget.Button[@text="Log in"]').exists:
                return False


    def spotify_logout(self, package):
        device = self.device
        self.spotify_close(package)
        self.spotify_start(package)
        sleep(15)

        if device.xpath('//android.widget.Button[@text="Log in"]').exists:
            return False

        if device.xpath('//android.widget.Button[@text="Maybe later"]').exists:
            device.xpath('//android.widget.Button[@text="Maybe later"]').click()

        self.get_better_recommendation_frame(package)
        sleep(5)

        device.xpath(f'//*[@resource-id="{package}:id/faceheader_image"]').click()
        device.xpath('//android.widget.TextView[@text="Settings and privacy"]').click()

        # get email
        email = (device(resourceId='android:id/list').child(index=2, className='android.widget.FrameLayout')
                 .child(index=0).child(index=0).child(index=1).get_text())

        while True:
            device(resourceId='android:id/list').swipe('up', steps=2)
            if device.xpath('//android.widget.TextView[@text="Log out"]').exists:
                device.xpath('//android.widget.TextView[@text="Log out"]').click()
                break

        print(email)
        print("Spotify logged out")
        sleep(5)
        return email

    # utils methods
    def like_track(self):
        device = self.device
        device.xpath('//*[@content-desc="Like this album"]').click_exists()

    def play_track(self):
        device = self.device
        device.xpath('//*[@content-desc="Play album"]').click_exists()

    def follow_artists(self):
        device = self.device
        device.xpath('//*[@content-desc="Follow"]').click_exists()

    def play_artists(self):
        device = self.device
        device.xpath('//*[@content-desc="Shuffle Play artist"]').click_exists()
        sleep(3)
        device.xpath(f'//*[@content-desc="Enable shuffle for this artist"]').click_exists()
        sleep(3)
        device.xpath(f'//*[@content-desc="Play artist"]').click_exists()

    def like_playlists(self, package):
        device = self.device
        device.xpath(f'//*[@resource-id="{package}:id/follow_actions_placeholder"]').click_exists()


    def play_playlists(self, package):
        device = self.device
        device.xpath(f'//*[@content-desc="Enable shuffle for this playlist"]').click_exists()
        sleep(3)
        device.xpath(f'//*[@resource-id="{package}:id/button_play_and_pause"]').click_exists()
        sleep(5)
        device.xpath(f'//*[@resource-id="{package}:id/now_playing_bar_container"]').click()
        sleep(5)
        device.xpath(f'//*[@content-desc="Shuffle tracks"]').click_exists()
        sleep(3)
        device.xpath(f'//*[@content-desc="Close"]').click()



    def artist_select(self, package):
        device = self.device
        for i in range(random.randint(15, 20)):
            try:
                device(resourceId=f'{package}:id/picker_recycler_view').child(index=random.randint(0, 6)).click()
                sleep(3)
            except Exception as e:
                print(f"Error selecting artist: {e}")
                continue

        sleep(5)
        device.xpath('//android.widget.Button[@text="Done"]').click()
        sleep(5)
        device.xpath('//android.widget.Button[@text="Start Listening"]').click()
        sleep(3)
        print("Artist selected and started listening")
        return True

    def get_better_recommendation_frame(self, package):
        if self.device.xpath('//android.widget.TextView[@text="Get better recommendations"]').exists:
            self.device.xpath('//android.widget.Button[@text="Choose Artists"]').click()
            sleep(5)
            try:
                self.artist_select(package)
            except Exception as e:
                pass

            return True

    # apps methods
    def open_url_in_spotify(self, url, app_package):
        self.open_url(url, app_package, '.MainActivity')
        self.device.sleep(5)


    def get_app_lists(self):
        user_plan = sql_methods.get_user_data().get('plan')
        my_app_lists = []
        apps = self.device.app_list('com.spotify')
        print(f'Recognize app list: {apps}')

        if user_plan == 'basic':
            for num, app in enumerate(apps):
                if num <= 3:
                    my_app_lists.append(app)

        elif user_plan == 'premium':
            for num, app in enumerate(apps):
                if num <= 10:
                    my_app_lists.append(app)

        elif user_plan == 'pro':
            for num, app in enumerate(apps):
                if num <= 30:
                    my_app_lists.append(app)

        elif user_plan == 'admin':
            for num, app in enumerate(apps):
                if num <= 30:
                    my_app_lists.append(app)

        return my_app_lists



if __name__ == "__main__":
    device = Spotify('XMOBX22111188926')
    #print(device.app_lists)
    #device.open_url_in_spotify('https://open.spotify.com/intl-es/track/1a0AIAK11kXO3pLeBMl0nY', 'com.spotify.musig')
    #device.spotify_logout('com.spotify.musig')
    device.spotify_login('grandes0455@mailto.plus', 'maravilla2', 'com.spotify.musid')
    #device.spotify_play_artists_catalog('https://open.spotify.com/intl-es/artist/1HcAkAeL4xf02wzAnl7mIV', 'com.spotify.musig')