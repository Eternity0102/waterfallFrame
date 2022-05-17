from views import registerClass, LoginClass
from waterfall.HTTPServer.httpserver import HTTPServer
from waterfall import url

url(
    {
        '/register': registerClass,
        '/login':LoginClass,
    }
)

server = HTTPServer('0.0.0.0', 8888)
server.static_path = '../static/'
server.run()

