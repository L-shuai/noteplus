import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
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
clear_df = pd.read_csv('../trainTestSetClear.csv',names=['content','category'])


# 划分训练集
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(clear_df.content,clear_df.category,test_size=0.25,random_state=6)
# x_train,x_test,y_train,_y_test = train_test_split(train_test_data[0],train_test_data[1],test_size=0.25,random_state=6)
now = time.asctime( time.localtime(time.time()))
print('数据集划分完毕：',now)


# x_train = x_train[:50000]
# x_test = x_test[:10000]
# y_train = y_train[:50000]
# y_test = y_test[:10000]

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


def feature_extractor(input_x, case='tfidf', max_df=1.0, min_df=0.0):
    """
    特征抽取
    :param corpus:
    :param case: 不同的特征抽取方法
    :return:
    """
    return TfidfVectorizer(token_pattern='\w', ngram_range=(1,2), max_df=max_df, min_df=min_df).fit_transform(input_x)


# 调用LogisticRegression(),基于线性分类器的变种模型有很多，我们将会在后面的试验中使用添加了L1范式的lasso回归，添加了L2范式的岭回归回归
def fit_and_predicted(train_x, train_y, test_x, test_y, penalty='l2', C=1.0, solver='lbfgs'):
    """
    训练与预测
    :param train_x:
    :param train_y:
    :param test_x:
    :param test_y:
    :return:
    """
    clf = linear_model.LogisticRegression(penalty=penalty, C=C, solver=solver, n_jobs=-1).fit(train_x, train_y)
    predicted = clf.predict(test_x)
    print(metrics.classification_report(test_y, predicted))
    # f1.append(f1_score(test_y,val_pred,average='macro'))
    print('f1_score: ',f1_score(test_y,predicted,average='macro'))
    print('accuracy_score: %0.5fs' %(metrics.accuracy_score(test_y, predicted)))
    print('*'*200)




from sklearn import decomposition
import numpy as np
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
from sklearn.feature_extraction.text import TfidfVectorizer


from sklearn import linear_model
tfidf = TfidfVectorizer(max_features=20000)
# tfidf = TfidfVectorizer()
train_x = tfidf.fit_transform(x_train)
test_x = tfidf.transform(x_test)
train_y = y_train
test_y = y_test



print('x_train_shape',train_x.shape)
print('x_test_shape',test_x.shape)
# x_train_shape (20000, 116844)
# x_test_shape (3000, 116844)

# train_x = train_x.todense()
# test_x = test_x.todense()


# print('x_train_dense_shape',train_x.shape)
# print('x_test_dense_shape',test_x.shape)

# 将矩阵转为数组
# train_x_arr = np.array(train_x)
# test_x_arr = np.array(test_x)
# train_x = train_x.toarray()
# test_x = test_x.toarray()

# print('x_train_array_shape',train_x_arr.shape)
# print('x_test_array_shape',test_x_arr.shape)

# PCA 降维
# pca = decomposition.PCA(
#         n_components=8000,
#         whiten=False,
#         # svd_solver='auto'
#         svd_solver='randomized'
#     )

tsvd = TruncatedSVD(n_components=8000)
train_x_tsvd = tsvd.fit_transform(train_x)
test_x_tsvd = tsvd.transform(test_x)
clf = SVC(kernel='rbf',C=10,gamma=0.1)
clf.fit(train_x_tsvd,train_y)



print('x_train_pca_shape',train_x_tsvd.shape)
print('x_test_pca_shape',test_x_tsvd.shape)
# reg = linear_model.LogisticRegression(penalty='l2',C=1.0,solver='liblinear')
# reg.fit(x_train,y_train)

print('svc training begin')
clf = SVC(kernel='rbf',C=10,gamma=0.1)
clf.fit(train_x_tsvd,train_y)
print('train over')
print('predict begin')
val_pred = clf.predict(test_x_tsvd)
print('predict over')


# 打印详细参数
print(metrics.classification_report(test_y, val_pred))

print('预测结果中各类新闻数目')
print(pd.Series(val_pred).value_counts())
print('\n F1 score为')
print(f1_score(y_test, val_pred, average='macro'))



# 5000规模：F1 score为
# 0.16691994286054326


'''
规模20000时：
Loading model cost 0.786 seconds.
Prefix dict has been built successfully.
数据集划分完毕： Fri Mar 26 21:24:33 2021
开始分词
开始分词： Fri Mar 26 21:24:34 2021
100
3100
6100
9100
12100
15100
18100
x_train cut over
100
结束分词
分词完毕： Fri Mar 26 21:26:16 2021
<class 'list'>
x_train_shape (20000, 20000)
x_test_shape (3000, 20000)
x_train_pca_shape (20000, 8000)
x_test_pca_shape (3000, 8000)
svc training begin
train over
predict begin
predict over
              precision    recall  f1-score   support
          5g       0.79      0.93      0.85       227
         avi       0.56      0.52      0.54       227
          db       0.75      0.80      0.77       230
        fund       0.62      0.65      0.64       226
        game       0.66      0.61      0.64       244
         iot       0.62      0.60      0.61       249
        java       0.64      0.72      0.67       226
      mobile       0.64      0.62      0.63       215
         ops       0.74      0.82      0.77       258
       other       0.47      0.38      0.42       238
      python       0.67      0.76      0.71       242
         sec       0.65      0.56      0.60       248
         web       0.67      0.54      0.60       170
    accuracy                           0.66      3000
   macro avg       0.65      0.66      0.65      3000
weighted avg       0.65      0.66      0.65      3000
预测结果中各类新闻数目
ops       287
python    276
5g        269
java      254
db        243
iot       241
fund      236
game      228
avi       213
sec       213
mobile    210
other     195
web       135
dtype: int64
 F1 score为
0.6510877150937393
'''


'''
规模50000时，
              precision    recall  f1-score   support
          5g       0.88      0.93      0.91       768
         avi       0.65      0.64      0.65       730
          db       0.80      0.85      0.83       798
        fund       0.69      0.69      0.69       798
        game       0.75      0.74      0.74       818
         iot       0.69      0.71      0.70       773
        java       0.72      0.81      0.76       805
      mobile       0.72      0.74      0.73       774
         ops       0.77      0.84      0.81       811
       other       0.62      0.51      0.56       761
      python       0.79      0.80      0.80       855
         sec       0.72      0.64      0.68       771
         web       0.72      0.62      0.66       538
    accuracy                           0.74     10000
   macro avg       0.73      0.73      0.73     10000
weighted avg       0.73      0.74      0.73     10000
预测结果中各类新闻数目
java      902
ops       887
python    873
db        843
game      808
5g        807
fund      802
iot       793
mobile    791
avi       710
sec       693
other     626
web       465
dtype: int64
 F1 score为
0.731706858015891

'''