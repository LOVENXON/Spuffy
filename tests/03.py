import uiautomator2

d = uiautomator2.connect('10.0.0.75:5555')
d.xpath('//android.widget.TextView[@text="Username"]').click()

if d(resourceId='android:id/edit').exists:
    d(resourceId='android:id/edit').send_keys('sgsdgsd')
else:
    print('Username field not found')

