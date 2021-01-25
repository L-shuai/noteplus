# 处理和笔记相关的请求


# 分发函数
import json
# 返回json的数据
from bs4 import BeautifulSoup
from django.http import JsonResponse
# django内置的user
from django.contrib.auth.models import User
from datetime import datetime

# ==========================================================================================================================
from common.models import Note, Sort


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
	# elif action == 'modify_customer':
	# 	return modifycustomer(request)
	# elif action == 'del_customer':
	# 	return deletecustomer(request)
	# elif action == 'find_customer':
	# 	return findcustomer(request)
	else:
		return JsonResponse({'ret': 1, 'msg': '不支持该类型的http请求'})


# ==========================================================================================================================


def init_page_note(request):
	"""
	这是登录成功后到note.html的请求
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
	# print('username11:', user_dic['username'], 'userid:', user_dic['userid'])
	# user = User.objects.get(id=user_dic['userid'])
	# print('user', user.email)
	# last_login = str(user.last_login)  # 2021-01-23T03:18:54.836Z

	# tmp = last_login[0:10] + ' '

	# tmp += last_login[11:19]

	# print(tmp)
	# user = {
	# 	'id': user.id,
	# 	'username': user.username,
	# 	'email': user.email,
	# 	'last_login': tmp,
	# }
	print("user:", user)
	# request.session['user'] = user
	return JsonResponse({'ret': 0, 'user': user})


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
	# print('content:', content)
	abstract = '这是笔记摘要'
	keyword = '关键词1|关键词2|关键词3'
	img_url = 'https://t7.baidu.com/it/u=1657358789,951623903&fm=193&f=GIF'
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
	                             abstract=abstract, img_url=img_url, author=user, sort=sort, keyword=keyword,
	                             collected=False, deleted=False)
	# print(record.id)
	return JsonResponse({'ret': 0, 'id': record.id})

# ==========================================================================================================================
