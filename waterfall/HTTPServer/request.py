from waterfall import REQUEST, BROWSER, CHARSET, COOKIES
from waterfall.Htools.restools import _response_head


class Request():
    def __init__(self,requestMethod,connHost,connAddr,requestMessage,childGroup):
        self.__connHost = connHost
        self.__connAddr = connAddr
        self.__requestMethod = requestMethod
        self.__requestMessage = requestMessage
        self.paramenter = childGroup
        self.request = REQUEST
        self.browser = BROWSER
        self.cookies = COOKIES
        self.strs: str = ''
        for kw in self.request:
            exec('self.%s=self.request[kw]' % kw)

    def _set_option(self,**kwargs):
        for kw in kwargs:
            exec('self.%s=kwargs[kw]'%kw)
        rtnChild = self.__call_childMethod()
        if rtnChild is None:
            rtnChild = _response_head(200)+self.strs
        self.__connHost.send(rtnChild.encode(CHARSET['charset']))

    def __call_childMethod(self):
        child_method = getattr(self, self.__requestMethod.lower())
        return child_method()

    def write(self,strs):
        self.strs += strs+'\r\n'

    def get(self,*args,**kwargs):
        pass

    def post(self,*args,**kwargs):
        pass

    def head(self,*args,**kwargs):
        pass

    def put(self,*args,**kwargs):
        pass

    def delete(self,*args,**kwargs):
        pass

    def connect(self,*args,**kwargs):
        pass

    def options(self,*args,**kwargs):
        pass

    def trace(self,*args,**kwargs) :
        pass