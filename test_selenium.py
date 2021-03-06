# -*- encoding:utf-8 -*-

#selenium:3.12.0
#webdriver:2.38
#chrome.exe: 65.0.3325.181（正式版本） （32 位）

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('window-size=1920x3000') #指定浏览器分辨率
chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" #手动指定使用的浏览器位置

executable_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
driver=webdriver.Chrome(executable_path=executable_path,chrome_options=chrome_options)
driver.get('https://www.baidu.com')
print(driver.page_source)
print(len(driver.page_source))

print('hao123' in driver.page_source)


# driver.close() #切记关闭浏览器，回收资源