import os
import sys
import traceback
from waterfall import _set_static, _set_charset
from socket import socket,AF_INET,SOL_SOCKET,SOCK_STREAM,SO_REUSEADDR
from waterfall.Htools.httpprocess import _HandlerRequestThread


class HTTPServer(object):
    """启动服务的具体类,用于建立连接后的收发任务交给HandlerRequest类执行"""

    def __init__(self, ip, port,charset='utf-8'):
        sys.path.append(os.getcwd())
        self.sockfd = socket(family=AF_INET, type=SOCK_STREAM)
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sockfd.bind((ip, int(port)))
        self.sockfd.listen(8)
        self.ip = ip
        self.port = int(port)
        self.static_path: str = '/'
        _set_charset(charset)

    def __del__(self):
        self.sockfd.close()

    def __start_server(self):
        """启动服务，创建对应的链接，启动一个线程处理连接请求"""
        while True:
            try:
                connHost, connAddr = self.sockfd.accept()
                connthread = _HandlerRequestThread(connHost, connAddr)
                connthread.setDaemon(True)
                connthread.start()
            except:
                traceback.print_exc()

    def run(self):
        if self.static_path[-1] != '/':
            self.static_path += '/'
        _set_static(self.static_path)
        self.__start_server()
