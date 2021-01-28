from django.db import models
# django内置的user
from django.contrib.auth.models import User
import datetime
# Create your models here.
'''
common这个app是专门用来存放一些公共的对象  model
'''


# django定义对象，需要继承models.Model

# 笔记分类
class Sort(models.Model):
	# 分类名称
	name = models.CharField(max_length=200)
	# 分类描述   可为空
	sort_desc = models.CharField(max_length=200, null=True, blank=True)

	def to_dict(self):
		data = {}
		for f in self._meta.concrete_fields:
			data[f.name] = f.value_from_object(self)
		return data


# 笔记表
class Note(models.Model):
	# 标题
	title = models.CharField(max_length=200)
	# 内容  markdown格式的   长文本
	content_md = models.TextField()
	# 内容  html格式的   长文本
	content_html = models.TextField()
	# 内容  纯文本格式的   长文本
	content = models.TextField()
	# 作者  # 外键 User表的主键   在数据库中的列为user_id
	user = models.ForeignKey(User,on_delete=models.PROTECT)
	# 分类  外键  Sort表的主键  sort_id
	sort = models.ForeignKey(Sort,on_delete=models.PROTECT)
	# 内容摘要  自动生成的
	abstract = models.TextField()
	# 关键词  可能有多个 用|分开
	keyword = models.CharField(max_length=200,default='关键词')
	# 词云图的url
	img_url = models.CharField(max_length=200)
	# 发布日期
	publish_date = models.DateTimeField(default=datetime.datetime.now())  #默认值为创建时的时间
	# 修改编辑日期   更新该记录时，这个字段会自动更新   前端不需要传来具体时间
	modify_date = models.DateTimeField(auto_now=True)
	# 被删除标志
	deleted = models.BooleanField(default=False)
	# 被收藏标志
	collected = models.BooleanField(default=False)

	def to_dict(self):
		data = {}
		for f in self._meta.concrete_fields:
			data[f.name] = f.value_from_object(self)
		return data



# 将sort和note注册到admin模块中，这样能在admin后台直接操作
from django.contrib import admin

admin.site.register(Sort)
admin.site.register(Note)