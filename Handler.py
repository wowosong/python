import re
from util import  *
class HTMLRenderer:
    def start_paragraph(self):
        print '<p>'

    def end_paragraph(self):
        print '</p>'

    def sub_emphasis(self,match):
        return '<em>%s</em>'%match.group(1)
    def feed(self,data):
        print  data
    def callback(self,prefix,name,*args):
        method=getattr(self,prefix+name,None)
        if callable(method):return  method(*args)
    def start(self,name):
        self.callback('start_',name)
    def end(self,name):
        self.callback('end_',name)
    def sub(self,name):
        def substitution(match):
            result=self.callback('sub_',name,match)
            if result is None:result=match.group(1)
            return result
        return substitution
class Rule:
    def action(self,block,handler):
        handler.start(self.type)
        handler.feedback(block)
        handler.end(self.type)
        return  True
class Parser:
    """
    A Parser reads a text file.applying rules and controlling a handler.
    """
    def __init__(self,handler):
        self.handler=handler
        self.rules=[]
        self.filters=[]
    def addRule(self,rule):
        self.rules.append(rule)
    def addFilter(self,pattern,name):
        def filter(block,handler):
            return  re.sub(pattern,handler.sub(name),block)
        self.filters.append(filter)
    def parse(self,file):
        self.handler.start('document')
        for block in blocks(file):
            for filter in self.filters:
                block=filter(block,self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    last=rule.action(block,self.handler)
                    if last:break
        self.handler.end('document')
class HeadingRule(Rule):
    type='heading'
    def condition(self,block):
        return  not '\n' in block and len(block)<=70 and not block[-1]==':'
class TitleRule(HeadingRule):
    type='title'
    first=True
    def  condition(self,block):
        if not self.first:return  False
        self.first=False
        return HeadingRule.condition(self,block)
class ListItemRule(Rule):
    type='listitem'
    def condition(self,block):
        return  block[0]=='-'
    def action(self,block,handler):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return  True

class ListRule(ListItemRule):
    type='list'
    inside=False
    def condition(self,block):
        return  True
    def action(self,block,handler):
        if not self.inside and ListItemRule.condition(self,block):
            handler.start(self.type)
            self.inside=True
        elif self.inside and not ListItemRule.condition(self,block):
            handler.end(self.type)
            self.inside=False
        return False
class ParagraphRule(Rule):
    type='paragraph'
    def condtion(self,block):
        return  True

