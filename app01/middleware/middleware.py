from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class AuthMiddleware(MiddlewareMixin):
    """ 中间件 """

    def process_request(self, request):
        # 排除某些可以不用登录就能直接访问的页面
        if request.path_info in ['/login/', '/image/code/']:
            return

        request_info = request.session.get('info')
        if request_info:
          return

        # 如果session的info信息获取失败，则返回登录页面
        return redirect('/login/')

    # def process_response(self, request, response):
    #     print("M1.process_response")
    #     return response