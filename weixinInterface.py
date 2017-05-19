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
import random
import pylibmc


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
     
    
def xiaohuangji(ask):
    ask = ask.encode('UTF-8')
    enask = urllib2.quote(ask)
    send_headers = {
    'Cookie':'Filtering=0.0; Filtering=0.0; isFirst=1; isFirst=1; simsimi_uid=50840753; simsimi_uid=50840753; teach_btn_url=talk; teach_btn_url=talk; sid=s%3AzwUdofEDCGbrhxyE0sxhKEkF.1wDJhD%2BASBfDiZdvI%2F16VvgTJO7xJb3ZZYT8yLIHVxw; selected_nc=zh; selected_nc=zh; menuType=web; menuType=web; __utma=119922954.2139724797.1396516513.1396516513.1396703679.3; __utmc=119922954; __utmz=119922954.1396516513.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
    }
    baseurl = r'http://www.simsimi.com/func/reqN?lc=zh&ft=0.0&req='
    url = baseurl + enask
    req = urllib2.Request(url,headers=send_headers)
    resp = urllib2.urlopen(req)
    reson = json.loads(resp.read())
    return reson
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
            mc=pylibmc.Client()
                
            if isinstance(recMsg,receive.Msg):
                fromUser = recMsg.FromUserName
                toUser = recMsg.ToUserName
                if recMsg.MsgType == "text":
                    content = recMsg.Content
                    if content.lower() == 'help':
                        replyText=u"1.输入中文或者英文返回对应的英中翻译\n2.输入m随机来首音乐听，建议在WiFi下听"
                        return self.render.reply_text(fromUser,toUser,int(time.time()),replyText)
                    if content.lower() == 'bye':
                        mc.delete(fromUser+'_xhj')
                        return self.render.reply_text(fromUser,toUser,int(time.time()),u"您已经退出了和小黄鸡的交谈中，请输入help来显示操作指令")
                    if content.lower() == 'xhj':
                        mc.set(fromUser+'_xhj','xhj')
                        return self.render.reply_text(fromUser,toUser,int(time.time()),u"您已经进入和小黄鸡的交谈中，输入bye来跳出与他的交谈")
                    
                    mcxhj = mc.get(fromUser+'_xhj')
                    if(mcxhj == 'xhj'):
                        res = xiaohuangji(content)
                        reply_text = res['sentence_resp']
                        if u'微信' in reply_text:
                            reply_text = u"小黄鸡脑袋出问题了，请换个问题"
                        return self.render.reply_text(fromUser,toUser,int(time.time()),reply_text)
                    
#                    if content == 'm':
#                        
#                        musicList = [
#                                       [r'http://bcs.duapp.com/yangyanxingblog3/music/destiny.mp3','Destiny',u'献给我的宝贝晶晶'],
#                                       [r'http://bcs.duapp.com/yangyanxingblog3/music/5days.mp3','5 Days',u'献给我的宝贝晶晶']
#                                ]
#                        music = random.choice(musicList)
#                        musicTitle = music[1]
#                        musicURL = music[0]
#                        
#                        return self.render.replpy_music(fromUser,toUser,int(time.time()),musicTitle,"你好",musicURL)
                    if type(content).__name__ == 'unicode':
        				content = content.encode('UTF-8'）
                    Nword=youdao(content)
                    return self.render.reply_text(fromUser,toUser,int(time.time()),Nword)
                elif recMsg.MsgType == "image":
                    mediaId = recMsg.MediaId
                    return self.render.reply_image(fromUser,toUser,int(time.time()),mediaId)
                elif recMsg.MsgType == 'event':
                    if recMsg.Event == "subscribe":
                        content = u"欢迎关注本订阅号，这个订阅号是本人业余爱好所建立,输入help查看功能，目前功能还在完善中"
                        return self.render.reply_text(fromUser,toUser,int(time.time()),content)
                else:
                    return "success"
            else:
                print "暂且不处理"
                return "success"
        except Exception,Argument:
            return Argument

