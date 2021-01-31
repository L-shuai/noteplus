# 处理和用户相关的请求


# 分发函数
import json
# 返回json的数据
from django.http import JsonResponse
# django内置的user
from django.contrib.auth.models import User
from datetime import datetime
# 多条件查询  Q
from django.db.models import Q
# ==========================================================================================================================
from common.models import Note


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
	# action = request.params['action']
	if action == 'init_page':
		return init_page(request)
	elif action == 'register':
		return register(request)
	elif action == 'sendEmail':
		return sendEmail(request)
	elif action == 'sendCode':
		return sendCode(request)
	elif action == 'modify_password':
		return modify_password(request)
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
	user_dic = request.session.get('user', default=None)
	# print('user_dic:', user_dic)
	# print('username11:', user_dic['username'], 'id:', user_dic['id'])
	user = User.objects.get(id=user_dic['id'])
	# print('user', user.email)
	last_login = str(user.last_login)  # 2021-01-23T03:18:54.836Z

	tmp = last_login[0:10] + ' '

	tmp += last_login[11:19]

	date_joined = str(user.date_joined)  # 2021-01-23T03:18:54.836Z

	tmp2 = date_joined[0:10] + ' '

	tmp2 += date_joined[11:19]

	# print(tmp)
	user = {
		'id': user.id,
		'username': user.username,
		'email': user.email,
		'last_login': tmp,
		'date_joined': tmp2,
	}
	# # print("user:", user)
	request.session['user'] = user

	retlist = get_notelist(request)
	# # print(retlist)
	notelist = retlist['notelist']
	collectlist = notelist['collectlist']
	deletelist = notelist['deletelist']
	usagelist = notelist['usagelist']

	# 获取回收站列表
	# qs是QuerySet对象，包含属于该用户的未被删除的全部笔记
	# deleteqs = Note.objects.filter(user_id=user['id'], deleted=True).values()
	# 将QuerySet对象转换为list类型。否则不能转化为json字符串
	# deletelist = list(deleteqs)
	# # print('deletelist:',deletelist)
	# 存入session
	# request.session['deletelist'] = deletelist
	# request.session['collectlist'] = collectlist
	# request.session['usagelist'] = usagelist
	return JsonResponse({'ret': 0, 'user': user,
	                     'notelist': {'deletelist': deletelist, 'collectlist': collectlist, 'usagelist': usagelist}})


# ==========================================================================================================================


# ==========================================================================================================================
def get_notelist(request):
	# request.session['user'] = user
	user_dic = request.session.get('user', default=None)
	# 获取属于该用户的全部笔记  用于以后的分类
	allListqs = Note.objects.filter(user_id=user_dic['id']).values('id', 'title', 'content', 'sort_id', 'collected',
	                                                               'keyword', 'deleted')
	# 将QuerySet对象转换为list类型。否则不能转化为json字符串
	alllist = list(allListqs)
	# 遍历笔记列表
	list_len = len(alllist)
	deletelist = []
	collectlist = []
	usagelist = []
	if list_len > 0:

		for i in range(list_len):
			note = alllist[i]
			if note['deleted']:
				deletelist.append(note)
			elif note['collected']:
				collectlist.append(note)
			else:
				# sortId = note['sort_id']
				# # print('sortId:',sortId)
				# sortId = 'sort'
				usagelist.append(note)

	# # print('deletelist:',deletelist)
	# # print('collectlist:',collectlist)
	# # print('usagelist:',usagelist)

	# 获取回收站列表
	# qs是QuerySet对象，包含属于该用户的未被删除的全部笔记
	# deleteqs = Note.objects.filter(user_id=user['id'], deleted=True).values()
	# 将QuerySet对象转换为list类型。否则不能转化为json字符串
	# deletelist = list(deleteqs)
	# # print('deletelist:',deletelist)
	# 存入session
	# request.session['deletelist'] = deletelist
	# request.session['collectlist'] = collectlist
	# request.session['usagelist'] = usagelist
	notelist = {'notelist': {'deletelist': deletelist, 'collectlist': collectlist, 'usagelist': usagelist}}
	return notelist


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
		code = info['code']
		# 判断用户名是否存在
		if User.objects.filter(username=username).exists():
			# context = {}
			# context['register_info'] = True
			# context['previous_page'] = request.GET.get('from_page')
			return JsonResponse({'ret': 1, 'msg': '用户名已被注册！'})
		# return render(request, 'register.html', context)
		else:
			# 从session中取出code
			code_ = ''
			if 'code' in request.session:
				code_ = request.session.get('code', default=None)
				if code == code_:
					user = User.objects.create_user(username=username, email=email, password=password)
					user.save()
				# 	注册成功后，将session中的code销毁
					request.session['code'] = None
				else:
					return JsonResponse({'ret': 1, 'msg': '验证码错误！'})

			else:
				return JsonResponse({'ret': 1, 'msg': '注册过程异常，请重新注册！！'})

			return JsonResponse({'ret': 0, 'msg': '注册成功！'})

	# return HttpResponseRedirect(request.GET.get('from_page'))
	except:
		return JsonResponse({'ret': 1, 'msg': '注册过程异常，请重新注册！！'})


import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

import random


def getcode(n):
	str = ""
	for i in range(n):
		ch = chr(random.randrange(ord('0'), ord('9') + 1))
		str += ch
	return str


def sendEmail(request):
	try:
		# data是传过来的json  我自定义的data            var jsonstr = {"action": 'add_customer', 'data': {'name': _name, 'phonenumber': _phonenumber, 'address': _address}};
		# info = request.params['data']
		username = request.params['username']
		# password = info['password']
		email = request.params['email']
		receiver = email
		# 判断用户名是否存在
		qs1 = User.objects.filter(username=username).values('id')
		qs2 = User.objects.filter(email=email).values('id')
		if len(list(qs1)) > 0:
			# context = {}
			# context['register_info'] = True
			# context['previous_page'] = request.GET.get('from_page')
			return JsonResponse({'ret': 1, 'msg': '用户名已被注册！'})
		elif len(list(qs2)) > 0:
			return JsonResponse({'ret': 1, 'msg': '邮箱已被注册！'})
		# return render(request, 'register.html', context)
		else:
			# 可以发送邮件
			my_sender = 'noteplus@88.com'  # 发件人邮箱账号
			my_pass = 'xvm2HKBPmcyESBUI'  # 发件人邮箱的授权码
			# my_user = '1472174772@qq.com'  # 收件人邮箱账号，我这边发送给自己

			# same = ['leeshuai@88.com', 'WTCIfPyJinpCnPK5','smtp.88.com','欢迎注册noteplus','尊敬的用户：您好！ 您正在进行注册操作，请填入验证码：','。此为系统邮件，请勿回复！']
			code = getcode(6)  # 生成6位数
			ret = True
			try:
				msg = MIMEText('尊敬的用户：您好！ 您正在进行注册操作，请填入验证码：' + code + '。此为系统邮件，请勿回复！', 'plain', 'utf-8')
				msg['From'] = formataddr(["www.noteplus.top", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
				msg['To'] = formataddr(["register", receiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
				msg['Subject'] = "欢迎注册noteplus"  # 邮件的主题，也可以说是标题
				server = smtplib.SMTP_SSL("smtp.88.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
				server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
				server.sendmail(my_sender, [receiver, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
				print('send ok')
				server.quit()  # 关闭连接
			except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的ret=False
				ret = False
			if ret:
				# 将code存入session
				request.session['code'] = code
				return JsonResponse({'ret': 0, 'msg': '发送成功', 'code': code})
			else:
				return JsonResponse({'ret': 1, 'msg': '发送失败'})
	except Exception as e:
		# print('e',e)
		return JsonResponse({'ret': 1, 'msg': '注册过程异常，请重新注册！！'})

# ret = sendEmail()
# if ret:
# 	print("邮件发送成功")
# else:
# 	print("邮件发送失败")


# def sendvarify():
# 	# -*- coding: UTF-8 -*-
# 	import requests
# 	import random
# 	from bs4 import BeautifulSoup
# 	from datetime import datetime
# 	from email.header import Header
# 	from email.mime.text import MIMEText
# 	from email.utils import parseaddr, formataddr
# 	import smtplib
# 		msg_from = 'leeshuai@88.com'  # 发送方邮箱
# 		passwd = 'WTCIfPyJinpCnPK5'  # 填入发送方邮箱的授权码
# 		# receivers = ['321657622@qq.com,']  # 收件人邮箱
#
# 		subject = '今日份的睡前小故事'  # 主题
# 		# html=getHTMLText(url,headers)
# 		# content=parsehtml2(html)
# 		content = '我要发给你的小故事'  # 正文
# 		msg = MIMEText(content)
# 		msg['Subject'] = subject
# 		msg['From'] = msg_from
# 		msg['To'] = ','.join(receivers)
# 		print('封装完成')
# 		s = smtplib.SMTP_SSL("smtp.88.com", 465)  # 邮件服务器及端口号
# 		print('建立链接')
# 		try:
# 			# s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
# 			s.login(msg_from, passwd)
# 			s.sendmail(msg_from, msg['To'].split(','), msg.as_string())
# 			print("发送成功")
# 		except:
# 			print("发送失败")
# 		finally:
# 			s.quit()
#
# 	if __name__ == '__main__':
# 		sendemail2()
#
# 	return None


#
def modify_password(request):

	info = request.params['data']
	user = request.session.get('user',default=None)
	# 取出session中的code
	if 'code' in request.session:
		code = request.session.get('code',default=None)
		code_ = info['code']
		if code == code_:

			try:
				# 根据id从数据库中找到相应的客户记录
				user = User.objects.get(id=user['id'])
			except User.DoesNotExist:
				return {
					'ret': 1,
					'msg': '用户不存在'
				}
			psw1=''
			psw2=''

			# 	获取新密码
			if 'psw' in info:
				psw = info['psw']
			user.set_password(psw)
			user.save()
			# 修改成功后，将session中的code销毁
			request.session['code'] = None
			return JsonResponse({'ret':0,'msg':'密码修改成功'})
		else:
			return JsonResponse({'ret':1,'msg':'验证码错误'})

	else:
		return JsonResponse({'ret':1,'msg':'密码修改失败'})




def sendCode(request):
	try:
		# data是传过来的json  我自定义的data            var jsonstr = {"action": 'add_customer', 'data': {'name': _name, 'phonenumber': _phonenumber, 'address': _address}};
		# info = request.params['data']
		user_dic = request.session.get('user')
		user = User.objects.get(id=user_dic['id'])
		receiver = user.email

		# 可以发送邮件
		my_sender = 'noteplus@88.com'  # 发件人邮箱账号
		my_pass = 'xvm2HKBPmcyESBUI'  # 发件人邮箱的授权码
		# my_user = '1472174772@qq.com'  # 收件人邮箱账号，我这边发送给自己

		# same = ['leeshuai@88.com', 'WTCIfPyJinpCnPK5','smtp.88.com','欢迎注册noteplus','尊敬的用户：您好！ 您正在进行注册操作，请填入验证码：','。此为系统邮件，请勿回复！']
		code = getcode(6)  # 生成6位数
		ret = True
		try:
			msg = MIMEText('尊敬的用户：您好！ 您正在进行修改密码操作，请填入验证码：' + code + '。此为系统邮件，请勿回复！', 'plain', 'utf-8')
			msg['From'] = formataddr(["www.noteplus.top", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
			msg['To'] = formataddr(["register", receiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
			msg['Subject'] = "修改密码noteplus"  # 邮件的主题，也可以说是标题
			server = smtplib.SMTP_SSL("smtp.88.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
			server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
			server.sendmail(my_sender, [receiver, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
			print('send ok')
			server.quit()  # 关闭连接
		except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的ret=False
			ret = False
		if ret:
			# 将code存入session
			request.session['code'] = code
			return JsonResponse({'ret': 0, 'msg': '发送成功', 'code': code})
		else:
			return JsonResponse({'ret': 1, 'msg': '发送失败'})
	except Exception as e:
		# print('e',e)
		return JsonResponse({'ret': 1, 'msg': '注册过程异常，请重新注册！！'})
