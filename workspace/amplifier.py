#coding:utf-8
#author:mrtang
#date:2020.1.7

from ads1299 import *
from esp32ap import *
import time
import usocket

class Amplifier():
    def __init__(self):
        self.ads = Ads1299()
        self.ads.init()
        self.ap = Esp32Ap('Esp32AdsPort8089','192.168.66.1')
        
        self.sock = usocket.socket(usocekt.AF_INET,uscoekt.SOCK_DGRAM)
        self.sock.bind(('192.168.66.1',8089))
        
    def run(self):
        while not self.ap.isconnected():
            time.sleep(0.1)
        # 通过udp进行通信
        # 上位机客户端绑定后，向esp32发送任何内容，即可启动esp32向上位机发送数据
        # 该操作的目的是让上位机向esp32暴露自己的地址
        _,self._addr = self.sock.recvfrom(128)  

        data = bytearray(0)
        disconnect_counter = 0
        while True:
            onedata = self.ads.get_data()
            if len(onedata)==0: continue
            data += onedata
            if self.ap.isconnected():
                disconnect_counter = 0
                self.sock.sendto(data,self.addr)
                data = bytearray(0)
            else:
                disconnect_counter += 1
                if disconnect_counter > 400:    # 断线超过20秒退出
                    break
            time.sleep(0.1)
            
def main():
    amp = Amplifier()
    while True:
        amp.run()
