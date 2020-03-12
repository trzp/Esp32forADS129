#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 19:11
# @Version : 1.0
# @File    : sync_sock.py
# @Author  : Jingsheng Tang
# @Version : 1.0
# @Contact : mrtang@nudt.edu.cn   mrtang_cs@163.com
# @License : (C) All Rights Reserved


try:
    import esp 
except:
    raise Exception('The script is suitable for micropython on ESP32/8266 platform')


import socket
import struct
import utime
import math


# 经过测试，esp32上浮点运算精度有限，因此，尽量避免在其上进行运算

# window,linux系统时间戳的起始时间为1970-1-1 00:00:00
# 在esp32嵌入式系统中，起始时间为2000-1-1 00:00:00
# 1970年-2000年之间的秒差为 946656000
TIMOFFSET = 946656000.0


def getclk():
    return utime.ticks_us()/1000000.

# esp32一般来说不作为服务器

# class LNPTServer():
#     def __init__(self,addr):
#         lt = time.time()
#         gt = getclk()
#         self.clk_time_offset = lt - gt
#
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.myip = addr[0]
#         self.sock.bind(addr)
#         self.sock.listen(128)
#
#         print('[LNTP] service start!')
#
#     def start(self):
#         while True:
#             self.client, addr = self.sock.accept()
#             print('[LNTP] synchronize network time with: %s-%i'%addr,end='\r')
#             if addr[0] == self.myip: #根据ip匹配到来自同一台物理设备
#                 info = bytes('LNTP-ssfinish',encoding='utf-8')
#                 offset = struct.pack('d',self.clk_time_offset)
#                 self.client.send(info + offset)
#             else: # 不同设备，开始同步
#                 info = bytes('LNTP----start', encoding='utf-8')
#                 self.client.send(info + b'\x00'*8)
#                 self._syncloop()
#             self.client.close()
#             print('[LNTP] synchronize network time with client @%s-%i, OK'%addr)
#
#     def _syncloop(self):
#         while True:
#             buf = self.client.recv(128)
#             info = bytes.decode(buf[:13], encoding='utf-8')
#             if info == 'LNTP-----over':
#                 info = bytes('LNTP-s-finish', encoding='utf-8')
#                 offset = struct.pack('d', self.clk_time_offset)
#                 self.client.send(info + offset)
#                 break
#             else:
#                 info = bytes('xxxxxxxxxxxxx', encoding='utf-8')
#                 clock_buf = struct.pack('d',getclk())
#                 self.client.send(info + clock_buf)

class LNTPClient():
    def __init__(self,server_addr):
        self.er = None
        self.offset = None
        self.server_addr = server_addr

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('[LNTP] connect to the server', end='\r')
        connect = False

        for i in range(31):
            try:
                self.sock.connect(self.server_addr)
                connect = True
                break
            #except socket.error:
            except:
                utime.sleep(2)

        if not connect:
            raise Exception('[LNTP] connect to the server: failure')
        else:
            print('[LNTP] connect to the server: OK')

        # 开始同步
        buf = self.sock.recv(128)
        info = bytes.decode(buf[:13],'utf-8')
        if info == 'LNTP-ssfinish':  # 同一物理设备
            self.er = 0
            self.offset = struct.unpack('d', buf[13:21])[0]

        elif info == 'LNTP----start':
            self._sync_loop()
        else:
            raise Exception('unknown error')

        self.sock.close()
        print('[LNTP] sync finish! clock offset: %f'%(self.er+self.offset))

    def _sync_loop(self):
        _t = 65536
        _clk_server = 0
        _clkA = 0

        info = bytes('LNTP----doing', 'utf-8')
        for i in range(10):
            clkA = getclk()
            clk_buf = struct.pack('d', clkA)
            self.sock.send(info + clk_buf)
            srvbuf = self.sock.recv(128)
            clkB = getclk()
            clk_server = struct.unpack('d',srvbuf[13:21])[0]
            t = 0.5*(clkB - clkA)

            if t < _t:
                _t = t
                _clk_server = clk_server
                _clkA = clkA

            utime.sleep(0.2)

        info = bytes('LNTP-----over--------', 'utf-8')
        self.sock.send(info)

        # 取通信时间最短的一组计算参数
        self.er = _clk_server - _t - _clkA

        srvbuf = self.sock.recv(128)
        info = bytes.decode(srvbuf[:13], 'utf-8')
        if info != 'LNTP-s-finish':
            raise Exception('[Info] unknown error!')
        else:
            self.offset = struct.unpack('d', srvbuf[13:21])[0]
            
        print('offset',struct.unpack('d', srvbuf[13:21])[0])

    def lntp_clk1(self):  # 浮点运算精度有限
        '''
        :return:  timestamp, datetime string
        '''
        timestamp = getclk() + self.er + self.offset
        d,i = math.modf(timestamp)
        dstr = '%i-%i-%i %i:%i%i'%(utime.localtime(int(i))[:6]) + '%.6f'%(d)
        return timestamp,None,dstr
        
    def lntp_clk(self):  # 浮点运算精度有限，只提供原始数据，最终的合成由上位机完成
        timestamp = getclk()
        return timestamp,self.er,self.offset,TIMOFFSET
        

def test():
    from esp32ap import Esp32Ap
    ap = Esp32Ap()
    print('waiting')
    while not ap.isconnected():
      utime.sleep(1)
      
    print('connected')
    
    #utime.sleep(15)
    
    #lntp = LNTPClient(('192.168.66.2',8989))
    #lntp.start()

    #for i in range(100):
    #    _,_,now = lntp.lntp_clk()
    #    print(now,end='\r')
    #    utime.sleep(1)
    
def t1():
    #timestamp = getclk() + 946656000.0
    timestamp = getclk()
    print(timestamp)
    d,i = math.modf(timestamp)
    print(d)
    print(i)
    dstr1 = '%i-%i-%i %i:%i:%i'%(utime.localtime(int(i))[:6])
    dstr2 =  '%.6f'%(d)
    return timestamp,None,dstr1+dstr2[1:]

def test1():
    for i in range(100):
      t,_,s = t1()
      print(s,end='\r')
      utime.sleep(1)





