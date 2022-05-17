import re


class RouterHandler(object):
    """
    处理请求路径的具体类
    """
    def __init__(self, recvRequest):
        self.recvRequest = recvRequest

    def handlerUrl(self):
        """从请求中分辨出请求路径和请求参数"""
        requestArgs: str = ''
        requestStr = re.match('(GET )(.*)( )', self.recvRequest).group(2)
        if '?' in requestStr and requestStr.count('?') == 1:
            request = requestStr.split('?')
            requestUrl = request[0]
            requestArgs = request[1]
        else:
            requestUrl = requestStr
        self.recvRequestArgs = requestArgs.split('&')
        self.requestUrlLst = requestUrl.split('/')
        return [self.requestUrlLst,self.recvRequestArgs]