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

        while True:
            try:
                if device.xpath('//android.widget.Button[@text="Log in"]').exists:
                    break
            except Exception as e:
                print(f'Error logging in: {e}')
                sleep(5)

        device.xpath('//android.widget.Button[@text="Log in"]').click()

        # check if second button exists
        sleep(3)
        if device.xpath('//*[@text="Continue with email"]').exists:
            device.xpath('//*[@text="Continue with email"]').click()
            sleep(3)

        device(resourceId=f'{package}:id/username_text').set_text(email)
        device(resourceId=f'{package}:id/password_text').set_text(password)
        sleep(4)
        device.press('enter')

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

            if device.xpath('//android.widget.Button[@text="Log in"]').exists:
                return False

            if device(resourceId=f'{package}:id/username_text').exists:
                return False


    def spotify_logout(self, package):
        device = self.device
        self.spotify_close(package)
        self.spotify_start(package)

        # check if bluetooth button is enabled
        sleep(10)
        if device.xpath('//android.widget.Button[@text="Maybe later"]').exists:
            device.xpath('//android.widget.Button[@text="Maybe later"]').click()

        while True:
            if device.xpath('//android.widget.Button[@text="Log in"]').exists:
                return False

            if device.xpath('//android.widget.Button[@text="Maybe later"]').exists:
                device.xpath('//android.widget.Button[@text="Maybe later"]').click()
                break

            if device.xpath(f'//*[@resource-id="{package}:id/home_tab"]').exists:
                break

        try:
            self.get_better_recommendation_frame(package)
            sleep(5)
        except Exception as e:
            print(f'Error getting better recommendation frame: {e}')


        device.xpath(f'//*[@resource-id="{package}:id/faceheader_image"]').click()
        device.xpath('//android.widget.TextView[@text="Settings and privacy"]').click()

        # get email
        email = (device(resourceId='android:id/list').child(index=2, className='android.widget.FrameLayout')
                 .child(index=0).child(index=0).child(index=1).get_text())

        while True:
            device(resourceId='android:id/list').swipe('up', steps=2)
            if device.xpath('//android.widget.TextView[@text="Log out"]').exists:
                device(resourceId='android:id/list').swipe('up', steps=2)
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
        if self.device.xpath(f'//*[@resource-id="{package}:id/browseButton"]').exists:
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
        print(f'User plan: {user_plan}')
        my_app_lists = []
        apps = self.device.app_list('com.spotify')
        print(f'Spotify app lists: {apps}')

        if user_plan == 'basic':
            for num, app in enumerate(apps):
                if num <= 1:
                    my_app_lists.append(app)

        elif user_plan == 'premium':
            for num, app in enumerate(apps):
                if num <= 3:
                    my_app_lists.append(app)

        elif user_plan == 'pro':
            for num, app in enumerate(apps):
                if num <= 5:
                    my_app_lists.append(app)

        elif user_plan == 'admin':
            for num, app in enumerate(apps):
                if num <= 5:
                    my_app_lists.append(app)

        return my_app_lists



if __name__ == "__main__":
    device = Spotify('ZPIVJB9SQOCYI74T')
    #device.device.app_clear('com.spotify.music')
    #print(device.app_lists)
    #device.open_url_in_spotify('https://auth-callback.spotify.com/r/android/music/login?sessionId=efc3042c-d891-49c5-8823-accde7b530b5-5&interact_ref=5XUBBDHFA7YI6KOLLHDC6XLPEE&hash=HxOOsC6iH-7LdmnpOdS2IuEM5LUY_zYBD5kLJL_84HC1FX4_XQq-oNMsZij7679QBPro1Clyd7oR9_erUdjeKg&flow_ctx=0ead7267-0066-43ec-91af-c08a07062361', 'com.spotify.music')
    #device.open_url('https://auth-callback.spotify.com/r/android/music/login?sessionId=fbd8f0a1-4582-4f39-8ef9-b7d15d871fc1-5&interact_ref=XJ6NIC3KNVRIW7Q26GGXS4B65Y&hash=IWDq8gT0WA6-MuWZKvs7adUHryPfUAQ02SMxBmnEJkLcVuYEIT_g6ITKs_7eo7rqv7rgDjq4G-4q1FehpehaSg&flow_ctx=aa1458f0-e1f4-4fdc-af9c-9c5939c37466')

    #device.open_url_in_spotify('https://open.spotify.com/intl-es/track/1a0AIAK11kXO3pLeBMl0nY', 'com.spotify.musig')
    #device.spotify_logout('com.spotify.musid')
    #device.spotify_login('grandes0455@mailto.plus', 'maravilla2', 'com.spotify.musid')
    #device.spotify_logout('com.spotify.musim')
    #device.spotify_play_artists_catalog('https://open.spotify.com/intl-es/artist/1HcAkAeL4xf02wzAnl7mIV', 'com.spotify.musig')