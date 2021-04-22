# 并列柱状图
import matplotlib.pyplot as plt
# plt.figure(num=3, figsize=(8, 5))
plt.rcParams['font.sans-serif']=['SimHei']#设置字体以便支持中文
import numpy as np

x=np.arange(4)#柱状图在横坐标上的位置
#列出你要显示的数据，数据的列表长度与x长度相同
# y1=[1,3,5,4,2]
# y2=[2,5,3,1,6]
y1= [0.8980033592774542,0.8648144554464927,0.8691734560345991,0.7804875150386908]
y2= [0.8912951609371579,0.8679240072899983,0.8719555972828188,0.787043684762799]
y3= [0.8887140594611089,0.8667470718170684,0.8711628007192949,0.7827466486790334]
y4 = [0.8878561036741941,0.8637608792831482,0.8680392172050102,0.7812169469215047]
bar_width=0.15#设置柱状图的宽度
# tick_label=['上海','武汉','南京','天津','南宁']
tick_label=['RBF','Linear','Poly','Sigmoid']

#设置坐标轴名称
plt.xlabel('SVM核函数')
plt.ylabel('模型评估指标')

#设置坐标轴范围
plt.ylim((0.5, 1))

#设置坐标轴刻度
# my_x_ticks = np.arange(-5, 5, 0.5)
my_y_ticks = np.arange(0.5, 1, 0.02)
# plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)

#绘制并列柱状图
plt.bar(x,y1,bar_width,color='red',label='f1-score')
plt.bar(x+bar_width,y2,bar_width,color='salmon',label='accuracy')
plt.bar(x+bar_width*2,y3,bar_width,color='yellow',label='precesion')
plt.bar(x+bar_width*3,y4,bar_width,color='orchid',label='recall')

plt.legend()#显示图例，即label
plt.xticks(x+bar_width*3/2,tick_label)#显示x坐标轴的标签,即tick_label,调整位置，使其落在两个直方图中间位置
plt.show()