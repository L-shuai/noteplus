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

# ==========================================================================================================================
from django.shortcuts import render

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
		# print('note dispatch：user:', user)
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
	# print("user:", user)
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
	                             abstract=abstract, img_url=img_url, user=user, sort=sort, keyword=keyword,
	                             collected=False, deleted=False)
	# print(record.id)
	return JsonResponse({'ret': 0, 'id': record.id})


# ==========================================================================================================================


# ==========================================================================================================================
def list_note(request):
	"""
	根据当前登录的用户，查询所有属于该用户的笔记，不包含已删除的
	:param request:
	:return:
	"""
	print('*' * 100)
	# 先获取session中登录的用户id
	user = request.session.get('user', default=None)
	userid = user['id']
	print('userid:', userid)
	# qs是QuerySet对象，包含属于该用户的未被删除的全部笔记
	qs = Note.objects.filter(user_id=userid, deleted=False).values()
	# 将QuerySet对象转换为list类型。否则不能转化为json字符串
	retlist = list(qs)

	# return JsonResponse({'ret':0,'user':user,'retlist':retlist})
	return JsonResponse({'data': retlist})


# ==========================================================================================================================


# ==========================================================================================================================
def delete_note(request):
	"""
	根据笔记的id进行删除
	:return:
	"""
	nid = request.params['id']
	print('nid:', nid)
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
	note.deleted = True
	# 注意，一定要执行save才能将修改信息保存到数据库中
	note.save()
	return JsonResponse({'ret': 0, 'msg': '删除成功'})


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
	print('nid:', nid, 'n_type:', n_type)
	request.session['nid'] = nid
	request.session['n_type'] = n_type
	redirect = './note.html'
	return JsonResponse({'ret': 0, 'redirect': redirect})


# ==========================================================================================================================


# ==========================================================================================================================
def init_nav(request):
	"""
	在list.html页面  获取侧边栏和顶部的数据
	:param request:
	:return:
	"""
	user = request.session.get('user', default=None)
	return JsonResponse({'ret':0,'user':user})

# ==========================================================================================================================


# ==========================================================================================================================
def get_note_byid(request):
	"""
	获取session中存的id和type，在note.html赋值
	:param request:
	:return:
	"""
	nid = request.session.get('nid',default=None)
	n_type = request.session.get('n_type',default=None)
	print('nid-id:', nid, 'n_type:', n_type)
	try:
		# 根据id从数据库中找到相应的客户记录
		note = Note.objects.get(id=nid)
	except Note.DoesNotExist:
		return {
			'ret': 1,
			'msg': f'id为`{nid}`的笔记不存在'
		}
	user = request.session.get('user', default=None)
	# print('note:',note)
	return JsonResponse({'ret':0,'note':model_to_dict(note),'user':user,'n_type':n_type,'msg':'返回成功'})



# ==========================================================================================================================


