import time

import uiautomator2

#R9HNA06388J
#R9PR407VZYJ
d = uiautomator2.connect('R9HNA06388J')
#d.press('back')
#print(d.shell('am broadcast -a android.intent.action.HEADSET_PLUG --ei state 0 '))
print(d.app_list('com.spotify'))
#print(d.app_current())
#d.app_clear('com.spotify.musii')
#print(d.app_current())
#d.app_uninstall('com.android.vending')
#d.shell('pm disable-user --user 0 com.android.vending')
#print(d.shell('ping -c 1 xmobileusa.com'))
#print(d.shell('curl  https://www.youtube.com'))