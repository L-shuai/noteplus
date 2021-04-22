import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']#设置字体以便支持中文
import numpy as np
def fun1():
	"""
	## 探究max_features对LogisticRegression 逻辑回归（二分类）模型的影响
	:return:
	"""
	features = [500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000]
	f1 = [0.5317535861859773, 0.5873312835023502, 0.6313546189536876, 0.6530764646427992, 0.6688806511499569,
	      0.6799675200948291, 0.6859766562872903, 0.6930651671927437, 0.698827415342323, 0.7035542188443452,
	      0.7067144654608659, 0.7090358858259018, 0.7122542786445598, 0.713940704817299]
	plt.plot(features, f1)

	plt.xticks(features)
	# plt.xticks(fontproperties = 'Times New Roman' ,size = 8,rotation = 30)
	# 旋转30度
	plt.xticks(size=8, rotation=30)
	plt.grid()
	plt.xlabel('max_features')
	plt.ylabel('f1_socre')
	# plt.figure(figsize=(200,100),dpi=10)
	# figsize=(12, 6), dpi=100
	plt.savefig('max_features对LogisticRegression 逻辑回归（二分类）模型的影响.png')
	plt.show()



def fun2():
	"""
	LogisticRegression 逻辑回归
	TF-IDF 不同的max_df对结果参数的影响
	:return:
	"""
	max_df = [0.2, 0.4, 0.5, 0.8, 1.0, 1.5, 5]
	f1 = [0.8041509358066935,0.783922912374395,0.7867002916174997,0.7885338160151141,0.7885338160151141,0.7885338160151141,0.7732881248319592]
	plt.plot(max_df, f1)

	# plt.xticks(max_df)
	# plt.xticks(fontproperties = 'Times New Roman' ,size = 8,rotation = 30)
	# 旋转30度
	plt.xticks(size=8, rotation=30)
	plt.grid()
	plt.xlabel('max_df')
	plt.ylabel('f1_socre')
	# plt.figure(figsize=(200,100),dpi=10)
	# figsize=(12, 6), dpi=100
	plt.savefig('LogisticRegression中TF-IDF 不同的max_df对结果参数的影响.png')
	plt.show()


def fun3():
	"""
	LogisticRegression 逻辑回归
	TF-IDF 不同的min_df对结果参数的影响
	:return:
	"""
	min_df = [0., 0.1, 0.2, 0.3, 0.4]
	f1 = [0.7885338160151141,0.5206649914196222,0.43274137638904175,0.33275367244513376,0.23445905615417306]

	plt.plot(min_df, f1)

	# plt.xticks(max_df)
	# plt.xticks(fontproperties = 'Times New Roman' ,size = 8,rotation = 30)
	# 旋转30度
	plt.xticks(size=8, rotation=30)
	# plt.grid()
	plt.xlabel('min_df')
	plt.ylabel('f1_socre')
	# plt.figure(figsize=(200,100),dpi=10)
	# figsize=(12, 6), dpi=100
	plt.savefig('LogisticRegression中TF-IDF 不同的min_df对结果参数的影响.png')
	plt.show()


def fun4():
	"""
	## 数据集简介
	:return:
	"""
	# data = [5, 20, 15, 25, 10]
	labels = ['Python', 'Java', 'Web', 'db', 'sec','5G','ops','mobile','fund','avi','game','iot','other']
	data_train = [3084,2960,1843,2972,2949,2913,2948,2920,2775,2599,2909,2835,2829]
	data_test = [9178,8872,5516,8926,8600,8576,8811,8797,8362,7622,8890,8849,8606]
	plt.bar(labels, data_test, label='训练集')
	plt.bar(labels, data_train, bottom=data_test, label='测试集')
	plt.legend()
	# plt.plot(features, f1)

	# plt.xticks(features)
	# plt.xticks(fontproperties = 'Times New Roman' ,size = 8,rotation = 30)
	# 旋转30度
	plt.xticks(size=8, rotation=30)
	# plt.grid()
	plt.xlabel('文章类别')
	plt.ylabel('数据集大小')
	# plt.figure(figsize=(200,100),dpi=10)
	# figsize=(12, 6), dpi=100
	plt.savefig('数据集描述.png')
	plt.show()

def fun5():
	"""
	## 不同分类算法的评估
	:return:
	"""
	data = [0.8880033592774542,0.5915763488198987, 0.6666085232105665, 0.8745625681126243, 0.8225113119306862, 0.8540816024068543]
	labels = ['SVM','SGD', 'KNN', 'RF', 'LR', 'DT']
	my_y_ticks = np.arange(0, 1, 0.05)
	# plt.xticks(my_x_ticks)
	plt.yticks(my_y_ticks)

	plt.bar(labels, data)
	# plt.legend()
	# plt.plot(features, f1)

	# plt.xticks(features)
	# plt.xticks(fontproperties = 'Times New Roman' ,size = 8,rotation = 30)
	# 旋转30度
	# plt.xticks(size=8, rotation=30)
	# plt.grid()
	plt.xlabel('分类算法')
	plt.ylabel('F1-score')
	# plt.figure(figsize=(200,100),dpi=10)
	# figsize=(12, 6), dpi=100
	plt.savefig('不同分类算法的评估.png')
	plt.show()


if __name__ == '__main__':
	fun5()