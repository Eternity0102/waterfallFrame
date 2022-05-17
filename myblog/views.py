import random
from myblog.blog_db import db
from waterfall.HTTPServer.response import *
from waterfall.HTTPServer.request import Request


base_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'
users_table = db.get_fromTable('users')


class registerClass(Request):
    def get(self,*args,**kwargs):
        return render('register.html',phoneExists=False,nicknameExists=False)

    def post(self,*args,**kwargs):
        print(self.request)
        print(self.browser)
        print(self.paramenter)
        users_table.select = ('phone',)
        users_table.filter = {'phone':self.request['phone']}
        phoneExists = users_table.get_data().get()
        if phoneExists:
            return render('register.html',phoneExists=True,nicknameExists=False)
        users_table.select = ('nickname',)
        users_table.filter = {'nickname':self.request['nickname']}
        nicknameExists = users_table.get_data().get()
        if nicknameExists:
            return render('register.html',phoneExists=False,nicknameExists=True)
        users_table.nickname = self.request['nickname']
        users_table.phone = self.request['phone']
        users_table.email = self.request['email']
        users_table.password = self.request['password']
        users_table.create()
        return render('login_index.html',isFalse=False,loginsuccess=True)


class LoginClass(Request):
    def get(self, *args, **kwargs):
        if 'nickname' in self.cookies and 'ltoken' in self.cookies:
            users_table.select = ('cookies',)
            users_table.filter = {'nickname': self.cookies['name']}
            ltoken = users_table.get_data().get()
            if ltoken and ltoken == self.request['ltoken']:
                return HTTPResponse('读取cookie正常')
        return render('login_index.html', isFalse=False,loginsuccess=False)

    def post(self, *args, **kwargs):
        users_table.select = ('password',)
        users_table.filter = {'phone':self.request['phone']}
        password = users_table.get_data().get()
        if password and password[0][0] == self.request['password']:
            if 'isSaved' in self.request:
                users_table.select = ('nickname',)
                users_table.filter = {'phone': self.request['phone']}
                nickname = users_table.get_data().get()[0][0]
                set_cookie('nickname', nickname)
                ltoken = [random.choice(base_str) for i in range(30)]
                ltoken = ''.join(ltoken)
                users_table.cookies = ltoken
                users_table.where_phone = self.request['phone']
                users_table.update()
                set_cookie('sickname',nickname)
                set_cookie('ltoken',ltoken)
            return HTTPResponse('验证成功')
        else:
            return render('login_index.html', isFalse=True,loginsuccess=False)

