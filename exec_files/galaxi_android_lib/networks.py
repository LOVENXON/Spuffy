import subprocess

from exec_files.AndroRPA.core.device import Device
from time import sleep
from exec_files.AndroRPA.core.actions import Actions


class Network(Device):
    def __init__(self, device_serial):
        super().__init__(device_serial)
        self.device_serial = device_serial
        self.action = Actions(device_serial)
        self.action.unlock()

    # connection verification
    def connection_verification(self):
        self.action.lock_screen_rotation()
        device_ = self.device
        device_.app_clear('com.netflix.Speedtest')
        sleep(2)
        self.device_start_apps('com.netflix.Speedtest')
        sleep(5)

        counter = 0
        while counter < 6:
            if device_.xpath('//android.widget.TextView[@text="Mbps"]').exists:
                return True

            if device_.xpath('//*[@resource-id="speed-units"]').exists:
                return True

            if device_.xpath('//*[@resource-id="speed-value"]').exists:
                speed = device_.xpath('//*[@resource-id="speed-value"]').get_text()
                try:
                    if int(speed) >= 1:
                        return True
                except Exception as e:
                    try:
                        if int(round(speed)) >= 1:
                            return True
                    except Exception as e:
                        pass

            if device_.xpath('//android.widget.TextView[@text="* Could not reach our servers to perform the test. You may not be connected to the internet"]').exists:
                return False

            sleep(10)
            counter += 1

        return False


    # wi-fi settings
    def wifi_connect(self, ssid, password, password_type='WPA'):
        if password_type == 'DEFAULT':
            password_type = 'WPA'

        device_ = self.device
        device_.shell(
            f"am start -n com.steinwurf.adbjoinwifi/.MainActivity -e ssid {ssid} -e password_type {password_type} -e password {password}")
        sleep(5)
        device_.app_stop('com.steinwurf.adbjoinwifi')
        return True

    # proxy settings
    def proxy_connect(self, proxy_ip, proxy_port, proxy_user, proxy_password):
        device_ = self.device
        self.action.lock_screen_rotation()

        while True:
            try:
                device_.app_clear('net.typeblog.socks')
                #device_.shell('pm grant net.typeblog.socks android.permission.POST_NOTIFICATIONS')
                self.device_start_apps('net.typeblog.socks')
                self.action.lock_screen_rotation()

                # insert data
                device_.xpath('//*[@text="Server IP"]').click()

                device_(resourceId='android:id/edit').send_keys(proxy_ip)
                sleep(1)
                device_.xpath('//*[@text="OK"]').click()
                sleep(1)
                device_.xpath('//*[@text="Server Port"]').click()
                sleep(1)
                device_(resourceId='android:id/edit').send_keys(proxy_port)
                sleep(1)
                device_.xpath('//*[@text="OK"]').click()
                sleep(1)

                device_(resourceId='android:id/decor_content_parent').swipe('up', steps=50)

                #device(resourceId='android:id/widget_frame', index=1).click()
                for i in range(5):
                    device_(text='Username & Password Authentication', index=0).click()
                    device_.xpath('//android.widget.TextView[@text="Username"]').click()

                    sleep(2)
                    if device_(resourceId='android:id/edit').exists:
                        device_(resourceId='android:id/edit').send_keys(proxy_user)
                        break

                #device_(text='Username & Password Authentication', index=0).click()
                #device_(text='Username & Password Authentication', index=0).click()
                sleep(2)

                device_.xpath('//android.widget.TextView[@text="Username"]').click()
                device_(resourceId='android:id/edit').send_keys(proxy_user)
                sleep(1)
                device_.xpath('//*[@text="OK"]').click()
                sleep(1)

                device_.xpath('//android.widget.TextView[@text="Password"]').click()
                device_(resourceId='android:id/edit').send_keys(proxy_password)
                sleep(1)
                device_.xpath('//*[@text="OK"]').click()
                sleep(2)

                # start the connection
                device_(resourceId='net.typeblog.socks:id/switch_action_button', checked=False).click()

                sleep(10)
                if device_.xpath('//*[@text="OK"]').exists:
                    device_.xpath('//android.widget.Button[@text="OK"]').click()
                    sleep(5)

                if self.connection_verification():
                    device_.press('home')
                    return True
                else:
                    return False

            except Exception as e:
                print(f'Error connecting to proxy: {e}')


    def proxy_stop(self):
        device_ = self.device
        device_.app_stop('com.txthinking.brook')
        print('proxy stopped')
        return True

    def proxy_switch(self):
        device_ = self.device
        self.device_start_apps('com.txthinking.brook')
        sleep(3)
        device_.xpath('//android.widget.Button[@text="Stop"]').click()
        sleep(5)
        device_.xpath('//android.widget.Button[@text="Start"]').click()
        sleep(3)
        if device_.xpath('//*[@text="Connection request"]').exists:
            device_.xpath('//android.widget.Button[@text="OK"]').click()

        while True:
            if device_.xpath('//android.widget.Button[@text="Stop"]').exists:
                break

        print('proxy switch to start')
        return True


if __name__ == '__main__':
    device = Network('R9HNA06388J')
    device.proxy_connect('p.webshare.io', 80, 'mrcwgsyw-DO-1209', 'kljbbyogu41k')
    #print(device.connection_verification())
    #device.wifi_connect('STARLINK', '123123123')



