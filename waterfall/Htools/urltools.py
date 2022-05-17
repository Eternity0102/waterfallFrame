import re
from waterfall import URLS, _set_request
from waterfall.Exceptions.Exception import BubblingException
from waterfall.HTTPServer import NOTFOUNDERROR
from waterfall.Htools.reqtools import _response


class _Url(object):
    """处理url的类"""

    def __init__(self, requestUrl, requestArg, requestMethod, connHost, connAddr,recvRequest):
        self.requestUrl = requestUrl
        self.requestArg = requestArg
        self.requestMethod = requestMethod
        self.connHost = connHost
        self.connAddr = connAddr
        self.recvRequest = recvRequest

    def __get_request_args(self):
        if self.requestMethod == "POST":
            requestArgs = re.findall('[\r\n]+?\s*?(.+?=.+?&.*)+?[\r\n]*?', self.recvRequest)
            if requestArgs:
                requestArgs = requestArgs[0].split('&')
        elif self.requestArg:
            requestArgs = self.requestArg.split('&')
        else:
            requestArgs = []
        return requestArgs

    def __url(self):
        """设置url，urldic参数：url正则，处理相关类"""
        for urls in URLS:
            try:
                matchUrl = re.match(urls, self.requestUrl).group()
            except AttributeError:
                continue
            # 判断匹配的url和访问的url是否相等
            if matchUrl == self.requestUrl:
                try:
                    childGroup = re.finditer(urls, self.requestUrl)
                    for child in childGroup:
                        childGroup = child.groups()
                        break
                except IndexError:
                    childGroup = []
                requestArgs = self.__get_request_args()
                for args in requestArgs:
                    kvl = args.split('=')
                    _set_request(kvl[0],kvl[1])
                urlobj = URLS[urls](self.requestMethod, self.connHost, self.connAddr,self.recvRequest, childGroup)
                urlobj._set_option(requestMethod=self.requestMethod)
                break
        else:
            try:
                self.connHost.send(_response(404,NOTFOUNDERROR))
            except BrokenPipeError:
                print('管道破裂，无法回发客户端，异常')
                raise BubblingException()

    def run(self):
        self.__url()