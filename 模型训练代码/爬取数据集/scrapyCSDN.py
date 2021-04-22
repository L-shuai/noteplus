import json
import requests
import urllib.request
from urllib.request import Request, urlopen
# import urllib2
from bs4 import BeautifulSoup
from distutils.filelist import findall
# from lxml import etree
# 正则表达式
import re
import csv
from demo import Common
import numpy as np

import random

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    #模拟浏览器访问
my_headers=["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
]
category = ['python','java','web','db','5g','game','mobile','ops','sec','iot','fund','avi','other']
# python已经爬完  6691条
# category = ['java','web','db','5g','game','mobile','ops','sec','iot','fund','avi','other']
# 从iot开始，22500条
# category = ['iot','fund','avi','other']
# category = ['web','5g','mobile','ops','sec','iot','other']
category = ['avi','other']
#
# def getAllLinks(cate):
#     link_list = []
#     # url = "https://blog.csdn.net/nav/"+cate
#     url = Common.csdn_url+cate
#     # data = urllib.request.urlopen().read().decode("utf-8","ignore")  #  ignore 的意思是如果编码出错也强行编码
#     # page = urllib.request.urlopen(url)
#     req = urllib.request.Request(url, headers= Common.headers)
#     contents = urllib.request.urlopen(req).read().decode('utf-8')
#     # contents = page.read()
#     # print(contents)
#     # 读取指定页面
#     soup = BeautifulSoup(contents, "html.parser")
#     for tag in soup.find_all('div', class_='title'):
#         title = ''.join(tag.find('h2').get_text().split())
#         link = tag.find('a').get('href')
#         print("title: "+title+"   link:"+link)
#
#
#
#     # # 查找所有class属性为hd的div标签
#     # div_list = soup.find_all('div', class_='title')
#     # # 获取每个div中的h2中的a（第一个），并获取其文本
#     # for each in div_list:
#     #     movie = each.h2.a.text.strip()
#     #     link_list.append(movie)
#
#     return link_list

def getAllLinks(cate):
    """
    根据博客类别，获取该类别下的所有文章链接
    :param cate:
    :return:
    """
    link_list = []
    # 每个类别查询500次
    for i in range(1000):
        print("下拉：",i)
        random_header = random.choice(my_headers)
        url = "https://blog.csdn.net/api/articles?type=more&category="+cate+"&shown_offset=100"
        #包装头部
        # firefox_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        firefox_headers = {'User-Agent': random_header}
        response = ''
        request = ''
        #构建请求
        request = Request(url)
        request.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36')
        request.add_header("GET",url)
        request.add_header("Host","blog.csdn.net")
        request.add_header("Referer","https://blog.csdn.net/nav/"+cate)
        response = urlopen(request).read()

        # 转换为字符串
        data_str = str(response)
        print("data_str:\n"+data_str)
        # 转换为json
        data_json = json.dumps(data_str)
        print("data_json:\n"+data_json)
        # 转换为字典数据
        data_dic = json.loads(response)
        # print("data_dic:\n"+data_dic)
        # print(json.read())
        # articles = data_dic['articles'
        articles = data_dic.get('articles')
        # print(articles)
        # print(len(articles))
        # print(articles[0])

        length = len(articles)
        print('本次下拉共获取：',length,' 篇文章')
        for i in range(length):
            link = articles[i].get('url')
            print(articles[i].get('title'),articles[i].get('url'))
        # getDetailHtml(link)
            link_list.append(link)
    return link_list

import requests
def getAllLinks2(cate):
    url = "https://blog.csdn.net/api/articles?type=more&category="+cate+"&shown_offset=0"
    r = requests.get(url,headers=headers)
    print(r)
    d=r.json()#一般ajax返回的都是json格式数据，将返回的数据json格式化，.json()是requests库自带函数
    print(d)
    articles = d['articles']#字典形式
    print(articles)
    linkList = []
    for article in articles:
        print("title:",article['title'],"url:",article['url'])
        linkList.append(article['url'])

from selenium import webdriver
import time
def getAllLinks3(cate):
    browser = webdriver.Chrome("E:\IT\Python\chromedriver_win32\chromedriver.exe")
    browser.get('https://blog.csdn.net/nav/'+cate)
    # browser.implicitly_wait(10)
    browser.implicitly_wait(3)
    i = 0
    for i in range(1200):###设置下拉1200次，如果想获取更多信息，增加下拉次数即可
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')##下拉，execute_script可以将进度条下拉到最底部
        time.sleep(1)##睡眠一下，防止网络延迟，卡顿等
    #     横向滚动条
        rand_x = random.randint(-100,100)
        # print(rand_x)
        js = "window.scrollTo("+str(rand_x)+",400);"
        browser.execute_script(js)

    print("下拉完成")
    data = []
    pattern = re.compile('<li.*?blog".*?>.*?title">.*?<a.*?>(.*?)</a>.*?<dd.*?name">.*?<a.*?blank">(.*?)</a>'
                     '.*?<span.*?num">(.*?)</span>.*?text">(.*?)</span>.*?</li>',re.S)
    print("正则匹配")
    # print("全部html:\n",browser.page_source)
    contents = browser.page_source
    linkList = []
    soup = BeautifulSoup(contents, "html.parser")
    for tag in soup.find_all('div', class_='title'):
        title = ''.join(tag.find('h2').get_text().split())
        link = tag.find('a').get('href')
        print("title: "+title+"   link:"+link)
        linkList.append(link)
    return linkList





    # items = re.findall(pattern,browser.page_source)##这里网页源代码为下拉5次后的代码
    # print("全部html:\n",browser.page_source)
    # print("匹配完成")
    # print("items:\n",items)
    # for item in items:
    #     print("item:\n",item)
    #     data.append({
    #         'Title':item[0].strip(),
    #         'Author' : item[1].strip(),
    #         'ReadNum' : item[2] + item[3]
    #     })
def getDetailHtml(url):
    """
    根据博客的url，获取该博客 的html
    :param url:
    :return:
    """
    # content = ''
    # 获取正文内容
    # response = requests.get(url,headers = headers)       #请求访问网站
    html = ''
    try:
        response=urllib.request.urlopen(url)
        response.encoding = 'utf-8'
        html = response.read().decode('utf-8')       #获取网页源码
        getFilterText(html)
    except:
        html='url异常-404'
    return html



def getFilterText(html):
    """
    根据某博客的html，获取正文的txt
    :param html:
    :return:
    """
    soup = BeautifulSoup(html, 'html.parser')
    # for li in soup.find_all(id="content_views"):         #遍历父节点
    # 获取博客标题
    title = 'blank'
    div = 'blank'
    try:
        title = soup.find(id="articleContentId").get_text().strip()
    except:
        title = '未知标题'
    try:
        div = soup.find(id = "content_views")
    except:
        return None
    if div is None:
        div = 'blank'
        text = {'title':'......','content':'......'}

    else:
        text = ''.join(div.get_text().strip())
        # 去除空格
        text = text.replace(' ','')
        # 去除回车换行
        text = text.replace('\n', '').replace('\r', '')
        # print("text:\n",text)
        text = {'title':title,'content':text}

    return text


def spiderStart():
    length = len(category)
    csv_reader = csv.reader(open('article-5000.csv')) # 有的文件是utf-8编码
    # count = len(list(csv_reader))
    count = 124072
    # count = len(csv_reader)
    print("count:",count)
    num = 1
    b = False
    if count>=1:
        num = count
    # print(length)
    for cate in  category:
        print("cate:",cate)
        link_List = []
        link_List = getAllLinks3(cate)
        for link in link_List:
            html = getDetailHtml(link)
            text = getFilterText(html)
            if text is None:
                text = 'blank'
                continue
            with open('article-5000.csv','a',encoding='utf-8') as f:    #设置文件对象
                fieldnames = ['id','title','content','category']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                # writer = csv.writer('article.csv', delimiter=',')
                # f.write(text)                 #将字符串写入文件中
                if b is False:
                    b = True
                    writer.writeheader()
                content =text.get('content').replace(u'\xa0', u'')
                title =text.get('title').replace(u'\xa0', u'')
                count+=1
                print("count:",count,"  title: ",title)
                writer.writerow({'id': count,'title':title,'content':content,'category':cate})
                # writer.writerow(text)


if __name__ == "__main__":
    # getAllLinks3("python")
    spiderStart()