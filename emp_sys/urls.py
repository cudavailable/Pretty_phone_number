"""
URL configuration for emp_sys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from app01 import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 部门管理
    path('dept/list/', views.dept_list),
    path('dept/add/', views.dept_add),
    path('dept/delete/', views.dept_delete),
    path('dept/<int:nid>/edit/', views.dept_edit),

    # 用户管理
    path('user/list/', views.user_list),
    path('user/add/', views.user_add),

    # ModelForm
    path('user/model/form/add/', views.user_model_form_add),
    path('user/<int:nid>/edit/', views.user_edit),
    path('user/<int:nid>/delete/', views.user_delete),

    # 靓号管理
    path('pretty/list/', views.pretty_list),
    path('pretty/add/', views.pretty_add),
    path('pretty/<int:nid>/edit/', views.pretty_edit),
    path('pretty/<int:nid>/delete/', views.pretty_delete),

    # 管理员
    path('admin/list/', views.admin_list),
    path('admin/add/', views.admin_add),
    path('admin/<int:nid>/edit/', views.admin_edit),
    path('admin/<int:nid>/delete/', views.admin_delete),
    path('admin/<int:nid>/reset/', views.admin_reset),

    # 登录
    path('login/', views.login),
    #path('register/', views.register),
    path('logout/', views.logout),
    path('image/code/', views.image_code),

    # ajax
    path('task/list/', views.task_list),
    path('task/ajax/', views.task_ajax),
]
