# -*- coding: utf-8 -*-
# @Time    : 2019-04-05 20:36
# @Author  : shawnLiu
# @Email   : 614477862@QQ.COM
# @File    : MDNSScript.py
# @Software: PyCharm


import time

from selenium import webdriver
from selenium.webdriver.support.select import Select
from PIL import Image


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

driver = webdriver.Chrome()

driver.set_window_size(800, 600)  # 对于Phantomjs记得加上这个要不然会出错
driver.get("https://www.mdnsonline.com/customer/login")
time.sleep(1)
driver.find_element_by_id("customerloginform-email").send_keys("username")
driver.find_element_by_id("customerloginform-password").send_keys("***********")
driver.find_element_by_class_name("btn-login").click()
time.sleep(1)


productID = 1850

while 1:
    time.sleep(5)
    if (productID == 1851):
        productID = 1850
    else:
        driver.get("https://www.mdnsonline.com/product/"+str(productID))
        time.sleep(1)
        selectSize = Select(driver.find_element_by_id("size"))  # 实例化select 尺码
        options_list = driver.find_elements_by_tag_name('option')
        sizeArray = []
        # 遍历option
        for option in options_list:
            # 获取下拉框的value和text
            if option.text in {"S","M","L"} :
                if int(option.get_attribute("value")) >500:
                    sizeArray.append(option.get_attribute("value"))
                    print("Value is:%s  Text is:%s" % (option.get_attribute("value"), option.text))
        if(len(sizeArray)>0):
            selectSize.select_by_value(sizeArray[len(sizeArray)-1])
            selectQuantity = Select(driver.find_element_by_id("quantity"))  # 实例化select 数量
            selectQuantity.select_by_index(1)  # 选择第2项选项 从1开始
        else:
            productID=productID+1
            continue


        # driver.find_element_by_xpath("//div[@class='item-button']/a[1]").click()

        buttonAddCart = driver.find_element_by_xpath("//div[@class='item-button']/a[1]")

        time.sleep(1)
        driver.execute_script("arguments[0].click()", buttonAddCart)
        # driver.save_screenshot('/Users/liuxiaoying/Desktop/2.png')


        if(len(sizeArray)>=1):
            time.sleep(1)
            driver.get("https://www.mdnsonline.com/shopping-cart")
            time.sleep(1)

            buttonSummary = driver.find_element_by_xpath("//div[@class='cart_summary']/a[1]")
            driver.execute_script("arguments[0].click()", buttonSummary)
            # time.sleep(1)
            # driver.find_element_by_xpath("//div[@class='cart_summary']/a[1]").click()
            # driver.save_screenshot('/Users/liuxiaoying/Desktop/3.png')

            button = driver.find_element_by_xpath("//a[@class='btn_submit']")
            driver.execute_script("arguments[0].click()", button)
            time.sleep(1)

            # checkbox 确定地址
            confirmaddress = driver.find_element_by_id('orderform-confirmaddress')
            driver.execute_script("arguments[0].click()", confirmaddress)
            # driver.save_screenshot('/Users/liuxiaoying/Desktop/4.png')

            # driver.find_element_by_id('orderform-confirmaddress').click()  # click
            # checkbox 确定订单
            confirmorder = driver.find_element_by_id('orderform-confirmorder')
            driver.execute_script("arguments[0].click()", confirmorder)
            # driver.find_element_by_id('orderform-confirmorder').click()  # click

            # radio 支付宝支付
            alipay = driver.find_element_by_xpath('//input[@value="alipay"]')
            driver.execute_script("arguments[0].click()", alipay)
            # driver.find_element_by_xpath('//input[@value="alipay"]').click()  # click

            # checkbox 同意所有
            agreeterm = driver.find_element_by_id('orderform-agreeterm')
            driver.execute_script("arguments[0].click()", agreeterm)
            # driver.find_element_by_id('orderform-agreeterm').click()  # click

            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            time.sleep(5)
            # 验证码
            driver.save_screenshot('/Users/liuxiaoying/Desktop/验证码1.png')
            element = driver.find_element_by_xpath('//div[@class="form-group field-orderform-captcha"]/img')  # 找到验证码图片
            # time.sleep(3)
            left = element.location['x']
            top = element.location['y']
            right = element.location['x'] + element.size['width']
            bottom = element.location['y'] + element.size['height']

            im = Image.open('/Users/liuxiaoying/Desktop/验证码1.png')
            im = im.crop((215, 300, 450, 380))
            im = im.crop()
            im.save("/Users/liuxiaoying/Desktop/验证码_"+str(productID)+".png")
            """ 读取图片 """

            productID = productID + 1

            # driver.quit()