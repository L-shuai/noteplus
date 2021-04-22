import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
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


# 读取数据集
clear_df = pd.read_csv('../trainTestSet2.csv',names=['content','category'])
# 划分训练集
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(clear_df.content,clear_df.category,test_size=0.25,random_state=6)


# x_train,x_test,y_train,_y_test = train_test_split(train_test_data[0],train_test_data[1],test_size=0.25,random_state=6)
now = time.asctime( time.localtime(time.time()))
print('数据集划分完毕：',now)


# x_train = x_train[:500]
# x_test = x_test[:100]
# y_train = y_train[:500]
# y_test = y_test[:100]

from jieba import analyse
# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


analyse.set_stop_words("../baidu_stopwords.txt")
# 对列表进行分词并用空格连接
def segmentWord2(cont):
    c = []
    # 引入TF-IDF关键词抽取接口
    tfidf = analyse.extract_tags
    count = 1
    rate = 100
    for i in cont:
      if(count>rate):
        print(rate)
        rate=rate+3000
      count= count+1
      outstr = ''
      # 基于TF-IDF算法进行关键词抽取
      keywords = tfidf(i,topK=100)
      kw = ''
      for keyword in keywords:
        kw+=keyword
        kw+=' '
      # a = list(jieba.cut(i))
      # b = " ".join(a)
      c.append(kw)
    return c



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

# # 对列表进行分词并用空格连接
# def segmentWord(cont):
#     c = []
#     for i in cont:
#         a = list(jieba.cut(i))
#         b = " ".join(a)
#         c.append(b)
#     return c


def cutword(x):
    seg = jieba.cut(x)  # 结巴分词函数
    return ' '.join(seg)


print('开始分词')
now = time.asctime( time.localtime(time.time()))
print('开始分词：',now)
# x_train = cutword(x_train)
x_train = segmentWord(x_train)
print('x_train cut over')
x_test = segmentWord(x_test)
print('结束分词')
now = time.asctime( time.localtime(time.time()))
print('分词完毕：',now)
print(type(x_train))

from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import RidgeClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score
from sklearn.svm import SVC
import time



from sklearn import linear_model
# tfidf = TfidfVectorizer(ngram_range=(1,2),max_features=8000)
tfidf = TfidfVectorizer(ngram_range=(1,2))
x_train = tfidf.fit_transform(x_train)
x_test = tfidf.transform(x_test)
reg = linear_model.LogisticRegression(penalty='l2',C=1.0,solver='liblinear')
reg.fit(x_train,y_train)
val_pred = reg.predict(x_test)
# 打印详细参数
print(metrics.classification_report(y_test, val_pred))
print('预测结果中各类新闻数目')
print(pd.Series(val_pred).value_counts())
print('\n F1 score为')
print('f1_score',f1_score(y_test, val_pred, average='macro'))
from sklearn.metrics import accuracy_score
print('accuracy:',accuracy_score(y_test, val_pred))
from sklearn.metrics import precision_score
print('precesion:',precision_score(y_test, val_pred, average='macro'))
from sklearn.metrics import recall_score
print('recall:',recall_score(y_test, val_pred, average='macro'))


"""

数据集划分完毕： Fri Mar  5 14:26:22 2021
开始分词
开始分词： Fri Mar  5 14:26:23 2021
100
3100
6100
9100
12100
15100
18100
21100
24100
27100
30100
33100
36100
39100
42100
45100
48100
51100
54100
57100
60100
63100
66100
69100
72100
75100
78100
81100
84100
87100
90100
93100
96100
99100
102100
105100
108100
x_train cut over
100
3100
6100
9100
12100
15100
18100
21100
24100
27100
30100
33100
36100
结束分词
分词完毕： Fri Mar  5 14:46:56 2021
<class 'list'>
预测结果中各类新闻数目
java      3531
python    3347
ops       3342
db        3167
5g        3156
game      2932
mobile    2896
iot       2791
fund      2703
sec       2673
avi       2104
other     1986
web       1908
dtype: int64
 F1 score为
0.730925932602053

"""


'''
最终
数据集划分完毕： Thu Apr  1 23:11:07 2021
开始分词
开始分词： Thu Apr  1 23:11:08 2021
100
3100
6100
9100
12100
15100
18100
21100
24100
27100
30100
33100
36100
39100
42100
45100
48100
51100
54100
57100
60100
63100
66100
69100
72100
75100
78100
81100
84100
87100
90100
93100
96100
99100
102100
105100
108100
x_train cut over
100
3100
6100
9100
12100
15100
18100
21100
24100
27100
30100
33100
36100
结束分词
分词完毕： Thu Apr  1 23:39:43 2021
<class 'list'>
              precision    recall  f1-score   support
          5g       0.88      0.95      0.92      2940
         avi       0.80      0.66      0.72      2571
          db       0.87      0.92      0.90      2976
        fund       0.80      0.78      0.79      2768
        game       0.82      0.82      0.82      2915
         iot       0.75      0.76      0.75      2839
        java       0.83      0.95      0.88      2974
      mobile       0.86      0.86      0.86      2940
         ops       0.83      0.92      0.87      2931
       other       0.86      0.66      0.75      2822
      python       0.88      0.95      0.91      3077
         sec       0.78      0.71      0.74      2915
         web       0.79      0.77      0.78      1868
    accuracy                           0.83     36536
   macro avg       0.83      0.82      0.82     36536
weighted avg       0.83      0.83      0.83     36536
预测结果中各类新闻数目
java      3413
python    3330
ops       3259
5g        3161
db        3147
mobile    2960
game      2909
iot       2899
fund      2704
sec       2634
other     2186
avi       2118
web       1816
dtype: int64
 F1 score为
0.8225113119306862

'''

'''
全部参数
24100
27100
30100
33100
36100
结束分词
分词完毕： Sun Apr  4 13:20:18 2021
<class 'list'>
              precision    recall  f1-score   support
          5g       0.88      0.95      0.92      2940
         avi       0.80      0.66      0.72      2571
          db       0.87      0.92      0.90      2976
        fund       0.80      0.78      0.79      2768
        game       0.82      0.82      0.82      2915
         iot       0.75      0.76      0.75      2839
        java       0.83      0.95      0.88      2974
      mobile       0.86      0.86      0.86      2940
         ops       0.83      0.92      0.87      2931
       other       0.86      0.66      0.75      2822
      python       0.88      0.95      0.91      3077
         sec       0.78      0.71      0.74      2915
         web       0.79      0.77      0.78      1868
    accuracy                           0.83     36536
   macro avg       0.83      0.82      0.82     36536
weighted avg       0.83      0.83      0.83     36536
预测结果中各类新闻数目
java      3413
python    3330
ops       3259
5g        3161
db        3147
mobile    2960
game      2909
iot       2899
fund      2704
sec       2634
other     2186
avi       2118
web       1816
dtype: int64
 F1 score为
f1_score 0.8225113119306862
accuracy: 0.8287989927742501
precesion: 0.8259313525759981
recall: 0.8239037133850441

'''