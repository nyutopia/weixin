def application(environ, start_response):
    start_response('200 ok', [('content-type', 'text/plain')])
    return ['Hello, SAE!']

#coding: UTF-8
import os

import sae
import web

from weixinInterface import WeixinInterface

urls=(
	'/weixin','WeixinInterface'

)

app_root=os.path.dirname(__file__)
templates_root = os.path.join(app_root,'templates')
render=web.templates.render(templates_root)

app=web.application(urls,globals()).wsgifunc()
application=sae.create_wsgi_app(app)
