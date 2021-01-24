import re
from bs4 import BeautifulSoup
from lxml import etree

html = '<p>你好</p><br/><font>哈哈</font><b>大家好</b>'

# 法一
pattern = re.compile(r'<[^>]+>', re.S)
result = pattern.sub('', html)
print(result)
# 法二
soup = BeautifulSoup(html, 'html.parser')
print(soup.get_text())

# 法三
response = etree.HTML(text=html)
# print(dir(response))
print(response.xpath('string(.)'))

# 你好哈哈大家好
# 你好哈哈大家好
# 你好哈哈大家好