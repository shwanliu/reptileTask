
from selenium import webdriver
from selenium.webdriver.support.select import Select
from PIL import Image
from bs4 import BeautifulSoup
import requests



def autoLogin(url):
    driver = webdriver.Chrome()
    driver.set_window_size(800, 600)  # 对于Phantomjs记得加上这个要不然会出错
    driver.get(url)

    # driver.switch_to.frame(0)
    driver.find_element_by_id('lbNormal').click()
    # 需要加上不然会找不到email元素
    driver.switch_to.frame(0)
    driver.find_element_by_name('email').send_keys("****")
    driver.find_element_by_name('password').send_keys("*****")

    driver.find_element_by_id('dologin').click()

def get_text(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    headers = {'User-Agent': user_agent}
    try:
        response = requests.get(url,headers=headers, timeout = 20)
        # response.raise_for_status()
        # response.encoding = response.apparent_encoding
        return response.text
    except:
        print("error happen")

# 抓取西刺客的ips并且保存
def get_ip_list(response,filePath):
    f = open(filePath,'w')
    ip_list= []
    soup = BeautifulSoup(response, 'html.parser')
    ips  = soup.find(id='ip_list').find_all('tr')
    for ip_ in ips:
        if len(ip_.select('td'))>=8:
            ip = ip_.select('td')[1].text
            port = ip_.select('td')[2].text
            protocol = ip_.select('td')[5].text
            if protocol in ('HTTP','HTTPS'):
                ip_list.append(f'{protocol}://{ip}:{port}')
                # f.write(f'{protocol}://{ip}:{port}')
                # f.write('\n')
    return ip_list

#使用代理进行网页访问
def using_proxy(url, proxy):
    proxies = {}
    if proxy.startswith('HTTPS'):
        proxies['https'] = proxy
    else:
        proxies['http'] = proxy
    
    try:
        r = requests.get(url,proxies=proxies)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return (r.text, r.status_code)
    except:
        print('无法访问网页' + url)
        return False

if __name__ == "__main__":
    # url = 'https://mail.163.com'
    # autoLogin(url)
    r = get_text('https://www.xicidaili.com/')
    # # print(r)
    ip_list = get_ip_list(r,'ips_file')
    url = 'http://www.baidu.com'
    text = using_proxy(url, ip_list[0])
