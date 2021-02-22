import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import RidgeClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score
import jieba
jieba.load_userdict('baidu_stopwords.txt')
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

# 读取数据集  方式二  带编码
csv.field_size_limit(100000000)
# 读取训练集
def readtrain():
    # with open('trainTestSet-60000 (1).csv', 'r',encoding='UTF-8') as csvfile:
    with open('trainTestSet2.csv', 'r',encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # reader = csv.reader(csvfile)
        column1 = [row for row in reader]
    content_train = [i[2] for i in column1[1:]] #第一列为文本内容，并去除列名
    opinion_train = [i[3] for i in column1[1:]] #第二列为类别，并去除列名
    # print(content_train)
    # print(opinion_train)
    print('训练集有 %s 条句子' % len(content_train))
    print('训练集有 %s 个标签' % len(opinion_train))
    train = [content_train, opinion_train]
    return train


train_test_data = readtrain()

train_test_df = pd.DataFrame({'content':train_test_data[0],'category':train_test_data[1]})


# 划分训练集
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(train_test_df.content,train_test_df.category,test_size=0.25,random_state=6)
# x_train,x_test,y_train,_y_test = train_test_split(train_test_data[0],train_test_data[1],test_size=0.25,random_state=6)


# 只取出一部分
x_train = x_train[:200]
x_test = x_test[:30]
y_train = y_train[:200]
y_test = y_test[:30]
print(x_train.shape)
print(x_test.shape)
# 11:07得出score1  0.4866666666666667

# # 将utf8的列表转换成unicode
# def changeListCode(b):
#     a = []
#     for i in b:
#         a.append(i.decode('utf8'))
#     return a

# 对列表进行分词并用空格连接
def segmentWord(cont):
    c = []
    for i in cont:
        a = list(jieba.cut(i))
        b = " ".join(a)
        c.append(b)
    return c


def cutword(x):
    seg = jieba.cut(x)  # 结巴分词函数
    return ' '.join(seg)

print('开始分词')
# x_train = cutword(x_train)
x_train = segmentWord(x_train)
x_test = segmentWord(x_test)
print('结束分词')


from sklearn.feature_extraction.text import TfidfTransformer


# 训练和预测一体
# Pipeline可以将许多算法模型串联起来，可以用于把多个estamitors级联成一个estamitor,比如将特征提取、归一化、分类组织在一起形成一个典型的机器学习问题工作流。
# Pipleline中最后一个之外的所有text_clfs都必须是变换器（transformers），最后一个text_clf可以是任意类型（transformer，classifier，regresser）,如果最后一个text_clf是个分类器，则整个pipeline就可以作为分类器使用，如果最后一个text_clf是个聚类器，则整个pipeline就可以作为聚类器使用。
# text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', SVC(C=0.99, kernel = 'rbf',gamma=1))])
# 添加网格搜索  默认参数不填
# estimator = SVC()
# 加入网格搜索
# estimator = GridSearchCV(estimator,param_grid=param_grid,cv=3)    # 3折搜索
pipe = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('svm', SVC())])
# 未使用网格搜索时
pipe.fit(x_train, y_train)
print("score1:",pipe.score(x_test, y_test))
# 参数网格:（步骤名称）__（参数名称）
param_grid ={'svm__kernel':['rbf'],'svm__C':[0.0001, 0.001,0.1,1,10,100],'svm__gamma': [0.001, 0.0001,0.1,1]}
grid_clf = GridSearchCV(pipe,param_grid=param_grid,n_jobs=4,cv=3)    # 3折搜索
grid_clf.fit(x_train, y_train)

#选出最优参数
best_parameters = grid_clf.best_estimator_.get_params()
for para, val in list(best_parameters.items()):
    print(para, val)


#使用最优参数进行训练
clf = SVC(kernel='rbf', C=best_parameters['svm__C'], gamma=best_parameters['svm__gamma'], probability=True)
clf.fit(x_train,y_train)

# fit完后就可以保存模型了
joblib.dump(clf,'text_clf02-17-rbf-gridscv.pkl')
# text_clf = joblib.load('text_clf.pkl')
# print('test_content:',test_content)
# print('test_content:',test_content)
predicted = clf.predict(x_test)
print('SVC',np.mean(predicted == y_test))
print(set(predicted))

#   方法2：计算准确率
score = clf.score(x_test, y_test)
print('准确率为：\n', score)  # 0.9473684210526315

# 查看最佳参数
print('最佳参数：\n', grid_clf.best_params_)  # {'n_neighbors': 11}
# 查看最佳结果
print('最佳结果：\n', grid_clf.best_score_)  # 0.9734848484848484
# 查看最佳估计器
print('最佳估计器：\n', grid_clf.best_estimator_)  # KNeighborsClassifier(n_neighbors=11)
# 查看最佳交叉验证结果
print('最佳交叉验证结果：\n', grid_clf.cv_results_)

print('训练结束  开始评估')
# 评估
from sklearn.metrics import precision_score
print('准确率：',precision_score(y_test, predicted,average='macro'))
# 精准率：0.9473684210526315

from sklearn.metrics import recall_score
print('召回率：',recall_score(y_test, predicted,average='macro'))
# 召回率：0.8

from sklearn.metrics import f1_score
print('F1 score：',f1_score(y_test, predicted,average='macro'))
# F1 Score 指标：0.8674698795180723

