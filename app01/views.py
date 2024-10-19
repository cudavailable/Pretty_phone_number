from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from app01.utils.my_model_form import *

# Create your views here.
def dept_list(request):
    """部门列表"""
    query_set = models.Department.objects.all()

    return render(request, 'dept_list.html', {'query_set': query_set})

def dept_add(request):
    """添加部门"""
    if request.method == 'GET':
        return render(request, 'dept_add.html')

    # 如果是POST方法：
    dname = request.POST.get('dname')

    models.Department.objects.create(dname=dname)

    return redirect('/dept/list/')

# /dept/delete/?nid=9
def dept_delete(request):
    """删除部门"""
    nid = request.GET.get('nid')

    models.Department.objects.filter(id=nid).delete()

    return redirect('/dept/list/')

def dept_edit(request, nid):
    """编辑部门"""
    if request.method == 'GET':
        query_ans = models.Department.objects.filter(id=nid).first()
        return render(request, 'dept_edit.html', {'query_ans': query_ans})

    # 如果是post方法：
    dname = request.POST.get('dname')

    models.Department.objects.filter(id=nid).update(dname=dname)

    return redirect('/dept/list/')

def user_list(request):
    """用户列表"""
    user_list = models.UserInfo.objects.all()

    page_obj = pagiantion(request, user_list)
    context = {
        "user_list": page_obj.query_set,
        "page_string": page_obj.html(),
    }

    # 用python的语法获取数据表项
    # for obj in user_list:
    #     print(obj.id, obj.name, obj.pwd, obj.age, obj.sal, obj.crt_time.strftime('%Y-%m-%d'), obj.get_gender_display(), obj.dept.dname)

    return render(request, 'user_list.html', context)

def user_add(request):
    """添加用户"""

    if request.method == 'GET':
        context = {
            "gender_choices": models.UserInfo.gender_choices,
            "dept_list": models.Department.objects.all(),
        }
        return render(request, 'user_add.html', context)

    # 如果是post方法，获取提交的数据表项
    name = request.POST.get('name')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    sal = request.POST.get('sal')
    crt_time = request.POST.get('crt_time')
    gender = request.POST.get('gender')  # 数字代表性别
    dept = request.POST.get('dept')     # 部门号代表

    models.UserInfo.objects.create(name=name, pwd=pwd, age=age, sal=sal,
                                   crt_time=crt_time, gender=gender, dept_id=dept)
    return redirect('/user/list/')

def user_model_form_add(request):
    """新建用户ModelForm"""
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})

    # 如果是post方法，就提取数据表项，并进行校验
    form = UserModelForm(data=request.POST)  # 将POST提交的数据，交给form

    if form.is_valid():
        # print(form.cleaned_data)  # 输出正确结果
        form.save()     # 将获取的数据保存到数据库
        return redirect('/user/list/')

    # print(form.errors)  # 输出错误信息
    return render(request, 'user_model_form_add.html', {"form": form})

def user_edit(request, nid):
    """编辑用户"""
    row_obj = models.UserInfo.objects.filter(id=nid).first()  # 筛选出对应ID的一行记录

    if request.method == 'GET':
        #row_obj = models.UserInfo.objects.filter(id=nid).first()  # 筛选出对应ID的一行记录

        form = UserModelForm(instance=row_obj)  # 提交选中的记录，并且显示原来的信息
        return render(request, 'user_edit.html', {"form": form})

    # 如果是POST方法，需要更新数据库中的相关记录
    # row_obj = models.UserInfo.objects.filter(id=nid).first()
    form = UserModelForm(data=request.POST, instance=row_obj)  # 收取POST的数据

    # 信息校验
    if form.is_valid():
        # form.instance.password = '123'  # 若需要保存到数据库的字段有的没在页面表单里
        form.save()  # 保存到数据库，需要指定到某个确定的记录
        return redirect('/user/list/')

    # 如果校验有误
    return render(request, 'user_edit.html', {"form": form})

def user_delete(request, nid):
    """删除用户"""
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')

from app01.utils.pagination import pagiantion
def pretty_list(request):
    """靓号列表"""

    dict_list = {}
    search_data = request.GET.get('q', "")
    if search_data:
        dict_list['mobile__contains'] = search_data

    # 根据用户需要，分页展示 ###########################

    query_set = models.PrettyNum.objects.filter(**dict_list).order_by('-level')  # 从数据库中取出所需要的记录，传递给分页组件
    page_obj = pagiantion(request, query_set, pagenum=4)   # 实例化分页组件

    # 获取分页结果
    page_string = page_obj.html()

    # 传递给前端的参数配置
    context = {
        "query_set": page_obj.query_set, "search_data": search_data, "page_string": page_string,
        # "prev_page": prev_page, "post_page": post_page
    }

    # query_set = models.PrettyNum.objects.all().order_by('-level')  # select * from app01_prettynum order by level desc
    return render(request, 'pretty_list.html', context)

def pretty_add(request):
    """添加靓号"""
    if request.method == 'GET':
        form = PrettyNumModelForm()
        return render(request, 'pretty_add.html', {"form": form})

    # 如果是post方法
    form = PrettyNumModelForm(data=request.POST)
    # 错误校验
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    # 若有错误
    return render(request, 'pretty_add.html', {"form": form})

def pretty_edit(request, nid):
    """编辑靓号"""
    row_obj = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = PrettyNumModelForm(instance=row_obj)
        return render(request, 'pretty_edit.html', {"form": form})

    # 若是POST方法
    form = PrettyNumModelForm(instance=row_obj, data=request.POST)
    # 错误校验
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    # 发现有错误
    return render(request, 'pretty_edit.html', {"form": form})

def pretty_delete(request, nid):
    """删除靓号"""
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list/")

def admin_list(request):
    """管理员列表"""

    dict_list = {}
    search_data = request.GET.get('q', "")
    if search_data:
        dict_list['username__contains'] = search_data

    query_set = models.Admin.objects.filter(**dict_list)  # 需要提取的数据记录
    page_obj = pagiantion(request, query_set)  # 分页组件实例化

    context = {
        "query_set": query_set,
        "search_data": search_data,
        "page_string": page_obj.html(),
    }

    return render(request, 'admin_list.html', context)

def admin_add(request):
    """添加管理员"""
    title = "添加管理员"
    if request.method == 'GET':
        form = AdminModelForm()
        context = {
            "title": title,
            "form": form,
        }

        return render(request, 'change.html', context)

    # 若是POST方法
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    # 若有误
    return render(request, 'change.html', {"title": title, "form": form})

def admin_edit(request, nid):
    """编辑管理员信息"""
    row_obj = models.Admin.objects.filter(id=nid).first()
    if not row_obj:
        return redirect('/admin/list/')

    # 如果编辑页面请求有效
    title = "编辑管理员信息"
    if request.method == 'GET':
        """GET method"""
        form = AdminModelForm()
        return render(request, 'change.html', {"title": title, "form": form})

    # 如果是POST方法
    form = AdminModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    # 如果输入有误
    return render(request, 'change.html', {"title": title, "form": form})

def admin_delete(request, nid):
    """删除管理员"""
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')

def admin_reset(request, nid):
    """管理员重置密码"""
    row_obj = models.Admin.objects.filter(id=nid).first()
    if not row_obj:
        return redirect('/admin/list/')

    title = "重置密码 - {}".format(row_obj.username)

    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'change.html', {'title': title, 'form': form})

    # 如果是POST方法
    form = AdminResetModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    # 如果校验出错
    return render(request, 'change.html', {'title': title, 'form': form})

def login(request):
    """登录"""
    if request.method == 'GET':
        form = LoginForm(my_class='e')
        return render(request, 'login.html', {"form": form})

    # 如果是POST方法
    form = LoginForm(my_class='e', data=request.POST)
    if form.is_valid():

        # 校验验证码
        user_input_code = form.cleaned_data.pop('code')  # 获取验证码文本，同时弹出code项
        code = request.session.get('code', '')

        if code.upper() != user_input_code.upper():
            form.add_error('code', '验证码不正确')
            return render(request, 'login.html', {"form": form})

        admin_obj = models.Admin.objects.filter(**form.cleaned_data).first()
        print(form.cleaned_data)

        if not admin_obj:
            # 如果admin_obj是None，即数据库表中没有相应的用户记录
            form.add_error('password', '用户名或者密码不正确')
            return render(request, 'login.html', {"form": form})

        # 如果提交成功，则进入主页面
        # 给浏览器添加cookie，自己也保存cookie到django02_session
        request.session['info'] = {'id': admin_obj.id, 'username': admin_obj.username}
        # 重新设置session有效期：7天
        request.session.set_expiry(60*60*24*7)
        return redirect('/admin/list/')

    # 如果校验出错
    return render(request, 'login.html', {"form": form})

# def register(request):
#     """注册"""
#     if request.method == 'GET':
#         form = LoginForm(my_class='e')
#         return render(request, 'login.html', {"form": form})
# 
#     # 如果是POST方法
#     form = LoginForm(my_class='e', data=request.POST)
#     if form.is_valid():
#         print(form.cleaned_data)
#         return redirect('/admin/list/')
# 
#     # 如果校验出错
#     return render(request, 'login.html', {"form": form})

from app01.utils.code import check_code
from io import BytesIO

def image_code(request):
    """生成图片验证码"""
    img, code_str = check_code()

    # 保存验证码文本，便于后续验证码校验
    request.session['code'] = code_str
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())

def logout(request):
    """注销"""
    
    request.session.clear()  # 清除session
    return redirect('/login/')  # 返回登录界面

def task_list(request):
    """任务列表"""
    return render(request, 'task_list.html')

from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
# 使用装饰器，免除csrf
@csrf_exempt
def task_ajax(request):
    data_dict = {"status": True, "data": [11, 22, 2, 3, 4]}
    # json_str = json.dumps(data_dict)
    # return HttpResponse(json_str)
    return JsonResponse(data_dict)
    
