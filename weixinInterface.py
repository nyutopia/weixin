# -*- coding:utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2
import json
from lxml import etree
import receive


def youdao(word):
        qword=urllib2.quote(word)
        #baseurl=r"https://fanyi.youdao.com/openapi.do?keyfrom=nyutopia&key=1909528419&type=data&doctype=json&version=1.1&q="
        baseurl=r"https://fanyi.youdao.com/openapi.do?keyfrom=nyannew&key=1896715416&type=data&doctype=json&version=1.1&q="
        url=baseurl+qword
        resp=urllib2.urlopen(url)
        fanyi=json.loads(resp.read())
        if fanyi['errorCode']==0:
            if 'basic' in fanyi.keys():
                trans=u"%s:\n%s\n%s\n网络释义:\n%s"%(fanyi['query']," ".join(fanyi['translation'])," ".join(fanyi['basic']['explains'])," ".join(fanyi['web'][0]['value']))
            else:
                trans=u'%s:\n基本翻译:%s\n'%(fanyi['query']," ".join(fanyi['translation']))
            return trans
        elif fanyi['errorCode']==20:
            return u'对不起，要翻译的文本过长'
        elif fanyi['errorCode']==30:
            return u'对不起，无法进行有效的翻译'
        elif fanyi['errorCode']==40:
            return u'对不起，不支持的语言类型'
        else:
            return u'对不起，您输入的单词%s无法进行翻译，请检查拼写'% word
        
class WeixinInterface:
    def __init__(self):
    	self.app_root=os.path.dirname(__file__)
        self.templates_root=os.path.join(self.app_root,'templates')
        self.render=web.template.render(self.templates_root)
        
    def GET(self):
        try:
        	#获取输入参数
            data=web.input()
            if len(data)==0:
                return "hello,this is WeixinInterface view"
            signature=data.signature
            timestamp=data.timestamp
            nonce=data.nonce
            echostr=data.echostr
        	#自己的token
            token="nyannew920919" #这里改写你在微信公众平台里输入的token
        
        	#字典序排序
            list=[token,timestamp,nonce]
            list.sort()
            sha1=hashlib.sha1()
            map(sha1.update,list)
            hashcode=sha1.hexdigest()
            #sha1加密算法  
            print "WeixinInterface/GET fuc:hashcode,signature:",hashcode,signature
            #如果是来自微信的请求，则回复echostr
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception,Argument:
            return Argument
   
    
    def POST(self):
#        str_xml=web.data() #获得post来的数据
#        print "str_xml is"+str_xml
#        xml = etree.fromstring(str_xml)#进行xml解析
#        content=xml.find("Content").text#获得用户所输入的内容
#        msgType=xml.find("MsgType").text
#        fromUser=xml.find("FromUserName").text
#        toUser=xml.find("ToUserName").text
#        if type(content).__name__=='unicode':
#            content=content.encode('UTF-8')
#        Nword = youdao(content)
#        #return self.render.reply_text(fromUser,toUser,int(time.time()),u"我现在还在开发中，还没有什么功能，您刚才说的是："+content)
#        return self.render.reply_text(fromUser,toUser,int(time.time()),Nword)
        try:
            str_xml=web.data()
            print "str_xml is: ",str_xml
            recMsg=receive.parse_xml(str_xml)
            
                
            if isinstance(recMsg,receive.Msg) and recMsg.MsgType == 'text':
               
                fromUser = recMsg.FromUserName
                toUser = recMsg.ToUserName
                content = recMsg.Content
                Nword=youdao(content)
                return self.render.reply_text(fromUser,toUser,int(time.time()),Nword)
            else:
                print "暂且不处理"
                return "success"
        except Exception,Argument:
            return Argument

