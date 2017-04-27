# -*- coding:utf-8 -*-
from lxml import etree
import lxml
def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    xmlData = etree.fromstring(web_data)
    
    msg_type = xmlData.find('MsgType').text
    
    if msg_type=='text':
        
        return TextMsg(xmlData)
    elif msg_type == 'image':
        return ImageMsg(xmlData)
    elif mag_type = 'event':
        return EventMsg(xmlData)

class Msg(object):
    def __init__(self,xmlData):
        self.ToUserName=xmlData.find("ToUserName").text
        self.FromUserName=xmlData.find("FromUserName").text
        self.CreateTime=xmlData.find("CreateTime").text
        self.MsgType=xmlData.find("MsgType").text
        

class TextMsg(Msg):
    def __init__(self,xmlData):
        Msg.__init__(self,xmlData)
        self.MsgId=xmlData.find("MsgId").text
        self.Content=xmlData.find("Content").text.encode("utf-8")

class ImageMsg(Msg):
    def __init__(self,xmlData):
        Msg.__init__(self,xmlData)
        self.MsgId=xmlData.find("MsgId").text
        self.PicUrl=xmlData.find("PicUrl").text
        self.MediaId=xmlData.find("MediaId").text

class EventMsg(Msg):
    def __init__(self,xmlData):
        Msg.__init__(self,xmlData)
        self.Event=xmlData.find("Event").text
        