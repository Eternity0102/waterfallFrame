URLS: dict = {}  # 用户的路由记录
STATICPATH: dict = {'value':''}  # 设置的静态变量
REQUEST: dict = {}  # post提交的参数
BROWSER: dict = {}  # 请求的所有参数
CHARSET: dict = {}
COOKIES: dict = {}


def url(urls):
    global URLS
    for url in urls:
        URLS[url] = urls[url]


def _set_static(path):
    global STATICPATH
    STATICPATH['value'] = path


def _set_request(key,value):
    global REQUEST
    REQUEST[key] = value


def _set_browser(key,value):
    global BROWSER,COOKIES
    BROWSER[key.lower().replace('-','_')] = value


def _set_charset(value):
    global CHARSET
    CHARSET['charset'] = value


def _set_cookies(cookieDic):
    global COOKIES
    for cookie in cookieDic:
        COOKIES[cookie] = cookieDic[cookie]