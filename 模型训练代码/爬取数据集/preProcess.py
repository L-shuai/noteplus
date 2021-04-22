import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import RidgeClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score


# 全局变量
data_df = ''


# category = ['python','java','web','db','5g','game','mobile','ops','sec','iot','fund','avi','other']
category = ['web','5g','mobile','ops','sec','iot','other']
article_1000 = '/content/drive/Shareddrives/lishuaics-edu-tw/py_data/毕业设计/noteplus-基于SVM自动分类的笔记簿/数据集/article-1000_.csv'
cate_prefix = '/content/drive/Shareddrives/lishuaics-edu-tw/py_data/毕业设计/noteplus-基于SVM自动分类的笔记簿/数据集/'



# 读取数据  指定csv文件
def readFromCSV(path):
  """
  从指定路径的csv文件中读取数据
  """
  data_df = pd.read_csv(path)
  return data_df



# 选出指定类别的数据，并将其索引从0开始编号
def selectCate(cate):
  cate_df = data_df[['title','content','category']][data_df['category']==cate]
  cate_df_ = pd.DataFrame(cate_df)
  cate_df_.index = range(len(cate_df_))
  return cate_df


# 将指定数据写入指定csv文件中
def write2CSV(cate_pd,path):
  cate_pd.to_csv(path,index=True,header=True)
  return None



# 将csv的空白行和空白字段删除
import csv
csv.field_size_limit(100000000)
def delBlankLine():
  in_fnam = 'trainTestSet-60000 (1).csv'
  out_fnam = 'trainTestSet-60000 (2).csv'
  with open(in_fnam,encoding='UTF-8') as in_file:
    with open(out_fnam, 'w',encoding='UTF-8') as out_file:
        writer = csv.writer(out_file)
        for row in csv.reader(in_file):
            if any(row) and '......' not in row :
                writer.writerow(row)



from sklearn import svm
# 使用svm测试数据集F1_Score
def testSVM():
  train_test_data = pd.read_csv('trainTestSet-60000 (1).csv')
  tfidf = TfidfVectorizer(ngram_range=(1,3),max_features=3000)
  # train_test = tfidf.fit_transform(train_test_data['content'].values.astype('U'))   # 词向量 15000*max_features
  train_test = tfidf.fit_transform(train_test_data['content'].values.astype('U'))   # 词向量 15000*max_features

  reg = svm.SVC(C=1.0,kernel='linear',degree=3,gamma='auto',decision_function_shape='ovr')
  reg.fit(train_test[:29980],train_test_data['category'].values[:29980])
  # reg.fit(train_test[:36209],train_test_data['category'].values[:36209])

  # 预测
  val_pred = reg.predict(train_test[30000:35000])
  print('预测结果中各类新闻的数目')
  print(pd.Series(val_pred).value_counts())
  print('\n F1 Score为：')
  print(f1_score(train_test_data['category'].values[30000:35000],val_pred,average='macro'))



if __name__ == '__main__':
  # data_df = readFromCSV(article_1000)
  # for cate in category:
  #   print(cate)
  #   cate_df = selectCate(cate)
  #   cate_path = cate_prefix+cate+'-1000.csv'
  #   write2CSV(cate_pd=cate_df,path=cate_path)
  # testSVM()
  delBlankLine()