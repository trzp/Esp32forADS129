#coding:utf-8

import socket
from show_eeg import *
from unpack_ads129x_data import *
import numpy as np

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(('192.168.66.2',8090))
sock.sendto(b'',('192.168.66.1',8089))



# while True:
    # buf,_ = sock.recvfrom(8000)
    # print(len(buf))

ads_unpack = unpackAds1299Data()
p = PlotEEG2(channels=2,notchfilter=False,yamp = 100)

ndata = []

b = bytearray(0)

while p.on:
    buf,_ = sock.recvfrom(4096)
    
    b += buf

    data = []
    for i in range(0,len(buf),3):   #每三个字节为一个数据
        literal_bytes = buf[i:i+3]
        myInt = ads_unpack.unpack(literal_bytes)
        data.append(myInt)
    
    pnum = int(len(data)/8)
    data = np.array(data,dtype=np.float32)
    data = data.reshape(pnum,8).transpose()
    data = data[0:2,:]
    p.update(data)
    
    ndata.append(data)
    
    print(pnum)
    
    
d = np.hstack(ndata)
np.save('data.npy',d)

with open('buf.dat','wb') as f:
    f.write(b)