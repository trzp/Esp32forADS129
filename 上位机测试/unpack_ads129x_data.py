#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/6 19:11
# @Version : 1.0
# @File    : unpack_ads129x_data.py
# @Author  : Jingsheng Tang
# @Version : 1.0
# @Contact : mrtang@nudt.edu.cn   mrtang_cs@163.com
# @License : (C) All Rights Reserved

import struct

class unpackAds1299Data():
    def __init__(self,ads_gain = 24,scaling_output = True):
        ADS1299_Vref = 4.5         # reference voltage for ADC in ADS1299.  set by its hardware
        ADS1299_gain = ads_gain    #由主控芯片进行寄存器配置，默认设置为24
        self.scale_fac_uVolts_per_count = ADS1299_Vref /float((pow(2, 23) - 1)) / ADS1299_gain * 1000000.
        self.scaling_output = scaling_output
    
    def unpack(self,literal_bytes):    # 接受三个字节,对应一个数据
        unpacked = struct.unpack('3B', literal_bytes)

        # 3byte int in 2s compliment    对补码的处理
        if (unpacked[0] > 127):
            pre_fix = bytes(bytearray.fromhex('FF'))
        else:
            pre_fix = bytes(bytearray.fromhex('00'))

        literal_bytes = pre_fix + literal_bytes   #补齐为四字节

        # unpack little endian(>) signed integer(i)  #高位先行，即big-endian
        # (makes unpacking platform independent)
        myInt = struct.unpack('>i', literal_bytes)[0]

        if self.scaling_output:
            return myInt * self.scale_fac_uVolts_per_count
        else:
            return myInt