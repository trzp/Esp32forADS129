#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/12 11:20
# @Version : 1.0
# @File    : checkbuf.py
# @Author  : Jingsheng Tang
# @Version : 1.0
# @Contact : mrtang@nudt.edu.cn   mrtang_cs@163.com
# @License : (C) All Rights Reserved

from unpack_ads129x_data import unpackAds1299Data
import numpy as np
import scipy.signal as scipy_signal
import matplotlib.pyplot as plt

# decoder = unpackAds1299Data()
#
# with open('buf.dat','rb') as f:
#     buf = f.read()
#
# data = []
# for i in range(0,len(buf),3):   #每三个字节为一个数据
#     literal_bytes = buf[i:i+3]
#     myInt = decoder.unpack(literal_bytes)
#     data.append(myInt)
#
# print(len(data))

dd = np.load('data0.npy')

# bandpass filter
# bandpass = [1,90]
# fs = 250
# Wp = np.array([bandpass[0] / fs, bandpass[1] / fs])
# Ws = np.array([(bandpass[0]*0.5) / fs, (bandpass[1]+10) / fs])
# N, Wn = scipy_signal.cheb1ord(Wp, Ws, 3, 40)
# bpB, bpA = scipy_signal.cheby1(N, 0.5, Wn, 'bandpass')

# notch filter
# Fo = 50
# Q = 15
# w0 = Fo / (fs)
# notchB, notchA = scipy_signal.iirnotch(w0=w0, Q=Q)

sig = dd

# sig = scipy_signal.filtfilt(notchB, notchA, sig)
# sig = scipy_signal.filtfilt(bpB, bpA, sig)

plt.plot(sig[0,:])
# plt.show()