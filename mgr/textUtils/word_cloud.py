# coding=utf-8
import os

import jieba
import matplotlib.pyplot as plt
import pandas as pd
import wordcloud
from nltk import FreqDist
import time

# font_path = 'C:\Windows\Fonts\msyh.ttc'
font_path = 'simhei.ttf'

project_path = os.getcwd()
# print(path)
# 运行Django时  输出：E:\IT\Python\pystudy\Django_demo\noteplus
path = os.path.join(project_path,'mgr')
path = os.path.join(path,'textUtils')
stopword_path = os.path.join(path,'baidu_stopwords.txt')
print('stopword_path:',stopword_path)
font_path = os.path.join(project_path,'mgr')
font_path = os.path.join(font_path,'textUtils')
font_path = os.path.join(font_path,'simhei.ttf')
# stoplist = list(pd.read_csv('./stopwords.txt', names=['w'], sep='aaa', encoding='utf-8', engine='python').w)
# stoplist2 = list(pd.read_csv('./停用词.txt', names=['w'], sep='aaa', encoding='utf-8', engine='python').w)
stoplist3 = list(pd.read_csv(stopword_path, names=['w'], sep='aaa', encoding='utf-8', engine='python').w)
# stoplist3 = list(pd.read_csv("./baidu_stopwords.txt", names=['w'], sep='aaa', encoding='utf-8', engine='python').w)
# stoplist4 = list(pd.read_csv('./cn_stopwords.txt', names=['w'], sep='aaa', encoding='utf-8', engine='python').w)
# stoplist5 = list(pd.read_csv('./hit_stopwords.txt', names=['w'], sep='aaa', encoding='utf-8', engine='python').w)

# print(stoplist)

# text = "遍历列表中的所有元素是常用的一种操作，在遍历的过程中可以完成查询、处理等功能。在生活中，如果想要去商场买一件衣服，就需要在商场中逛一圈，看是否有想要买的衣服。逛商场的过程相当于列表的遍历操作。在Python中遍历列表的方法介绍如下： 方法一：最简单常用的，直接使用for循环实现 语法格式： for item in listname: #输出item 用法示例: list = [2, 3, 4]for num in list:    print (num) 输出： 234 方法二：利用python内置函数enumerate（）列举出list中的数语法格式: for index,item in enumerate(listname):    #输出index和item 参数 index - 用于保存元素的索引 item - 用于保存获取到的元素值，要输出元素内容时，直接输出该变量即可 listname - 列表名称 用法示例 list = [2, 3, 4]for index ,item in enumerate(list):    print（index+1, item） 输出： 1 22 33 4 方法三：使用iter（）迭代器语法格式： iter(object[, sentinel]) 函数用来生成迭代器，返回迭代对象。 参数： object -- 支持迭代的集合对象。 sentinel -- 如果传递了第二个参数，则参数 object 必须是一个可调用的对象（如，函数），此时，iter 创建了一个迭代器对象，每次调用这个迭代器对象的__next__()方法时，都会调用 object。 用法示例： list = [2, 3, 4]for i in iter(list):    print (i) 输出： 234 方法四：使用range（）函数pytho range(start, stop[, step]) 函数返回类型是dtarray，可用list（）返回一个整数列表，一般用在 for 循环中。参数 start: 计数从 start 开始。默认是从 0 开始。例如range（5）等价于range（0， 5）; end: 计数到 end 结束，但不包括 end。例如：range（0， 5） 是[0, 1, 2, 3, 4]没有5 step：步长，默认为1。例如：range（0， 5） 等价于 range(0, 5, 1) 用法实例 list = [2, 3, 4]for i in range(len(list)):    print i,list[i] 输出： 0 2 1 3 2 4"
def m_cut(intxt):
	return [w for w in jieba.cut(intxt) if w not in stoplist3]

# tokens = m_cut(text)
# tokens = "".join(jieba.cut(text,cut_all=False))
# print(tokens)
# 生成完备的词条频数词典
# fdist = FreqDist(tokens)

# cloudobj = wordcloud.WordCloud(
# 	font_path=font_path,
# 	# background_color=None,
# 	background_color="white",
# 	width=1600,
# 	height=1000,
# 	max_words=15,
#
# ).fit_words(fdist)
#
# plt.imshow(cloudobj)
# plt.axis("off")
# plt.show()

# 保存高清图片
# cloudobj.to_file('词云2.png')

def get_WC(txt):
	"""
	生成并保存词云图  返回值为词云图文件地址
	:param txt:
	:return:
	"""
	tokens = m_cut(txt)
	# 生成完备的词条频数词典
	fdist = FreqDist(tokens)
	cloudobj = wordcloud.WordCloud(
		font_path=font_path,
		# background_color=None,
		background_color="white",
		width=600,
		height=400,
		max_words=15,

	).fit_words(fdist)

	plt.imshow(cloudobj)
	plt.axis("off")
	# plt.show()

	# 获取时间戳 作为文件名
	t = time.time()
	filepath = os.path.join(project_path,'static')
	filepath = os.path.join(filepath,'space')
	filepath = os.path.join(filepath, str(int(t))+'.png')
	filename = str(int(t))+'.png'
	# 保存高清图片
	cloudobj.to_file(filepath)
	return filename

# print(get_WC(text))

