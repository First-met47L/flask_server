
from selenium import webdriver
import em,time

driver = webdriver.PhantomJS()
url = 'https://mp.weixin.qq.com/profile?src=3&timestamp=1505268498&ver=1&signature=jmaYw3DkdTVDWD0SCOphrtO4IoQZEQSpixhkVNBEMpHFVxfOgcyO5mqUjQWFwcpd2Ly84Q26ge5cKu2Y3HVB0A=='
driver.set_window_size(1200, 800)
cookies = driver.get_cookies()

# print(cookies)
# driver.get(url)
# for k, v in cookies.iteritems():
#     cookie_dict = {'name': k, 'value': v}
#     driver.add_cookie(cookie_dict)
driver.get(url)

imageBin = driver.get_screenshot_as_png()
em.send(imageBin)

# element = driver.find_element_by_id('seccodeImage')
# left = int(element.location['x'])
# top = int(element.location['y'])
# right = int(element.location['x'] + element.size['width'])
# bottom = int(element.location['y'] + element.size['height'])
#
# im = Image.open('screenshot.png')
# im = im.crop((left, top, right, bottom))
# im.save('code.png')

