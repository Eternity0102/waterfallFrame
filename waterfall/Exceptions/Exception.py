class WaterFallVarsException(Exception):
    def __init__(self,errorInfo):
        super().__init__()
        self.errorInfo = errorInfo

    def __str__(self):
        return str(self.errorInfo)+'变量或模板参数出错'


class TagIsNotCloseExecption(Exception):
    def __init__(self,errorInfo):
        super().__init__()
        self.errorInfo = errorInfo

    def __str__(self):
        return str(self.errorInfo)+' 未结束的标签'


class BubblingException(Exception):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return '通知主线程异常'


class RepeatedReferenceException(Exception):
    def __init__(self, errorInfo):
        super().__init__()
        self.errorInfo = errorInfo

    def __str__(self):
        return str(self.errorInfo) + ' 标签或模板重复引用'


class TemplateNotFoundException(Exception):
    def __init__(self, errorInfo):
        super().__init__()
        self.errorInfo = errorInfo

    def __str__(self):
        return '找不到模板 ' + str(self.errorInfo)


class TagException(Exception):
    def __init__(self, errorInfo):
        super().__init__()
        self.errorInfo = errorInfo

    def __str__(self):
        return '未知的模板标签 ' + str(self.errorInfo)