# waterfall框架

框架编写说明

本框架基于python socket TCP通信，写法如Django和Tornado，目前功能还未完善，当前实现的功能可供学习参考测试。本框架设计模式为TVC(Templates、views,Controller)，实现Templates运用了大量正则，效率较低，所有内部代码都在waterfall包下

版权说明©

未经作者同意，不可对项目中的内容下载自编自改，仅供学习测试



## 1.Controller层

### 1.服务相关

1.启动服务

```python
from waterfall.HTTPServer.httpserver import HTTPServer
server = HTTPServer('0.0.0.0', 8888,'utf-8') #默认是utf-8
server.run()
```

2.设置路由

```python
from waterfall import url
url(
    {
        #路由正则表达式:处理类,
        '/register': registerClass,
        '/login':LoginClass,
    }
)
```

3.指定静态文件路径

```python
server.static_path = '../static/' #指定的静态路径必须要在启动服务之前
```

### 2.处理类相关

1.处理路由类的继承

所有的处理类必须继承自Request，不可重写Request类的初始化方法

```python
from waterfall.HTTPServer.request import Request
class registerClass(Request):
```

2.继承类中可重写方法

所有请求类型(POST,GET,DELETE......)对应的方法都可以被重写，方法名均为请求类型对应的小写

```python
from waterfall.HTTPServer.request import Request
class registerClass(Request):
    def get(self,*args,**kwargs):
        ......
    def post(self,*args,**kwargs):
        ......
```

3.继承方法中的返回内容

1. 可用render返回想要返回的模板文件，render可以任意传入关键字参数给中的变量使用
2. 可用HTTPResponse返回想要返回的字符串

```python
from waterfall.HTTPServer.response import render
class registerClass(Request):
    def get(self,*args,**kwargs):
        return render('register.html',name='test',age='22')
    def post(self,*args,**kwargs):
        return HTTPResponse('请求成功')
```

4.可重定向网页

无需进行导入，访问方法在继承类父类中

```python
from waterfall.HTTPServer.response import render
class registerClass(Request):
    def post(self,*args,**kwargs):
        return self.redirect('/index')
```

5.设置网页cookie值

设置cookie可以连续设置

```python
from waterfall.HTTPServer.response import render
class registerClass(Request):
    def post(self,*args,**kwargs):
        set_cookie('sickname',nickname)
        set_cookie('token',ltoken)
        return self.redirect('/index')
```

6.向缓冲区写入字符

当处理类运行结束后才能将缓冲区的字符发送到前端，无需进行导入，访问方法在继承类父类中，在没有返回值的情况下会返回self.write写入的内容

```python
from waterfall.HTTPServer.response import render
class registerClass(Request):
    def post(self,*args,**kwargs):
        set_cookie('sickname',nickname)
        set_cookie('token',ltoken)
```

7.访问请求中的参数

访问中的参数:http://loclhost:8888?nickname=test&age=22

```python
from waterfall.HTTPServer.response import render
class registerClass(Request):
    def post(self,*args,**kwargs):
		print('浏览器提交的键值对:', self.paramenter)
        return ......
```

8.浏览器提交的参数

访问后浏览器提交的所有值，包括User-Agent,是一个字典，在访问的时候，所有的“-”都变成了“_”，大写都变成小写，例如User-Agent,访问时应该用：self.browser[user_agent]

```python
from waterfall.HTTPServer.response import render
class registerClass(Request):
    def post(self,*args,**kwargs):
		print('浏览器提交的所有值:', self.browser)
        return ......
```



## 2.模板层

1.模板中的注释

```
{% notes %}
这是注释掉的内容
{% notes %}
```

2.模板中的块

块主要是用于模板的继承，可在代码中任意位置插入标签，命名只能是字母数字和下划线

```
<body>
父文件第一行
{%block 命名 %}
父文件第二行
{% end block%}
父文件最后一行
</body>
```

3.模板中的继承

需要在模板首行声明继承自哪个文件，例如有两个文件father.html和child.html

```
{%extends father.html %}  <!--文件名不能加引号-->
<!DOCTYPE html>
....
```

4.在继承中使用块

只要在父文件前面声明继承，在子文件相同的block名称就会把父元素中的其他内容继承过来，唯独block中的内容会被替换掉

```
{%extends father.html %}  <!--文件名不能加引号-->
{%block 命名 %}
父文件的第二行被我替换了
{% end block%}
```

6.模板中的变量

在模板中，如果使用了变量，必须用“{{}}”括起来，这对括号不能嵌套，如果非要写成{{{{name}}}}样式，那么需要写成{{ {{name}} }}，变量的值需要用render函数的关键字传参方法传入参数

```python
<input type='text' value="{{name}}">
```

```python
render('index.html',name='cc')
```

7.模板中的if-elif-else语句

语法和python相同，不需要加引号，在if语句中，涉及变量不需要加{{   }}，但是变量依然需要从render中传入

```
......
{% if name == "cc" %}
	<p>这是name的值{{name}}</p>
{% elif name == "bb" %}
	<p>这是name的值{{name}}</p>
{% elif name == "aa"%}
	<p>这是name的值{{name}}</p>
{% end if %}
......
```

8.模板中的for语句

语法与python相同，用法与，所有变量都需要用render中传入，但是在循环遍历中，涉及到循环变量i，一定要加{{}},只是在定义for循环语句不用加{{}}

```
<table>
	{% for i in range(20)%}
		<tr>
			<td>输入第{{i}}行内容</td>
		</tr>
	{%end for%}
</table>
```

或

```
<table>
	{% for i in range(20)%}
		<tr>
			<td>输入第{{i}}行内容</td>
		</tr>
	{% end for%}
</table>
```





## 3.结语

大致内容应该就这些，可能小部分细节没写到此处，这段时间还没能把它完善好，暂时就放在github上，等以后有时间了，再拿出来给它完善一下