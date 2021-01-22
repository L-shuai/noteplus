"""noteplus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# 静态资源文件服务
from django.conf.urls.static import static

urlpatterns = [
	              path('admin/', admin.site.urls),
	              # 以api/mgr/开头的url，由mgr模块的urls.py处理
	              path('api/mgr/', include('mgr.urls')),
	              # 静态资源目录
              ] + static("/", document_root="./source")  # 若上面的路由没有匹配上，就匹配这个z_dist目录下
