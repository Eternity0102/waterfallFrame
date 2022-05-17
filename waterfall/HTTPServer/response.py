import os
import datetime
from waterfall.Htools.templatetools import *
from waterfall.Htools.restools import _response_head, __http_response, _redirect_headers
from waterfall import STATICPATH


cookies: str = ''
sessions: str = ''
# class HttpResponse(object):
#     def __init__(self):
#         cookies: str = ''
#         sessions: str = ''


def __alter_time(seconds):
    GMT_FORMAT = '%a,%d %b %Y %H:%M:%S GMT'
    nowtime = datetime.datetime.now()
    nowtime = str(nowtime.year) + '/' + str(nowtime.month) + '/' + str(nowtime.day) + ' ' + str(nowtime.hour) + ':' + str(
        nowtime.minute) + ':' + str(nowtime.second)
    nowtime = datetime.datetime.strptime(nowtime, "%Y/%m/%d %H:%M:%S")
    nowtime = nowtime + datetime.timedelta(seconds=seconds)
    nowtime = nowtime.strftime(GMT_FORMAT)
    return nowtime


def set_cookie(
               name,
               value,
               domain='',
               path='',
               httpOnly='',
               secure='',
               sameSite='',
               lastAccessed='',
               comment='',
               timeout=60*60*24*15):
    global cookies
    domain = 'domain='+domain+'; ' if domain else ''
    path = 'path='+path+'; ' if path else ''
    expires = 'expires='+__alter_time(timeout)+'; ' if timeout else ''
    httpOnly = 'httpOnly='+httpOnly+'; ' if httpOnly else ''
    secure = 'secure='+str(secure)+'; ' if secure else ''
    sameSite = 'sameSite='+sameSite+'; ' if sameSite else ''
    comment = 'comment='+comment+'; ' if comment else ''
    lastAccessed = 'lastAccessed='+lastAccessed+'; ' if lastAccessed else ''
    cookies += ('Set-Cookie:'+name+'='+value+'; '+domain+path+expires+httpOnly+secure
                     +sameSite+comment+lastAccessed)+'\r\n'


# def set_session( key, value):
#     sessions += key+'='+value+';'


def HTTPResponse(resp):
    resp = __http_response(resp)
    head = _response_head(200, cookies, sessions)
    return head+resp


def render(respFile,**kwargs):
    head = _response_head(200,cookies,sessions)
    with open(STATICPATH['value'] + respFile, 'r') as f:
        strs = f.read()
    strs = BeTags(strs,respFile).run()  # 处理系统标签，继承，注释
    strs = BeSyntaxs(strs,**kwargs).run()  # 处理语句
    strs = BeVars(strs,**kwargs).run()  # 处理变量
    return head+strs


def redirect(reUrl):
    return _redirect_headers(reUrl)
