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
clear_df = pd.read_csv('../trainTestSet2.csv',names=['content','category'])


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

print('SVC training')
clf = SVC(kernel='rbf',C=10,gamma=0.1)
clf.fit(train_x,train_y)
print('SVC predict')
val_pred = clf.predict(test_x)

# 保存模型：
joblib.dump(tfidf, 'tfidf.pkl')
joblib.dump(clf, 'text_clf.pkl')

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


# 打印详细参数
print(metrics.classification_report(test_y, val_pred))

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



'''
最终
分词完毕： Thu Apr  1 23:20:29 2021
<class 'list'>
SVC training
SVC predict
x_train_shape (108642, 198811)
x_test_shape (36214, 198811)
              precision    recall  f1-score   support
          5g       0.93      0.97      0.95      2883
         avi       0.77      0.76      0.76      2540
          db       0.88      0.92      0.90      2919
        fund       0.83      0.82      0.83      2810
        game       0.86      0.86      0.86      2929
         iot       0.79      0.79      0.79      2835
        java       0.84      0.89      0.86      2953
      mobile       0.84      0.87      0.86      2820
         ops       0.84      0.90      0.87      2888
       other       0.84      0.76      0.80      2765
      python       0.90      0.90      0.90      3060
         sec       0.82      0.77      0.80      2952
         web       0.83      0.73      0.78      1860
    accuracy                           0.85     36214
   macro avg       0.84      0.84      0.84     36214
weighted avg       0.85      0.85      0.84     36214
预测结果中各类新闻数目
java      3122
ops       3103
python    3061
db        3025
5g        3007
mobile    2931
game      2928
iot       2847
fund      2771
sec       2767
avi       2509
other     2505
web       1638
dtype: int64
 F1 score为
0.8416453892462792


'''


'''
0.01
结束分词
分词完毕： Fri Apr  2 15:53:36 2021
<class 'list'>
SVC training
SVC predict
x_train_shape (109606, 1006517)
x_test_shape (36536, 1006517)
              precision    recall  f1-score   support
          5g       0.83      0.83      0.83      2940
         avi       0.66      0.18      0.28      2571
          db       0.83      0.69      0.76      2976
        fund       0.64      0.44      0.52      2768
        game       0.50      0.70      0.58      2915
         iot       0.46      0.64      0.53      2839
        java       0.74      0.81      0.78      2974
      mobile       0.78      0.58      0.66      2940
         ops       0.72      0.79      0.75      2931
       other       0.23      0.44      0.30      2822
      python       0.85      0.81      0.83      3077
         sec       0.52      0.40      0.46      2915
         web       0.73      0.48      0.58      1868
    accuracy                           0.61     36536
   macro avg       0.65      0.60      0.60     36536
weighted avg       0.65      0.61      0.61     36536
预测结果中各类新闻数目
other     5460
game      4101
iot       3926
java      3240
ops       3211
python    2947
5g        2938
db        2491
sec       2254
mobile    2171
fund      1889
web       1221
avi        687
dtype: int64
 F1 score为
0.6035265300061353

'''


'''
全部指标
SVC predict
x_train_shape (109606, 1006517)
x_test_shape (36536, 1006517)
              precision    recall  f1-score   support
          5g       0.93      0.96      0.95      2940
         avi       0.81      0.76      0.78      2571
          db       0.93      0.95      0.94      2976
        fund       0.85      0.84      0.85      2768
        game       0.88      0.87      0.88      2915
         iot       0.80      0.81      0.80      2839
        java       0.90      0.94      0.92      2974
      mobile       0.90      0.92      0.91      2940
         ops       0.89      0.92      0.91      2931
       other       0.89      0.84      0.87      2822
      python       0.94      0.95      0.95      3077
         sec       0.84      0.81      0.82      2915
         web       0.86      0.83      0.85      1868
    accuracy                           0.88     36536
   macro avg       0.88      0.88      0.88     36536
weighted avg       0.88      0.88      0.88     36536
预测结果中各类新闻数目
python    3131
java      3107
5g        3054
db        3042
ops       3038
mobile    3007
game      2876
iot       2873
sec       2811
fund      2728
other     2669
avi       2396
web       1804
dtype: int64
 F1 score为
f1_score 0.8780033592774542
accuracy: 0.8812951609371579
precesion: 0.8787140594611089
recall: 0.8778561036741941

'''