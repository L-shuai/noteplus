from django.urls import path

from mgr import sign_in_out,user,note
urlpatterns = [
	# path(浏览器请求路径，具体函数)
	# 路径前面不要带斜杠  最后要带上斜杠
	path('user',user.dispatcher),
	path('note',note.dispatcher),
	path('signin',sign_in_out.signin),
	path('signout',sign_in_out.signout),
	# path('medicines',medicine.dispatcher),
	# path('orders', order.dispatcher),

]
