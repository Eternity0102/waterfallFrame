import re


def _redirect_headers(url):
    response = "HTTP/1.1 302 OK\r\n"
    response += 'Content-Type:textml\r\n'
    response += 'Location:%s\r\n'%url
    response += '\r\n'
    return response


def _response_head(statusCode,cookies='',sessions='',statement=''):
    header = "HTTP/1.1 %s %s\r\n" % (statusCode,statement)
    if cookies:
        header += cookies
    # if sessions:
    #     header += 'Set-Session:{}\r\n'.format(sessions)
    header += '\r\n'
    return header


def __http_response(strs):
    string = '''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
    </head>
    <body></body>
    </html>'''
    string = string.replace('<body></body>','<body>\n'+strs+'\n</body>')
    return string


class _browser(object):
    """用于分辨并且处理浏览器的请求参数"""

    def __init__(self, strs):
        self.strs = strs
        self._broswer: dict = {}
        self._cookie: dict = {}
        self.__run()

    def __search_with(self):
        values = re.findall('(.+?): ([\s\S]+?)[\n\r\n]', self.strs)
        for sets in values:
            self._broswer[sets[0]] = sets[1]
        if 'Cookie' in self._broswer:
            keys = self._broswer['Cookie'].split('; ')
            for i in keys:
                kv = i.split('=')
                self._cookie[kv[0]] = kv[1]


    def __run(self):
        self.__search_with()
