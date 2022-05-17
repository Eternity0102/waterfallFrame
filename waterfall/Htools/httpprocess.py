import os
import time
import traceback
import urllib.parse
from threading import Thread
from waterfall import STATICPATH, _set_browser, CHARSET, _set_cookies
from waterfall.HTTPServer import SERVERERROR
from waterfall.Exceptions.Exception import BubblingException
from waterfall.Htools.reqtools import _response, _RequestStrHandler
from waterfall.Htools.restools import _browser
from waterfall.Htools.urltools import _Url


class _HandlerRequestThread(Thread):
    def __init__(self, connHost, connAddr):
        super().__init__()
        self.connHost = connHost
        self.connAddr = connAddr
        self.requestStr: str = ''
        self.requestResource: str = ''

    def __not_document(self,strs):
        """递归查找请求的文件"""
        tempPath = STATICPATH['value'] + strs
        if os.path.exists(tempPath):
            rtn = _response(200, tempPath)
            self.connHost.send(rtn)
            return
        else:
            tempIndex = strs.find('/')
            if tempIndex == -1:
                raise FileNotFoundError()
            else:
                strs = strs[tempIndex + 1:]
                self.__not_document(strs)

    def run(self):
        try:
            self._handler_request()
        except:
            traceback.print_exc()
            raise BubblingException()

    def _handler_request(self):
        try:
            recvRequest = self.connHost.recv(10240).decode(CHARSET['charset'])
            if not recvRequest:
                self.__del__()
            recvRequest = urllib.parse.unquote(recvRequest)
            browserArgs = _browser(recvRequest)._broswer  # 用于分辨是不是浏览器,存的是浏览器的请求头信息
            if not (browserArgs and browserArgs['User-Agent']):
                self.__del__()
            for browserArg in browserArgs:
                _set_browser(browserArg,browserArgs[browserArg])
            _set_cookies(_browser(recvRequest)._cookie)
            handlerUrl = _RequestStrHandler(recvRequest)
            handlerUrl.run()
            self.requestStr = handlerUrl.requestStr
            self.requestUrl = handlerUrl.requestUrl
            self.requestResource = handlerUrl.requestResource
            if self.requestUrl == '/favicon.ico':
                self.__del__()
            elif self.requestResource != 'document':
                # 不是请求html文件的情况
                self.__not_document(self.requestStr)
            else:
                self.requestArg = handlerUrl.requestArg
                self.requestMethod = handlerUrl.requestMethod
                # 对整理分类好的路由进行处理
                _Url(self.requestUrl, self.requestArg, self.requestMethod,
                     self.connHost, self.connAddr,recvRequest).run()
                time.sleep(0.01)
            self.connHost.close()
        except:
            traceback.print_exc()
            self.__del__()

    def __del__(self):
        try:
            self.connHost.send(_response(500, SERVERERROR))
            self.connHost.close()
        except:
            pass
        print('子进程被销毁')