# -- coding: utf-8 --
import requests
from lxml import html
from openpyxl import Workbook
from bs4 import BeautifulSoup

# 创建Excel
wb = Workbook()
ws = wb.active

# 获取数据
# url = 'https://place.qyer.com/china/citylist-0-0-1/'


def getpage(url):
    # 请求头，模拟浏览器登录
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

    # 访问链接，获取HTML
    r = requests.get(url, headers=headers)
    retext = r.text

    # 解析数据
    ht = html.fromstring(retext)

    # 使用xpath获取
    soup = BeautifulSoup(r.text, 'html.parser')
    tourist = ht.xpath('/html/body/div/section/div/div/main/div/div/div/div/div/div/div/div/form/table/tbody/tr/td/a')
    date_tag = soup.find_all('td', {'headers': 'categorylist_header_date', 'class': 'list-date small'})

    for i,j in zip(tourist,date_tag):
        count_people = i.text
        every_date = j.text
        # beento = i.xpath('./p[@class="beento"]/text()')[0]
        # list = i.xpath('./p[@class="pois"]/a/text()')
        # list2 = ''
        # for j in list:
        #     list2=list2+','+j.strip()
        # print(name,beento,list2[1:])
        # list = [place.strip() for place in list]
        # list2 = ','.join(list)
        datalist = [count_people, every_date]
        ws.append(datalist)


for i in range(1, 70):
    url = 'https://www.sgns.cn/info/number?start={}/'.format(i*15)
    getpage(url)

# Excel保存
fileanme = "D:\\workspace\\tif\\pachong"  # 路径可以自己设置，我这里是python源文件同级目录
wb.save("旅游景点.xlsx")