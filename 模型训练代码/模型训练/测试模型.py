import pandas as pd
import numpy as np
from pandas import DataFrame
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import RidgeClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score
import jieba
jieba.load_userdict('../baidu_stopwords.txt')
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.model_selection  import GridSearchCV
import csv
# 模型保存
import joblib
from sklearn.model_selection import GridSearchCV
# f1_score打分
from sklearn.metrics import f1_score
import time
import re
import numpy as np
import pandas as pd
from pandas import Series, DataFrame


# 对列表进行分词并用空格连接
def segmentWord(cont):
    # stopwords = stopwordslist('/content/drive/Shareddrives/leeshuai55/毕业设计/数据集/baidu_stopwords.txt')
    c = []
    count = 1
    rate = 100
    for i in cont:
      if(count>rate):
        print(rate)
        rate=rate+3000
      count= count+1
      outstr = ''
      i = str(i)
      sentence_seged = jieba.cut(i)
      for word in sentence_seged:
        word = str(word)
        # if word not in stopwords:
        if word != '\t':
          if len(word)>1:
            outstr += word
            outstr += " "
      # a = list(jieba.cut(i))
      # b = " ".join(a)
      c.append(outstr)
    return c

text_clf = joblib.load('text_clf.pkl')
tfidf = joblib.load('tfidf.pkl')
text = ['pandas，python+data+analysis的组合缩写，是python中基于numpy和matplotlib的第三方数据分析库，与后两者共同构成了python数据分析的基础工具包，享有数分三剑客之名。']
# text = [['pandas，python+data+analysis的组合缩写，是python中基于numpy和matplotlib的第三方数据分析库，与后两者共同构成了python数据分析的基础工具包，享有数分三剑客之名。']]
# text = 'pandas，python+data+analysis的组合缩写，是python中基于numpy和matplotlib的第三方数据分析库，与后两者共同构成了python数据分析的基础工具包，享有数分三剑客之名。'

print('type0:',type(text))  #应为List
# list to series
# text = Series(text, index = ['0',])
# print('type1:',type(text))  #应为series
# text = 'pandas，python+data+analysis的组合缩写，是python中基于numpy和matplotlib的第三方数据分析库，与后两者共同构成了python数据分析的基础工具包，享有数分三剑客之名。'
# text = 'python i love'
# data = {text:["0"]}
# print('data:',data)
# df = DataFrame(data)
text = segmentWord(text)  #这里应为list
print('text:',text)
print('type2:',type(text)) #应为List

train_x = tfidf.transform(text)

predicted = text_clf.predict(train_x)
print(set(predicted))
print(predicted[0])
# tfidf = TfidfVectorizer()
# tfidf = TfidfTransformer()
# train_x = tfidf.fit_transform(text)
# vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
# transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
# tfidf_before = vectorizer.fit_transform(text)
# tfidf = transformer.fit_transform(tfidf_before)

# predicted = text_clf.predict(train_x)
# print(predicted)


# text = 'pandas，python+data+analysis的组合缩写，是python中基于numpy和matplotlib的第三方数据分析库，与后两者共同构成了python数据分析的基础工具包，享有数分三剑客之名。'
# data = {text:["0"]}
# df = DataFrame(data)
# print('df.shape',df.shape)
# print('segmentWord(df):',segmentWord(df))
# tfidf = TfidfVectorizer()
# df = tfidf.fit_transform(df)
# # predicted = clf.predict(new_tfidf)
# predicted = text_clf.predict((df))
# # print('SVC', np.mean(predicted == Y_train))
# print(set(predicted))
# # print(y_pred)