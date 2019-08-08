# BeautifulSoup是一个可以将复杂的HTML文档转换成一个复杂的树形结构，
# 每个节点都是python对象，
# 所有对象可以归纳为4种：Tag、NavigableString、BeautifuSoup和Comment。

#1. tag其实就是HTML中的一个个标签，例如td、a等等HTML标签加上里面包括的内容就是Tag
# 需要掌握find函数的用法，find(name,attrs,recursive,text,**wargs)

from bs4 import BeautifulSoup as bs
import requests
from lxml import etree

def get_html(url):
    response = requests.get(url)
    html = bs(response.text,'lxml')
    return html

def get_itemBs(html):
    datas = []
    for data in html.find_all("tbody"):
        try:
            user = data.find('div', class_="auth").get_text(strip=True)
            # print(user)
            content = data.find('td',class_='postbody').get_text(strip=True)
            # print(content)
            datas.append((user,content))
        except:
            pass
    return datas

def bs4Get(url,file):
    url = 'http://www.dxy.cn/bbs/thread/626626#626626'
    html = get_html(url)
    datas = get_itemBs(html)
    response = requests.get(url)
    html = bs(response.text,'lxml')
    f = open(file,'w')
    i = 1
    for data in datas:
        f.write(str(i)+' '+data[0]+':'+data[1]+'\n')
        i+=1
        
def get_itemXpath(html):
    datas = []
    response = requests.get(url)
    html = response.text
    tree = etree.HTML(html)
    user = tree.xpath('//div[@class="auth"]/a/text()')
    # print(user)
    content= tree.xpath('//td[@class="postbody"]')
    # print(content)
    for i in range(len(user)):
        datas.append((user[i].strip(),content[i].xpath('string(.)').strip()))

    return datas


def xpathGet(url,file):
    url = 'http://www.dxy.cn/bbs/thread/626626#626626'
    html = get_html(url)
    datas = get_itemXpath(html)
    f = open(file,'w')
    i = 1
    for data in datas:
        f.write(str(i)+' '+data[0]+':'+data[1]+'\n')
        i+=1

if __name__ == "__main__":
    url = 'http://www.dxy.cn/bbs/thread/626626#626626'
    # bs4Get(url,'./bsget.txt')
    xpathGet(url,'./xpathget.txt')