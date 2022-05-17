import re
import traceback
from waterfall import CHARSET
from waterfall.Htools.restools import _response_head


def _response(StautsCode, filePath):
    with open(filePath, 'rb') as f:
        content = f.read()
        response = _response_head(StautsCode).encode(CHARSET['charset'])
        response += content
    return response


class _RequestStrHandler(object):
    """
    处理请求路径的具体类
    """
    def __init__(self, recvRequest):
        self.recvRequest = recvRequest  # 请求的所有内容
        self.requestArg: list = []
        self.requestUrl: list = []
        self.requestMethod: str = ''
        self.requestStr: str = ''
        self.requestResource: str = ''
        try:
            self.requestMethod = re.match('[A-Z]+[^ ]', recvRequest).group()
            self.requestStr = re.match('([A-Z]+ )(.*)( )', self.recvRequest).group(2)
            self.requestResource = re.findall('Sec-Fetch-Dest: (\S+)', self.recvRequest)[0]
        except:
            print('请求内容匹配异常')
            traceback.print_exc()

    def _handler_url(self):
        """从请求中分辨出请求路径和请求参数"""
        print('匹配的请求路径为:', self.requestStr)
        if self.requestStr == '/':
            self.requestUrl: str = '/'
        elif '?' in self.requestStr and self.requestStr.count('?') == 1:
            request = self.requestStr.split('?')
            self.requestUrl = request[0]
            self.requestArg = request[1]
        else:
            self.requestUrl = self.requestStr

    def run(self):
        self._handler_url()