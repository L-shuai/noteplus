# 处理和笔记相关的请求


# 分发函数
import json
# 返回json的数据
from bs4 import BeautifulSoup
from django.forms import model_to_dict
from django.http import JsonResponse
# django内置的user
from django.contrib.auth.models import User
from datetime import datetime

# 文本摘要和关键词算法
from FastTextRank.FastTextRank4Sentence import FastTextRank4Sentence
import codecs
import datetime
# 关键词
from FastTextRank.FastTextRank4Word import FastTextRank4Word


# 多条件查询  Q
from django.db.models import Q
# ==========================================================================================================================
from django.shortcuts import render

from common.models import Note  , Sort
from mgr.textUtils.word_cloud import get_WC
from mgr.user import get_notelist


def dispatcher(request):
	# 将请求参数统一放到request的params属性中，方便后续处理  这个params属性是我自定义的

	# GET请求  参数在request对象的GET属性中
	if request.method == 'GET':
		request.params = request.GET

	# POST PUT DELETE请求，从request对象的body属性中获取
	elif request.method in ['POST', 'PUT', 'DELETE']:
		# 根据接口，post put 和delete请求的消息体都是json格式
		request.params = json.loads(request.body)

	# 根据session判断用户是否登录
	action = request.params['action']
	# 若是注册时的请求  则直接跳过  不验证登录
	login = True
	if action != 'register':
		user = request.session.get('user', default=None)
		# # print('note dispatch：user:', user)
		if user is not None:
			if 'username' not in user:
				login = False
		else:
			login = False
	if not login:
		return JsonResponse({
			'ret': 302,
			'msg': '未登录',
			'redirect': '/login.html'},
			status=200)

	# if request.session['usertype'] != 'mgr':
	# 	return JsonResponse({
	# 		'ret': 302,
	# 		'msg': '用户非mgr类型',
	# 		'redirect': '/mgr/sign.html'},
	# 		status=302)

	# 	根据不同action分派给不同的函数进行处理
	action = request.params['action']
	if action == 'init_page_note':
		return init_page_note(request)
	elif action == 'add_note':
		return add_note(request)
	elif action == 'list_note':
		return list_note(request)
	elif action == 'delete_note':
		return delete_note(request)
	elif action == 'get_note':
		return get_note(request)
	elif action == 'get_note_byid':
		return get_note_byid(request)
	elif action == 'init_nav':
		return init_nav(request)
	elif action == 'get_sort_list':
		return get_sort_list(request)
	elif action == 'recover_note':
		return recover_note(request)
	elif action == 'cancel_collect_note':
		return cancel_collect_note(request)
	elif action == 'modify_note':
		return modify_note(request)
	elif action == 'find_note':
		return find_note(request)
	elif action == 'collect_note':
		return collect_note(request)
	# elif action == 'del_customer':
	# 	return deletecustomer(request)
	# elif action == 'find_customer':
	# 	return findcustomer(request)
	else:
		return JsonResponse({'ret': 1, 'msg': '不支持该类型的http请求'})


# ==========================================================================================================================


def init_page_note(request):
	"""
	这是登录成功后到write.html的请求
	这里要处理的业务：
		1，获取session中登录的用户username和userid以及email和last_login
		2，获取session中存的各种分类列表等
		3，完成笔记的添加和编辑删除等
	:param request:
	:return:
	"""
	# username = request.session['username']
	# userid = request.session['userid']
	user = request.session.get('user', default=None)
	# # print('username11:', user_dic['username'], 'userid:', user_dic['userid'])
	# user = User.objects.get(id=user_dic['userid'])
	# # print('user', user.email)
	# last_login = str(user.last_login)  # 2021-01-23T03:18:54.836Z

	# tmp = last_login[0:10] + ' '

	# tmp += last_login[11:19]

	# # print(tmp)
	# user = {
	# 	'id': user.id,
	# 	'username': user.username,
	# 	'email': user.email,
	# 	'last_login': tmp,
	# }
	# # print("user:", user)
	# request.session['user'] = user
	# deletelist = request.session.get('deletelist', default=None)
	# usagelist = request.session.get('usagelist', default=None)
	# collectlist = request.session.get('collectlist', default=None)

	retlist = get_notelist(request)
	# # print(retlist)
	notelist = retlist['notelist']
	collectlist = notelist['collectlist']
	deletelist = notelist['deletelist']
	usagelist = notelist['usagelist']
	return JsonResponse({'ret': 0, 'user': user,
	                     'notelist': {'deletelist': deletelist, 'collectlist': collectlist, 'usagelist': usagelist}})


# ==========================================================================================================================


# ==========================================================================================================================
def add_note(request):
	"""
	添加笔记，提交的数据在post请求体中
	:param request:
	:return:
	"""
	info = request.params['data']
	userid = info['userid']
	note = info['note']
	soup = BeautifulSoup(note['content_html'], 'html.parser')
	content = soup.get_text()
	# # print('content:', content)
	# 文本摘要算法
	mod_sen = FastTextRank4Sentence(use_w2v=False, tol=0.0001)
	# abstract = '这是笔记摘要'
	# abstract = ''
	# for sen in abstract_list:
	# 	abstract += sen
	# 	abstract += '||'
	# # print('abstract:',abstract)
	mod_word = FastTextRank4Word(tol=0.0001, window=2)
	# keyword = '关键词1|关键词2|关键词3'
	cont_len = len(content)
	if cont_len >= 200:
		keyword_list = mod_word.summarize(content, 5)  #取出5个关键词
		# 抽取3个摘要句子  返回数组
		abstract_list = mod_sen.summarize(content, 3)
	elif 100 < cont_len < 200:
		keyword_list = mod_word.summarize(content, 3)  #取出2个关键词
		# 抽取3个摘要句子  返回数组
		abstract_list = mod_sen.summarize(content, 2)
	elif 0< cont_len <= 100:
		keyword_list = mod_word.summarize(content, 1)  #取出1个关键词
		# 抽取3个摘要句子  返回数组
		abstract_list = mod_sen.summarize(content, 1)
	else:
		keyword_list = ''
		abstract_list = ''
	# # print('keyword_list:',keyword_list)
	# 将关键字list拼接  ||
	keyword = keyword_list
	abstract = abstract_list
	# keyword = ''
	# for word in keyword_list:
	# 	keyword+=word
	# 	keyword+='||'
	# 去除最后一个|
	# keyword = keyword.strip('|')
	# # print('keyword:',keyword)
	filepath = get_WC(content)
	# img_url = 'https://t7.baidu.com/it/u=1657358789,951623903&fm=193&f=GIF'
	img_url = 'http://www.noteplus.top/static/space/'+filepath
	user = User.objects.get(id=userid)
	# 这里最好别用filter   因为filter返回的是querySet
	sort = Sort.objects.get(name='python')
	# 从请求消息中  获取要添加客户的信息
	# 并且添加到数据库中
	# 若添加成功，则返回添加后对应的id   record是note类型的  是个对象
	# title content_md  content_html content abstract img_url publish_date modify_date
	# (外键对象) author    sort    keyword collected deleted
	record = Note.objects.create(title=note['title'], content_md=note['content_md'], content_html=note['content_html'],
	                             content=content,
	                             abstract=abstract, img_url=img_url, user=user, sort=sort, keyword=keyword,
	                             collected=False, deleted=False)

	# 向session中添加刚刚创建的笔记
	# usagelist = request.session.get('usagelist', default=None)
	# usagelist.append(record)
	# request.session['usagelist'] = usagelist
	# # print(record.id)
	retlist = get_notelist(request)
	# # print(retlist)
	notelist = retlist['notelist']
	collectlist = notelist['collectlist']
	deletelist = notelist['deletelist']
	usagelist = notelist['usagelist']
	return JsonResponse({'ret': 0, 'id': record.id,'note':model_to_dict(record),
	                     'notelist': {'deletelist': deletelist, 'collectlist': collectlist,
	                                  'usagelist': usagelist}})


# ==========================================================================================================================


# ==========================================================================================================================
def modify_note(request):
	"""
	修改笔记
	:param request:
	:return:
	"""
	info = request.params['data']
	note = info['note']
	try:
		# 根据id从数据库中找到相应的笔记记录
		note_ = Note.objects.get(id=note['id'])
	except Note.DoesNotExist:
		return {
			'ret': 1,
			'msg': '笔记不存在'
		}


	soup = BeautifulSoup(note['content_html'], 'html.parser')
	content = soup.get_text()
	# # print('content:', content)
	# 文本摘要算法
	mod_sen = FastTextRank4Sentence(use_w2v=False, tol=0.0001)
	# abstract = '这是笔记摘要'

	# abstract = ''
	# for sen in abstract_list:
	# 	abstract += sen
	# 	abstract += '||'
	# # print('abstract:',abstract)
	mod_word = FastTextRank4Word(tol=0.0001, window=2)
	# keyword = '关键词1|关键词2|关键词3'
	cont_len = len(content)
	if cont_len >= 200:
		keyword_list = mod_word.summarize(content, 5)  # 取出5个关键词
		# 抽取3个摘要句子  返回数组
		abstract_list = mod_sen.summarize(content, 3)
	elif 100 < cont_len < 200:
		keyword_list = mod_word.summarize(content, 3)  # 取出2个关键词
		# 抽取3个摘要句子  返回数组
		abstract_list = mod_sen.summarize(content, 2)
	elif 0 < cont_len <= 100:
		keyword_list = mod_word.summarize(content, 1)  # 取出1个关键词
		# 抽取3个摘要句子  返回数组
		abstract_list = mod_sen.summarize(content, 1)
	else:
		keyword_list = ''
		abstract_list = ''
	# # print('keyword_list:',keyword_list)
	# 将关键字list拼接  ||
	keyword = keyword_list
	abstract = abstract_list
	# keyword = ''
	# for word in keyword_list:
	# 	keyword+=word
	# 	keyword+='||'
	# 去除最后一个|
	# keyword = keyword.strip('|')
	# # print('keyword:',keyword)
	filepath = get_WC(content)
	# img_url = 'https://t7.baidu.com/it/u=1657358789,951623903&fm=193&f=GIF'
	img_url = 'http://www.noteplus.top/static/space/'+filepath
	# 这里最好别用filter   因为filter返回的是querySet
	sort = Sort.objects.get(name='python')
	# 从请求消息中  获取要添加客户的信息
	# 并且添加到数据库中
	# 若添加成功，则返回添加后对应的id   record是note类型的  是个对象
	# title content_md  content_html content abstract img_url publish_date modify_date
	# (外键对象) author    sort    keyword collected deleted

	if 'title' in note:
		note_.title = note['title']
	if 'content_md' in note:
		note_.content_md = note['content_md']
		note_.content_html = note['content_html']
		note_.content = content
		note_.abstract = abstract
		note_.keyword = keyword
		note_.img_url = img_url

	# 注意，一定要执行save才能将修改信息保存到数据库中
	note_.save()

	# 向session中添加刚刚创建的笔记
	# usagelist = request.session.get('usagelist', default=None)
	# usagelist.append(record)
	# request.session['usagelist'] = usagelist
	# # print(record.id)
	retlist = get_notelist(request)
	# # print(retlist)
	notelist = retlist['notelist']
	collectlist = notelist['collectlist']
	deletelist = notelist['deletelist']
	usagelist = notelist['usagelist']
	return JsonResponse({'ret': 0, 'id': note_.id, 'note': model_to_dict(note_),
	                     'notelist': {'deletelist': deletelist, 'collectlist': collectlist,
	                                  'usagelist': usagelist}})

# ==========================================================================================================================


# ==========================================================================================================================
def list_note(request):
	"""
	根据当前登录的用户，查询所有属于该用户的笔记，不包含已删除的
	:param request:
	:return:
	"""
	# print('*' * 100)

	# # print('sid_get:', sid_get)
	# 先获取session中登录的用户id
	user = request.session.get('user', default=None)

	# 从session中查sid，若没有 代表查询全部笔记 ，否则按照sid分类查询
	sid = request.session.get('sid', default=None)
	userid = user['id']
	# print('userid:', userid)
	retlist = []
	if 'sid' in request.params:
		sid_get = request.params['sid']
		if sid_get is not None:
			# retlist = None
			# 查询回收站
			if sid_get == '-1':
				# print('sid-get=-1')
				# qs是QuerySet对象，包含属于该用户的未被删除的全部笔记
				qs = Note.objects.filter(user_id=userid, deleted=True).values()
				retlist = list(qs)
				for i in range(len(retlist)):
					if len(retlist[i]['content']) > 60:
						retlist[i]['content'] = retlist[i]['content'][0:60] + '...'
						if len(retlist[i]['abstract']) > 30:
							retlist[i]['abstract'] = retlist[i]['abstract'][0:30] + '...]'
				return JsonResponse({'data': retlist})
			# 查询我的收藏
			elif sid_get == '-2':
				# print('sid-get=-2')
				qs = Note.objects.filter(user_id=userid, deleted=False, collected=True).values()
				retlist = list(qs)
				for i in range(len(retlist)):
					if len(retlist[i]['content']) > 60:
						retlist[i]['content'] = retlist[i]['content'][0:60] + '...'
						if len(retlist[i]['abstract']) > 30:
							retlist[i]['abstract'] = retlist[i]['abstract'][0:30] + '...]'
				return JsonResponse({'data': retlist})
			else:
				return JsonResponse({'ret': 1})

	# # print('if over')
	if sid is not None:
		# print('sid is not None')
		qs = Note.objects.filter(user_id=userid, deleted=False, sort_id=sid).values()
		# 	查看后 销毁session
		request.session['sid'] = None
		retlist = list(qs)
		for i in range(len(retlist)):
			if len(retlist[i]['content']) > 60:
				retlist[i]['content'] = retlist[i]['content'][0:60] + '...'
				if len(retlist[i]['abstract']) > 30:
					retlist[i]['abstract'] = retlist[i]['abstract'][0:30] + '...]'
		return JsonResponse({'data': retlist})
	else:
		# print('sid is  None')
		# qs是QuerySet对象，包含属于该用户的未被删除的全部笔记
		qs = Note.objects.filter(user_id=userid, deleted=False).values()
	# 将QuerySet对象转换为list类型。否则不能转化为json字符串
	retlist = list(qs)
	for i in range(len(retlist)):
		if len(retlist[i]['content']) > 60:
			retlist[i]['content'] = retlist[i]['content'][0:60]+'...'
			if len(retlist[i]['abstract']) > 30:
				retlist[i]['abstract'] = retlist[i]['abstract'][0:30]+'...]'
	return JsonResponse({'data': retlist})


# return JsonResponse({'ret':0,'user':user,'retlist':retlist})
# return JsonResponse({'data': retlist})


# ==========================================================================================================================


# ==========================================================================================================================
def delete_note(request):
	"""
	根据笔记的id进行删除，模式包括假删除和彻底删除
	:return:
	"""
	nid = request.params['nid']
	n_type = request.params['n_type']
	# print('nid:', nid)
	try:
		# 根据id从数据库中找到相应的客户记录
		note = Note.objects.get(id=nid)
	except Note.DoesNotExist:
		return {
			'ret': 1,
			'msg': f'id为`{nid}`的笔记不存在'
		}
	# 假删除
	if n_type == 0:
		# print('n_type = 0')
		# delete方法就将该记录从数据库中删除了
		# 这里不使用真正的删除  而是修改deleted变量
		note.deleted = True
		# 注意，一定要执行save才能将修改信息保存到数据库中
		note.save()
	# usagelist = request.session.get('usagelist', default=None)
	# usagelist.remove(note)
	# request.session['usagelist'] = usagelist
	# collectlist = request.session.get('collectlist', default=None)
	# if note in collectlist:
	# 	usagelist.remove(note)
	# request.session['collectlist'] = collectlist



	# 	同步session

	# deletelist = request.session.get('deletelist', default=None)
	# deletelist.append(note)
	# request.session['deletelist'] = deletelist
	# return JsonResponse({'ret': 0, 'msg':'删除成功',
	#                      'notelist': {'deletelist': deletelist, 'collectlist': collectlist,
	#                                   'usagelist': usagelist}})

	# 真删除
	elif n_type == 1:
		# print('n_type = 1')
		# deletelist = request.session.get('deletelist', default=None)
		# deletelist.remove(note)
		# request.session['deletelist'] = deletelist
		note.delete()
	# return JsonResponse({'ret': 1, 'msg': '删除成功','deletelist': deletelist})
	else:
		return JsonResponse({'ret': -1})

	retlist = get_notelist(request)
	# # print(retlist)
	notelist = retlist['notelist']
	collectlist = notelist['collectlist']
	deletelist = notelist['deletelist']
	usagelist = notelist['usagelist']

	return JsonResponse({'ret': 0, 'msg': '删除成功',
	                     'notelist': {'deletelist': deletelist, 'collectlist': collectlist,
	                                  'usagelist': usagelist}})


# ==========================================================================================================================


# ==========================================================================================================================
def recover_note(request):
	"""
	从回收站中恢复该笔记
	:param request:
	:return:
	"""
	nid = request.params['nid']
	# print('nid:', nid)
	try:
		# 根据id从数据库中找到相应的客户记录
		note = Note.objects.get(id=nid)
	except Note.DoesNotExist:
		return {
			'ret': 1,
			'msg': f'id为`{nid}`的笔记不存在'
		}
	# delete方法就将该记录从数据库中删除了
	# 这里不使用真正的删除  而是修改deleted变量
	note.deleted = False
	# 注意，一定要执行save才能将修改信息保存到数据库中
	note.save()
	retlist = get_notelist(request)
	# # print(retlist)
	notelist = retlist['notelist']
	collectlist = notelist['collectlist']
	deletelist = notelist['deletelist']
	usagelist = notelist['usagelist']

	return JsonResponse({'ret': 0, 'msg': '恢复成功',
	                     'notelist': {'deletelist': deletelist, 'collectlist': collectlist,
	                                  'usagelist': usagelist}})


# return JsonResponse({})
# ==========================================================================================================================

# ==========================================================================================================================
def cancel_collect_note(request):
	"""
	从收藏夹中移除该笔记
	:param request:
	:return:
	"""
	nid = request.params['nid']
	# print('nid:', nid)
	try:
		# 根据id从数据库中找到相应的客户记录
		note = Note.objects.get(id=nid)
	except Note.DoesNotExist:
		return {
			'ret': 1,
			'msg': f'id为`{nid}`的笔记不存在'
		}
	# delete方法就将该记录从数据库中删除了
	# 这里不使用真正的删除  而是修改deleted变量
	note.collected = False
	# 注意，一定要执行save才能将修改信息保存到数据库中
	note.save()
	retlist = get_notelist(request)
	# # print(retlist)
	notelist = retlist['notelist']
	collectlist = notelist['collectlist']
	deletelist = notelist['deletelist']
	usagelist = notelist['usagelist']

	return JsonResponse({'ret': 0, 'msg': '取消成功',
	                     'notelist': {'deletelist': deletelist, 'collectlist': collectlist,
	                                  'usagelist': usagelist}})


# ==========================================================================================================================


# ==========================================================================================================================

# ==========================================================================================================================


# ==========================================================================================================================
def get_note(request):
	"""
	前端在list.html页面点击查看或者编辑时，通过ajax传参，将id和type传入，存入session，以便转入新页面时可以获取id
	:param request:
	:return:
	"""
	# info = request.params['data']
	nid = request.params['nid']
	n_type = request.params['n_type']
	# print('nid:', nid, 'n_type:', n_type)
	request.session['nid'] = nid
	request.session['n_type'] = n_type
	redirect = './note.html'
	return JsonResponse({'ret': 0, 'redirect': redirect})


# ==========================================================================================================================


# ==========================================================================================================================
def init_nav(request):
	"""
	在list.html页面  获取侧边栏和顶部的数据    判断是查看还是编辑   n_type=0 | 1
	:param request:
	:return:
	"""
	user = request.session.get('user', default=None)
	# deletelist = request.session.get('deletelist', default=None)
	# usagelist = request.session.get('usagelist', default=None)
	# collectlist = request.session.get('collectlist', default=None)
	retlist = get_notelist(request)
	# # print(retlist)
	notelist = retlist['notelist']
	collectlist = notelist['collectlist']
	deletelist = notelist['deletelist']
	usagelist = notelist['usagelist']
	return JsonResponse({'ret': 0, 'user': user,
	                     'notelist': {'deletelist': deletelist, 'collectlist': collectlist, 'usagelist': usagelist}})


# ==========================================================================================================================


# ==========================================================================================================================
def get_note_byid(request):
	"""
	获取session中存的id和type，在note.html赋值     判断是查看还是编辑   n_type=0 | 1
	:param request:
	:return:
	"""
	nid = request.session.get('nid', default=None)
	n_type = request.session.get('n_type', default=None)
	# print('nid-id:', nid, 'n_type:', n_type)
	try:
		# 根据id从数据库中找到相应的客户记录
		note = Note.objects.get(id=nid)
	# 	将摘要和关键字转为list
		note.abstract = eval(note.abstract)
		note.keyword = eval(note.keyword)

		# last_modify = str(note.modify_date)  # 2021-01-23T03:18:54.836Z
		# # print('last_modify:'+last_modify)
		# tmp = last_modify[0:10] + ' '

		# tmp += last_modify[11:19]
		# # print('tmp:' + tmp)

		# note.publish_date = tmp
	except Note.DoesNotExist:
		return {
			'ret': 1,
			'msg': f'id为`{nid}`的笔记不存在'
		}
	user = request.session.get('user', default=None)

	retlist = get_notelist(request)
	# # print(retlist)
	notelist = retlist['notelist']
	collectlist = notelist['collectlist']
	deletelist = notelist['deletelist']
	usagelist = notelist['usagelist']
	# # print('model_to_dict(note):',model_to_dict(note))
	# # print('note:',note)
	return JsonResponse({'ret': 0, 'note': model_to_dict(note), 'user': user, 'n_type': n_type, 'msg': '返回成功','notelist': {'deletelist': deletelist, 'collectlist': collectlist,
	                                  'usagelist': usagelist}})


# ==========================================================================================================================


# ==========================================================================================================================
def get_sort_list(request):
	"""
	向session中存入要查看的分类id
	:param request:
	:return:
	"""
	sid = request.params['sid']

	# print('sid:', sid, )
	request.session['sid'] = sid
	redirect = './list.html'
	return JsonResponse({'ret': 0, 'redirect': redirect})

# return JsonResponse({})
# ==========================================================================================================================


# ==========================================================================================================================
def find_note(request):
	# 获取当前登录的用户
	user_dic = request.session.get('user', default=None)
	keyword = request.params['keyword']
	# print('keyword:',keyword)
	qs = Note.objects.filter((Q(title__icontains=keyword) | Q(content__icontains=keyword)) & Q(user_id=user_dic['id']) &Q(deleted=False)).values('id','title','content','deleted')
	retlist = list(qs)
	return JsonResponse({'ret':0,'retlist':retlist})


# ==========================================================================================================================


# ==========================================================================================================================
def collect_note(request):
	"""
	收藏笔记  或者取消收藏笔记
	n_type为true代表需要收藏      为false代表取消收藏
	:param request:
	:return:
	"""
	nid = request.params['nid']
	n_type = request.params['n_type']
	try:
		# 根据id从数据库中找到相应的客户记录
		note = Note.objects.get(id=nid)
		if n_type == 'false':
			# 需要取消收藏  将collected改为false
			note.collected = False
		if n_type == 'true':
			note.collected = 'True'
		note.save()
		retlist = get_notelist(request)
		# # print(retlist)
		notelist = retlist['notelist']
		collectlist = notelist['collectlist']
		deletelist = notelist['deletelist']
		usagelist = notelist['usagelist']
		# # print('model_to_dict(note):',model_to_dict(note))
		# # print('note:',note)
		return JsonResponse({'ret': 0, 'note': model_to_dict(note),  'n_type': n_type, 'msg': '收藏/取消收藏成功',
		                     'notelist': {'deletelist': deletelist, 'collectlist': collectlist,
		                                  'usagelist': usagelist}})

	except Note.DoesNotExist:
		return {
			'ret': 1,
			'msg': f'id为`{nid}`的笔记不存在'
		}
	return JsonResponse({'ret': 1, 'msg': '收藏/取消收藏失败'})

# ==========================================================================================================================


# ==========================================================================================================================
def share(request):
	"""
	返回值为字典形式
	:param request:
	:return:
	"""
	# print('nid:',nid)
	nid = request.GET.get('nid')
	print('nid:',nid)
	views_dict = {'name':'菜鸟教程','age':22}
	return render(request,'share.html',{'views_dict':views_dict})

# ==========================================================================================================================


