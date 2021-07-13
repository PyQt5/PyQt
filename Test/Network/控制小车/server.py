#!/usr/bin/env python
# -*- coding: utf-8 -*-
import atexit
import logging

import cv2
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.options import options, define
from tornado.tcpserver import TCPServer

try:
    import RPi.GPIO as GPIO  # @UnusedImport @UnresolvedImport
except:
    pass

define("port", default=8888, help="TCP port to listen on")
logger = logging.getLogger(__name__)

# SIZE = (640, 480)  # 分辨率
# FPS = 24
SIZE = (100, 80)  # 分辨率
FPS = 5
PARAM = [int(cv2.IMWRITE_JPEG_QUALITY), FPS]


class EchoServer(TCPServer):
    IMAGE = None

    def __init__(self, cap, *args, **kwargs):
        super(EchoServer, self).__init__(*args, **kwargs)
        self.cap = cap
        self.init()

    def init(self):
        """初始化管脚"""
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(17, GPIO.OUT)
            GPIO.setup(27, GPIO.OUT)
            GPIO.setup(22, GPIO.OUT)
            GPIO.setup(18, GPIO.OUT, initial=False)
            self.duo = GPIO.PWM(18, 300)
            self.p1 = GPIO.PWM(17, 10000)
            self.p2 = GPIO.PWM(27, 10000)
            en = GPIO.output(22, False)  # @UnusedVariable
            self.p1.start(0)
            self.p2.start(0)
            self.duo.start(0)
        except Exception as e:
            print(e)

    def forward(self, a):
        try:
            k = a / 100
            print("k=%lf" % k)
            self.p1.ChangeDutyCycle(k)
            self.p2.ChangeDutyCycle(0)
        except:
            pass

    def back(self, a):
        try:
            k = a / 100
            print("k1=%lf" % k)
            self.p1.ChangeDutyCycle(0)
            self.p2.ChangeDutyCycle(k)
        except:
            pass

    def lr(self, a):
        try:
            self.duo.ChangeDutyCycle(a)  # 左满舵a=32，右满舵a=52，中值a=42，则a值取32至52
        except:
            pass

    def stop(self):
        try:
            self.p1.ChangeDutyCycle(0)
            self.p2.ChangeDutyCycle(0)
            self.duo.ChangeDutyCycle(42)
        except:
            pass

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
                    try:
                        ver, value = data.decode().split(':')
                        if ver == 'L':
                            self.lr(int(value))
                        elif ver == 'R':
                            self.lr(int(value))
                        elif ver == 'F':
                            self.forward(int(value))
                        elif ver == 'B':
                            self.back(int(value))
                        yield stream.write(data)
                    except:
                        yield stream.write(b'\n')
            except StreamClosedError:
                logger.warning("Lost client at host %s", address[0])
                break
            except Exception as e:
                print(e)


def start(cap):
    """启动服务器"""
    options.parse_command_line()
    server = EchoServer(cap)
    server.listen(options.port)
    logger.info("Listening on TCP port %d", options.port)
    IOLoop.current().start()


if __name__ == "__main__":
    cap = None
    try:
        cap = cv2.VideoCapture(0)  # 开启摄像头
        atexit.register(lambda: cap.release())
        atexit.register(lambda: GPIO.cleanup())
        start(cap)
    except Exception as e:
        print(e)
    if cap:
        cap.release()
    try:
        GPIO.cleanup()
    except:
        pass
