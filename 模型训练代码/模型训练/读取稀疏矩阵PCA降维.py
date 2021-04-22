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

pca = TruncatedSVD(n_components=8000)
# 保留95% 的信息

# train_x = train_x.toarray()
# test_x = test_x.toarray()


train_x_pca = pca.fit_transform(train_x)
test_x_pca = pca.transform(test_x)

print('x_train_pca_shape',train_x_pca.shape)
print('x_test_pca_shape',test_x_pca.shape)
# reg = linear_model.LogisticRegression(penalty='l2',C=1.0,solver='liblinear')
# reg.fit(x_train,y_train)

print('svc training begin')
clf = SVC(kernel='rbf',C=10,gamma=0.1)
clf.fit(train_x_pca,train_y)
print('train over')
print('predict begin')
val_pred = clf.predict(test_x_pca)
print('predict over')


# 打印详细参数
print(metrics.classification_report(test_y, val_pred))

print('预测结果中各类新闻数目')
print(pd.Series(val_pred).value_counts())
print('\n F1 score为')
print(f1_score(y_test, val_pred, average='macro'))



# 5000规模：F1 score为
# 0.16691994286054326


"""
"D:\Program File(x86)\python\python.exe" "D:\Program File(x86)\Pycharm2020-3\PyCharm 2020.3\plugins\python\helpers\pydev\pydevconsole.py" --mode=client --port=51233
import sys; print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend(['E:\\IT\\Python\\pystudy\\demo\\黑马程序员_机器学习', 'E:/IT/Python/pystudy/demo/黑马程序员_机器学习'])
PyDev console: starting.
Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:57:54) [MSC v.1924 64 bit (AMD64)] on win32
runfile('E:/IT/Python/pystudy/demo/黑马程序员_机器学习/毕设论文/读取数据集PCA降维.py', wdir='E:/IT/Python/pystudy/demo/黑马程序员_机器学习/毕设论文')
Building prefix dict from the default dictionary ...
Loading model from cache C:\Users\TOP\AppData\Local\Temp\jieba.cache
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

"""