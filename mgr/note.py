# 处理和笔记相关的请求


# 分发函数
import json
# 返回json的数据
from django.http import JsonResponse
# django内置的user
from django.contrib.auth.models import User
from datetime import datetime


# ==========================================================================================================================

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
	if action != 'register':
		if 'username' not in request.session['user']:
			return JsonResponse({
				'ret': 302,
				'msg': '未登录',
				'redirect': 'http://127.0.0.1:8000/login.html'},
				status=200)

	# if request.session['usertype'] != 'mgr':
	# 	return JsonResponse({
	# 		'ret': 302,
	# 		'msg': '用户非mgr类型',
	# 		'redirect': '/mgr/sign.html'},
	# 		status=302)



	# 	根据不同action分派给不同的函数进行处理
	# action = request.params['action']
	if action == 'init_page_note':
		return init_page_note(request)
	# elif action == 'register':
	# 	return register(request)
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
	user = request.session['user']
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
