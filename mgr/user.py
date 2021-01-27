# 处理和用户相关的请求


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
	login = True
	if action != 'register':
		user = request.session.get('user',default = None)
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
	# action = request.params['action']
	if action == 'init_page':
		return init_page(request)
	elif action == 'register':
		return register(request)
	# elif action == 'modify_customer':
	# 	return modifycustomer(request)
	# elif action == 'del_customer':
	# 	return deletecustomer(request)
	# elif action == 'find_customer':
	# 	return findcustomer(request)
	else:
		return JsonResponse({'ret': 1, 'msg': '不支持该类型的http请求'})


# ==========================================================================================================================


def init_page(request):
	"""
	这是登录成功后到index.html的请求
	这里要处理的业务：
		1，获取session中登录的用户username和userid以及email和last_login
		2，查询数据库，获取笔记总数，各个分类的总数，以及各个分类的笔记标题列表（title,id,）,以及收藏的笔记列表和删除的笔记列表
		3，将第2步查询到的内容，全部存入session，以后做修改时（比如增删改查），则对session中的数据也做同步修改，这能大大减少数据库IO时间
	:param request:
	:return:
	"""
	# username = request.session['username']
	# userid = request.session['userid']
	user_dic = request.session.get('user',default = None)
	print('user_dic:',user_dic)
	print('username11:', user_dic['username'], 'id:', user_dic['id'])
	user = User.objects.get(id=user_dic['id'])
	print('user', user.email)
	last_login = str(user.last_login)  # 2021-01-23T03:18:54.836Z

	tmp = last_login[0:10] + ' '

	tmp += last_login[11:19]

	print(tmp)
	user = {
		'id': user.id,
		'username': user.username,
		'email': user.email,
		'last_login': tmp,
	}
	print("user:", user)
	request.session['user'] = user
	return JsonResponse({'ret': 0, 'user': user})


# ==========================================================================================================================


# ==========================================================================================================================

# 用户注册
def register(request):
	try:
		# data是传过来的json  我自定义的data            var jsonstr = {"action": 'add_customer', 'data': {'name': _name, 'phonenumber': _phonenumber, 'address': _address}};
		info = request.params['data']
		username = info['username']
		password = info['password']
		email = info['email']
		# 判断用户名是否存在
		if User.objects.filter(username=username).exists():
			# context = {}
			# context['register_info'] = True
			# context['previous_page'] = request.GET.get('from_page')
			return JsonResponse({'ret':1,'msg':'用户名已被注册！'})
			# return render(request, 'register.html', context)
		else:
			user = User.objects.create_user(username=username,email=email, password=password)
			user.save()
			return JsonResponse({'ret':0,'msg':'注册成功！'})

			# return HttpResponseRedirect(request.GET.get('from_page'))
	except:
		return JsonResponse({'ret': 1, 'msg': '注册过程异常，请重新注册！！'})
