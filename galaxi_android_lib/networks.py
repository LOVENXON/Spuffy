import subprocess

from galaxi_android_lib.devices import Device
from time import sleep


class Network(Device):
    def __init__(self, device_serial):
        super().__init__(device_serial)

    # connection verification
    def connection_verification(self):
        device = self.device
        device.app_clear('com.netflix.Speedtest')
        device.app_start('com.netflix.Speedtest')
        sleep(5)

        counter = 0
        while counter < 4:
            if device.xpath('//android.widget.TextView[@text="Mbps"]').exists:
                return True
            if device.xpath('//*[@resource-id="speed-value"]').exists:
                speed = device.xpath('//*[@resource-id="speed-value"]').get_text()
                if int(speed) >= 300:
                    return True

            if device.xpath('//android.widget.TextView[@text="* Could not reach our servers to perform the test. You may not be connected to the internet"]').exists:
                return False

            sleep(10)
            counter += 1

        return False


    # wi-fi settings
    def wifi_connect(self, ssid, password, password_type='WPA'):
        if password_type == 'DEFAULT':
            password_type = 'WPA'

        device = self.device
        device.shell(
            f"am start -n com.steinwurf.adbjoinwifi/.MainActivity -e ssid {ssid} -e password_type {password_type} -e password {password}")
        sleep(5)
        device.app_stop('com.steinwurf.adbjoinwifi')
        return True

    # proxy settings
    def proxy_connect(self, proxy_ip, proxy_port, proxy_user, proxy_password):
        device = self.device

        while True:
            try:
                device.app_clear('net.typeblog.socks')
                device.app_start('net.typeblog.socks')

                # insert data
                device.xpath('//*[@text="Server IP"]').click()
                device(resourceId='android:id/edit').send_keys(proxy_ip)
                device.xpath('//*[@text="OK"]').click()

                device.xpath('//*[@text="Server Port"]').click()
                device(resourceId='android:id/edit').send_keys(proxy_port)
                device.xpath('//*[@text="OK"]').click()

                device(resourceId='android:id/decor_content_parent').swipe('up', steps=25)

                device(text='Username & Password Authentication', index=0).click()
                device(text='Username & Password Authentication', index=0).click()

                device.xpath('//android.widget.TextView[@text="Username"]').click()
                device(resourceId='android:id/edit').send_keys(proxy_user)
                device.xpath('//*[@text="OK"]').click()

                device.xpath('//android.widget.TextView[@text="Password"]').click()
                device(resourceId='android:id/edit').send_keys(proxy_password)
                device.xpath('//*[@text="OK"]').click()

                # start the connection
                device(resourceId='net.typeblog.socks:id/switch_action_button', checked=False).click()

                sleep(10)
                if device.xpath('//*[@text="OK"]').exists:
                    device.xpath('//android.widget.Button[@text="OK"]').click()
                    sleep(5)

                if self.connection_verification():
                    device.press('home')
                    return True

            except Exception as e:
                print(f'Error connecting to proxy: {e}')


    def proxy_stop(self):
        device = self.device
        device.app_stop('com.txthinking.brook')
        print('proxy stopped')
        return True

    def proxy_switch(self):
        device = self.device
        device.app_start('com.txthinking.brook')
        sleep(3)
        device.xpath('//android.widget.Button[@text="Stop"]').click()
        sleep(5)
        device.xpath('//android.widget.Button[@text="Start"]').click()
        sleep(3)
        if device.xpath('//*[@text="Connection request"]').exists:
            device.xpath('//android.widget.Button[@text="OK"]').click()

        while True:
            if device.xpath('//android.widget.Button[@text="Stop"]').exists:
                break

        print('proxy switch to start')
        return True


if __name__ == '__main__':
    device = Network('XMOBX22111187310')
    #device.proxy_connect('p.webshare.io', 80, 'fmvdjkkj-rotate', 'p2i39kdgit3f')
    #print(device.connection_verification())
    device.wifi_connect('STARLINK', '123123123')

