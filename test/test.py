import os
import traceback
from waterfall.Exceptions.Exception import TagIsNotCloseExecption
from waterfall.HTTPServer.httpserver import HTTPServer
from waterfall import url
from waterfall.HTTPServer.response import *
from waterfall.HTTPServer.request import Request
import re


def test():
    class registerClass(Request):
        def get(self,*args,**kwargs):
            return render('register.html')

    class LoginClass(Request):
        def get(self,*args,**kwargs):
            return render('login_index.html')

    class ImgClass(Request):
        def post(self):
            pass
            print('post浏览器提交的键值对:', self.request)
            print('post浏览器的请求所有具体参数:', self.browser)
            print('post url中匹配的正则子组：', self.paramenter)
            # print('')

    class IndexClass(Request):
        def get(self):
            print('浏览器提交的键值对:', self.request)
            print('浏览器的请求所有具体参数:',self.browser)
            print('url中匹配的正则子组：',self.paramenter)
            return render('index.html', name='cc', age=88)

    class RtnMethod(Request):
        def get(self,*args,**kwargs):
            # self.write('abc')
            # self.write('123')
            # self.write('456')
            set_cookie('name','qgd',timeout=60*60)
            set_cookie('age','22')
            print(cookies)
            return redirect('/test?name=cc&age=88')

    class extendsClass(Request):
        def get(self):
            return render('extend2.html')

    class TestTagClass(Request):
        def get(self):
            return render(
                'testif-for.html',
                name = self.request['name'],
                age = self.request['age'],
                lst={'a':'a1','b':'b2','c':'c3'},
            )

    class Test1Class(Request):
        def get(self):
            return render('index.html')

    url(
        {
            '/register':registerClass,
            '/login':LoginClass,
            '/index':IndexClass,
            '/img':ImgClass,
            '/return':RtnMethod,
            '/tag':TestTagClass,
            '/extends': extendsClass,
            '^/index/(\w+)/(\d+)': IndexClass,
            '/test': IndexClass,
            '/test1': Test1Class,
            'ccc': Test1Class,
            'bbb': IndexClass,
        }
    )

    server = HTTPServer('127.0.0.1', 8888)
    server.static_path = 'static/'
    server.run()

test()
# class Test:
#     def get(self):
#         a = HttpResponse()
#         for i in range(20):
#             print('dododo')
#
#     def run(self):
#         pass
#
# print(bool(Test().run()))


