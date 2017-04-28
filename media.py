#-*- coding:utf-8 -*-
#filename:media.py
from basic import Basic
import urllib2
import os
import poster.encode
from poster.streaminghttp import register_openers

class Media(object):
    def __init__(self):
        register_openers()
    #上传图片
    def upload(self,accessToken,filePath,mediaType):
        openFile=open(filePath,"rb")
        param={"media":openFile}
        postData,postHeaders=poster.encode.multipart_encode(param)
 
        postUrl = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s"%(accessToken,mediaType)
        request=urllib2.Request(postUrl,postData,postHeaders)
        urlResp = urllib2.urlopen(request)
        print urlResp.read()
if __name__=='__main__':
    myMedia=Media()
    accessToken = Basic().get_access_token()
    root=os.path.dirname(__file__)
    filePath =os.path.join(root,'media/image/1.jpg')
    mediaType='image'
    myMedia.upload(accessToken,filePath,mediaType)

