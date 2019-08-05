# -*- coding:utf-8 -*-
# request-2.14.2版本
# 尝试使用requests或者是urllib用get方法向[https://www.baidu.com/](https://www.baidu.com/)发出一个请求，并将其返回结果输出。 
import requests
import re

def testRequest(url='https://www.baidu.com/'):
    response = requests.get(url)
    print('respons status code: %d'%(response.status_code))
    print('response encoding: ',response.encoding)
    print('response headers: ',response.headers)
    print(f'text:{response.text[:1000]}')

def get_one_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None
def get_one_info(url):
    html  = get_one_text(url)
    pattern = re.compile('<em class="">(.*?)</em>[\s\S]*?<span class="title">(.*?)</span>[\s\S]*?<p class="">[\s\S](.*?)&nbsp[\s\S]*?<br>[\s\S]*?(.*)&nbsp;/&nbsp;(.*?)&nbsp;/&nbsp')
    items = re.findall(pattern,html)
    l=[]
    for item in items:
        dic = {}
        dic['top'] = item[0].strip()
        dic['name'] = item[1].strip()
        dic['director'] = item[2].strip()
        dic['data'] = item[3].strip()
        dic['country'] = item[4].strip()
        l.append(dic)
    return l
def travel(url,filePath):
    f = open(filePath,'w')
    #f.write('top'+' '+'name'+' '+'director'+' '+'data'+' '+'country'+'\n')
    for i in range(1,11):
        tmp= url+'?start='+str(25*(i-1))
        for info in get_one_info(tmp):
            print(info)
            f.write(info['top']+','+info['name']+','+info['director']+','+info['data']+','+info['country']+'\n')

if __name__ == "__main__":
    url = 'https://movie.douban.com/top250'
    travel(url,'douBanTop250.txt')