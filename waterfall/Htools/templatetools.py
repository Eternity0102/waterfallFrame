import os.path
import re
import traceback
from copy import copy

from waterfall import STATICPATH
from waterfall.Exceptions.Exception import *


class BeTags(object):
    """整理系统关键标签"""

    def __init__(self, strs, fileName):
        self.strs = strs
        self.fileName = fileName

    def __del_sysTagContent(self):
        """删除系统标签中的内容"""
        pass

    def __raise_findErrTag(self, lst, endKeyword, Exception):
        """查找错误位置,找到直接报异常"""
        try:
            for err in range(0, len(lst), 2):
                if endKeyword not in lst[err] and endKeyword not in lst[err + 1]:
                    # 结束关键词不在第一个，并且不在第二个，说明第一个未结束
                    raise Exception(lst[err])
                elif endKeyword in lst[err]:
                    # 结束关键词在第一个，说明不成对
                    raise Exception(lst[err])
                else:
                    pass
        except IndexError:
            raise Exception(lst[-1])

    def __handler_Tag(self, startTag, endTag, reverse: bool):
        """用于获取标签的索引位置，{开始标签：结束标签}"""
        headIndex = self.strs.find(startTag)
        lenhead = len(startTag)
        footIndex = self.strs.find(endTag, headIndex + lenhead)
        lenfoot = len(endTag)
        # 以标签中内容为中心，分为三块，标签前的，标签中的，标签后的字符串
        tagBeforeStr = self.strs[:headIndex]
        tagMiddleStr = self.strs[headIndex + lenhead:footIndex]
        tagTailStr = self.strs[footIndex + lenfoot:]
        # 是否保留标签块中的内容
        if reverse:  # 如果保留块中内容
            pass
        else:  # 如果删除块中内容
            self.strs = tagBeforeStr + tagTailStr

    def __extends_relace(self, firstStrs, curStrs):
        firstStartEndTagLst = re.findall(r'{%\s*block\s+?\S+\s*?%}|{%\s*?end\s+?block\s*?%}',
                                         firstStrs)  # 匹配最前面一页开始结束所有block标签
        if not firstStartEndTagLst:  # 如果没有开始结束block标签，则这一层不需要做任何处理了
            return firstStrs
        elif len(firstStartEndTagLst) % 2:  # 如果匹配不成对，则一定有一个错
            self.__raise_findErrTag(firstStartEndTagLst, 'end', TagIsNotCloseExecption)
        else:
            for curous in range(0, len(firstStartEndTagLst), 2):
                curTagName = re.findall('{%\s*?block\s+?(\S+?)\s*?%}', firstStartEndTagLst[curous])[0]  # 把当前游标文件名block名字匹配出来
                reg = "{%\s*?block\s+?" + curTagName + "\s*?%}"
                curStartTag = re.findall(reg, curStrs)  # 根据名字匹配当前文件开始标签
                curEndTag = re.findall('{%\s*?end\s*?block\s*?%}', curStrs)  # 根据名字匹配当前文件结束标签
                if not curStartTag:  # 在当前文件中匹配不到父文件的开始标签，说明没有被继承，删除即可
                    firstTempStr = re.findall(
                        firstStartEndTagLst[curous] + '\s*?[\r\n]*?[\s\S]*?\s*?[\r\n]*?' + firstStartEndTagLst[
                            curous + 1], firstStrs)[0]  # 获取最顶层模板标签中的字符串
                    firstStrs = firstStrs.replace(firstTempStr, '')  # 将这一层的字符串替换为上一层的字符串
                    continue
                if not curStartTag and not curEndTag:
                    continue
                elif curEndTag and not curStartTag:
                    raise TagIsNotCloseExecption(firstStartEndTagLst[curous])
                else:  # 如果最底层的标签，出现在上一层，说明被继承了
                    try:
                        firstTempStr = re.findall(firstStartEndTagLst[curous] + '\s*?[\r\n]*?[\s\S]*?\s*?[\r\n]*?' +firstStartEndTagLst[curous + 1], firstStrs)[0]  # 获取最顶层模板标签中的字符串
                        curTempStr = re.findall(curStartTag[0] + '([\s\S]*?)' + curEndTag[0], curStrs)[0]  # 获取当前文件标签中的字符串
                        firstStrs = firstStrs.replace(firstTempStr, curTempStr)  # 将这一层的字符串替换为上一层的字符串
                    except IndexError:
                        continue
            return firstStrs

    def __del_finalTagExists(self, reg):
        """如果处理完成后标签依然存在，则不保留标签，直接从self.strs中删除"""
        results = re.findall(reg, self.strs)
        if len(results) % 2:
            self.__raise_findErrTag(results, 'end', TagIsNotCloseExecption)
        for result in results:
            self.strs = self.strs.replace(result, '')

    def __handler_declareExtendsTag(self, preStrs, curFileName):
        """用于递归处理注释标签{% extends %}"""
        try:
            with open(STATICPATH['value'] + curFileName, 'r') as f:
                curStrs = f.read()  # 读取当前的文件字符
        except FileNotFoundError:
            raise TemplateNotFoundException(curFileName)
        curTag = re.findall(r'\s*{%\s*extends\s+?\S+\s*?%}\s*', curStrs[:preStrs.find('\n')])  # 匹配首行是否有继承模板申明
        if curTag:  # 如果头部有继承标签，则查找相关文件
            nextFileName = re.findall(r'extends\s+(\S+?)\s*?%}', curTag[0])[0]
            if nextFileName == curFileName:
                raise RepeatedReferenceException(curTag[0])
            firstStrs = self.__handler_declareExtendsTag(curStrs, nextFileName)  # 找到最深层次，然后开始找block语句块
            firstStrs = self.__extends_relace(firstStrs, preStrs)
            return firstStrs
        else:  # 如果头部没有继承标签，就不需要再查找,处理当前文件
            return self.__extends_relace(curStrs, preStrs)

    def __handler_builtNotesTag(self):
        """用于处理注释标签{% notes %},"""
        notes = re.findall('{%\s*?notes\s*?%}', self.strs)
        if notes and not len(notes) % 2:  # 如果文件中有注释,并且都是注释成对出现
            for i in range(0, len(notes), 2):
                self.__handler_Tag(notes[i], notes[i + 1], False)
        elif notes:  # 如果文件中有注释，但不是双数
            raise TagIsNotCloseExecption(notes[-1])
        else:  # 直接未匹配到
            pass

    def run(self):
        self.strs = self.__handler_declareExtendsTag(self.strs, self.fileName)  # 处理extends标签，最先处理
        self.__del_finalTagExists('{%\s*block\s+?\S+\s*?%}|{%\s*?end\s+?block\s*?%}')
        self.__handler_builtNotesTag()  # 处理模板内建标签,目前只有注释标签，其次处理
        return self.strs


class BeSyntaxs(object):
    """整理语句,if/for"""

    def __init__(self, strs, **kwargs):
        self.__lst = [0, 0, 0, 0]
        self.__ifLst: list = []
        self.__elIfLst: list = []
        self.__endIfLst: list = []
        self.__record: list = []
        self.strs = strs
        self.kwargs = kwargs

    def __distinguish_tag(self, tag):
        """识别传入的标签是开始标签还是结束标签"""
        if re.findall('{%\s*?if\s+?.+?\s*?%}', tag):
            self.__lst[0] = 1
        elif re.findall('{%\s*?end\s*?if\s*?%}', tag):
            self.__lst[1] = 1
        elif re.findall('{%\s*?for\s+?\S+?\s+?in\s+?\S+?\s*?%}', tag):
            self.__lst[2] = 1
        elif re.findall('{%\s*?end\s*?for\s*?%}', tag):
            self.__lst[3] = 1
        else:
            raise TagException(tag)

    def __find_errKey(self, lst, cursor):
        """找出错误的值，传入进来的lst一定是一个长度为单数的"""
        if cursor < len(lst):
            self.__distinguish_tag(lst[cursor])
            if self.__lst.index(1) in [1, 3]:  # 如果对应游标位置是结束标签，就应该回溯一次看看是否前面有匹配
                raise TagIsNotCloseExecption(lst[cursor-1])
            try:
                self.__distinguish_tag(lst[cursor + 1])
            except IndexError:
                # 最后一个标签匹配不上才会运行到此
                return lst[cursor]
            if self.__lst.count(1) == 1:
                return self.__find_errKey(lst, cursor + 1)
            else:
                beforeIndex = self.__lst.index(1)
                self.__lst[beforeIndex] = 0
                afterIndex = self.__lst.index(1)
                self.__lst[afterIndex] = 0
                sub = afterIndex - beforeIndex
                if afterIndex != 2 and sub == 1:  # 避免索引是1和2的情况，只考虑0和1，2和3
                    # 刚好是开始结束标签的时候,将这两个元素移除
                    lst.remove(lst[cursor])
                    lst.remove(lst[cursor])
                    if cursor != 0:
                        cursor -= 1
                    return self.__find_errKey(lst, cursor)  # 继续查找元素
                else:
                    # 比对下一个标签
                    return self.__find_errKey(lst, cursor + 1)
        else:
            # 传入的是单数，不可能什么都匹配不到,只能返回一个空列表
            return lst

    def __handler_forTag(self,startTag,endTag):
        """通过for循环遍历拼接for里面的内容"""
        for kw in self.kwargs:
             exec('%s=self.kwargs[kw]'%kw)
        matchTag = startTag  # 只能用来匹配，防止改变startTag
        if '(' in startTag and ')' in startTag:
            matchTag = matchTag.replace('(','\(')
            matchTag = matchTag.replace(')','\)')
        reg = r'%s' % (matchTag + '[\s\S]*?' + endTag + '\s*?[\r\n]*?' )
        labelToLable = re.findall(reg, self.strs)[0]
        reg = r'%s' % (matchTag + '([\s\S]*?)' + endTag)
        inLabel = re.findall(reg,self.strs)[0]
        try:
            vars = re.findall('{%\s*?for\s+?(\w+)\s+?in\s*?(.+?)\s*?%}', startTag)
            iter = vars[0][0]  # for后面的值
            sequence = vars[0][1]  # in后面的值
        except:
            traceback.print_exc()
            raise TagException(startTag)
        tempInLabel = ''
        for varTag in eval('%s'%sequence):  # 每一次循环替换的值都不一样，所以先循环,看做模板里面的循环
            changeLabel = inLabel
            varInFor = re.findall('{{\s*?\S+?\s*?}}', inLabel)
            # 在for循环中的循环变量,标签不能嵌套,匹配出来的不可能为空
            varInFor = set(varInFor) #去掉重复值
            for var in varInFor:
                try:
                    inVar = re.findall('{{(.*?\W*?)(%s)(\W*?.*?)}}'%iter,var)[0]  # 从括号中提取出循环变量
                except:
                    continue
                repTag = inVar[0] + 'varTag' + inVar[2]
                newVar = eval(repTag)
                inLabels = re.findall('{%\s*?(.+?)\s*?%}',changeLabel)
                for label in inLabels:
                    varIn = '{{' + inVar[0] + inVar[1] + inVar[2] + '}}'
                    if varIn in label:
                        changeLabel = changeLabel.replace(label, label.replace(varIn,'"' + str(newVar) + '"'))
                changeLabel = changeLabel.replace(var,str(newVar))
            tempInLabel += changeLabel
        self.strs = self.strs.replace(labelToLable,tempInLabel)

    def __reg_brackets(self,tag):
        newtag = tag
        if '(' in newtag and ')' in newtag:
            newtag = tag.replace('(', '\(')
            newtag = newtag.replace(')', '\)')
        return newtag

    def __select_condition(self,elIfLst,index):
        try:
            return re.findall('{%\s*?(if|elif)+?\s+?(.+?)\s*?%}', elIfLst[index])[0][1]
        except:
            try:
                re.findall('{%\s*?else\s*?%}', elIfLst[index])
                return ''
            except:
                traceback.print_exc()
                raise TagException(elIfLst[index])

    def __handler_ifTag(self,startTag,elIfLst,endTag):
        """通过for循环遍历拼接for里面的内容"""
        for kw in self.kwargs:
            exec('%s=self.kwargs[kw]'%kw)
        elIfLst.insert(0,startTag)
        elIfLst.append(endTag)
        reg = r'(%s)' % ( elIfLst[0] + '[\s\S]*?' + endTag + '\s*?[\r\n]*?' )
        firstToLast = re.findall(reg, self.strs)[0]  # 先匹配出整个代码块内容
        for index in range(len(elIfLst)):
            curTag = self.__reg_brackets(elIfLst[index])  # 只能用来匹配，防止改变startTag
            condition = self.__select_condition(elIfLst,index)
            if condition:  # 判断是否有条件，如果有条件，则是if或elif，没有则是else
                if eval(condition):  # 如果模板中的条件成立
                    nextTag = self.__reg_brackets(elIfLst[index+1])
                    inLabel = re.findall(curTag + '\s*?[\r\n]+?([\s\S]*?)\s*?[\r\n]+?\s*?' + nextTag, self.strs)[0]
                    self.strs = self.strs.replace(firstToLast,inLabel)
                    break
            else:
                if curTag != endTag:  # 则是else标签
                    inLabel = re.findall(curTag + '\s*?[\r\n]+?([\s\S]*?)\s*?[\r\n]+?\s*?' + endTag, self.strs)[0]
                    self.strs = self.strs.replace(firstToLast,inLabel)
                else:  # 则是endif标签
                    self.strs = self.strs.replace(firstToLast,'')
                break

    def __find_ifTag(self,tagLst,cursor):
        """通过正则索引等方式递归找到最深度一组if或for标签，直到遇到endfor就交给另外一个函数执行"""
        if cursor < len(tagLst):
            tag = re.findall('{%\s*?if\s+?.+?\s*?%}', tagLst[cursor])
            if not tag:
                tag = re.findall('{%\s*?elif\s+?.+?\s*?%}|{%\s*?else\s*?%}', tagLst[cursor])
                if not tag:
                        self.__handler_ifTag(tagLst[self.__ifLst[0]], self.__elIfLst, tagLst[cursor])
                else:
                    self.__elIfLst.append(tagLst[cursor])
                    return self.__find_ifTag(tagLst, cursor + 1)
            else:
                self.__ifLst.insert(0,cursor)
                return self.__find_ifTag(tagLst, cursor + 1)
            del tagLst[self.__ifLst[0]:cursor+1]
            cursor = self.__ifLst[0]
            del self.__ifLst[0]
            self.__elIfLst = []
            self.__find_ifTag(tagLst, cursor)
        else:
            return

    def __find_forTag(self,tagLst,cursor,startRegex,endRegex,runFunc):
        """通过正则索引等方式递归找到最深度一组if或for标签，直到遇到endfor就交给另外一个函数执行"""
        if cursor < len(tagLst):
            startTag = re.match(startRegex, tagLst[cursor])
            if startTag:  # 列表中循环如果不是for，就匹配是不是endfor,是则向下执行，不是则else
                self.__record.insert(0, cursor)  # 在最前面插入是for的游标，记录过了几个for才遇到end
                return self.__find_forTag(tagLst, cursor + 1,startRegex,endRegex,runFunc)
            else:
                endTag = re.match(endRegex, tagLst[cursor])
                if endTag:
                    # 如果forend标签，就将其相应的内容交给另外一个函数执行，并且弹出相应的元素
                    try:
                        runFunc(tagLst[self.__record[0]],tagLst[cursor])  # 提交到这个方法处理
                    except:
                        raise TagException(tagLst[self.__record[0]])
                    tagLst.pop(cursor)  # 先弹出后一个元素，再弹出前面，防止游标对应的值发生变化
                    tagLst.pop(self.__record[0])
                    if not self.__record:  # 如果cursor里面有值，说明后面还有endfor，游标则不动
                        cursor = self.__record[0]
                    del self.__record[0]
                    return self.__find_forTag(tagLst, cursor - 1,startRegex,endRegex,runFunc)
                else:
                    return self.__find_forTag(tagLst, cursor + 1,startRegex,endRegex,runFunc)
        else:
            return


    def __handler_syntax(self):
        reg = '{%\s*?if\s+?.+?\s*?%}|{%\s*?for\s+?\S+?\s+?in\s+?\S+?\s*?%}|{%\s*?end\s*?if\s*?%}|{%\s*?end\s*?for\s*?%}'
        tagLst = re.findall(reg, self.strs)  # 先在外层匹配一次，如果内容里面有标签再去排错
        if tagLst:
            result = self.__find_errKey(copy(tagLst),0)  # 检查标签状态，如果没有值，则说明正常
            if result:
                raise TagIsNotCloseExecption(result)
            startRegex = '{%\s*?for\s+?(\S+?)\s+?in\s+?(\S+?)\s*?%}'
            endRegex = '{%\s*?end\s*?for\s*?%}'
            runFunc = self.__handler_forTag
            self.__find_forTag(tagLst,0,startRegex,endRegex,runFunc)  # 处理其中的for循环
            reg = '{%\s*?if\s+?.+?\s*?%}|{%\s*?elif\s+?.+?\s*?%}|{%\s*?else\s*?%}|{%\s*?end\s*?if\s*?%}'
            tagLst = re.findall(reg,self.strs)
            if tagLst:
                self.__find_ifTag(tagLst, 0)

    def run(self):
        self.__handler_syntax()
        return self.strs


class BeVars(object):
    """整理模板中的变量"""

    def __init__(self, strs,**kwargs):
        self.strs = strs
        self.kwargs = kwargs

    def __handler_vars(self):
        """处理模板变量"""
        print('self.kwargs', self.kwargs)
        for kw in self.kwargs:
            exec('%s = self.kwargs[kw]' % (kw))
        vars = re.findall('{{\s*?\S+?\s*?}}', self.strs)
        for var in vars:
            try:
                self.strs = self.strs.replace(var, str(eval('%s' % re.findall('\w+', var)[0])))
            except AttributeError:
                traceback.print_exc()

    def run(self):
        self.__handler_vars()
        return self.strs
