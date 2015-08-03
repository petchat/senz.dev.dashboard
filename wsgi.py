# coding: utf-8

import os

import leancloud
from wsgiref import simple_server

from app import app
from cloud import engine

from itsdangerous import Signer

APP_ID = os.environ['LC_APP_ID']
MASTER_KEY = os.environ['LC_APP_MASTER_KEY']
PORT = int(os.environ['LC_APP_PORT'])

signer = Signer(app.config['SECRET_KEY'])

leancloud.init(APP_ID, master_key=MASTER_KEY)

application = engine


if __name__ == '__main__':
    # 只在本地开发环境执行的代码
    app.debug = True
    server = simple_server.make_server('localhost', PORT, application)
    server.serve_forever()
