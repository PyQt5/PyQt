#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import cv2
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.options import options, define
from tornado.tcpserver import TCPServer


# Created on 2018年4月18日
# author: Irony
# site: https://github.com/892768447
# email: 892768447@qq.com
# file: 控制小车.server
# description:
__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


define("port", default=8899, help="TCP port to listen on")
logger = logging.getLogger(__name__)

SIZE = (640, 480)  # 分辨率
FPS = 24
PARAM = [int(cv2.IMWRITE_JPEG_QUALITY), FPS]


class EchoServer(TCPServer):

    IMAGE = None

    def __init__(self, *args, **kwargs):
        super(EchoServer, self).__init__(*args, **kwargs)
        try:
            self.cap = cv2.VideoCapture(0)
        except Exception as e:
            print(e)

    @gen.coroutine
    def handle_stream(self, stream, address):
        while True:
            try:
                data = yield stream.read_until(b"\n")
#                 logger.info("Received bytes: %s", data)
                if not data.endswith(b"\n"):
                    data = data + b"\n"
                if data == b'getimage\n' and self.cap and self.cap.isOpened():
                    _, frame = self.cap.read()  # 读取一帧图片
                    if str(type(frame)).find('ndarray') > -1:
                        frame = cv2.resize(frame, SIZE)
                        ret, data = cv2.imencode('.jpg', frame, PARAM)
                        if ret:
                            yield stream.write(data.tostring())  # 发送图片
                else:
                    yield stream.write(b'\n')
            except StreamClosedError:
                logger.warning("Lost client at host %s", address[0])
                break
            except Exception as e:
                print(e)


if __name__ == "__main__":
    options.parse_command_line()
    server = EchoServer()
    server.listen(options.port)
    logger.info("Listening on TCP port %d", options.port)
    IOLoop.current().start()
