#coding:utf-8
#author:mrtang
#date:2020.1.7

# log:
# 2020.1.11 0:15am 调试完成，注意任何代码的修改在workspace中，
# 避免直接在device中修改代码，防止代码丢失

# 引脚连接说明
# drdy <---> io27
# miso <---> io12 (spi id: 1  baudrate=40000000)  硬件spi
# sclk <---> io14  硬件spi
# cs   <---> io26
# reset<---> io33
# mosi <---> io13  硬件spi

# 由于clock_sel引脚已经置高，所以默认使用内部时钟，2.048Mhz


import utime
from machine import Pin
from machine import Timer
from machine import SPI
from machine import PWM
from ads1299_locals import *
import struct


class Ads1299:
  def __init__(self,drdy = 27, miso = 12, sclk = 14, cs = 26, clk = 25, reset = 33, mosi = 13):
    data_ready = Pin(drdy,Pin.IN,Pin.PULL_UP)
    data_ready.irq(trigger=Pin.IRQ_FALLING,handler=self._data_ready_callback)
    
    self.rst = Pin(reset,Pin.OUT)
    self.cs = Pin(cs,Pin.OUT,value=0) #使能
    
    # SPI init
    self.spi = SPI(1,baudrate=4000000,polarity=0,phase=1,firstbit=SPI.MSB,sck=Pin(sclk),mosi=Pin(mosi),miso=Pin(miso))

    self.buffer = bytearray(0)
    self.status = bytearray(3)
    
    # 以下用于测试
    self.count = 0
    tim = Timer(-1)
    tim.init(period=1000, mode=Timer.PERIODIC, callback=self.tim_callback)
    
  def powr_up(self,t = 3):  
    #ads初始化要求vcap1(100uF)充电至1.1v以上，大约需要3秒，可视启动ads模块的时间决定是否调用
    utime.sleep(t)
    
  def _data_ready_callback(self,pin):
    buf = bytearray(27)
    self.spi.readinto(buf)
    self.status = buf[:3]
    databuffer = buf[3:]
    #self.buffer += databuffer
    
    self.count += 1
    
  
  def write_cmd(self,data):
    self.spi.write(HEXCODE[data])
    utime.sleep_us(40)

  def get_data(self):
    # int24高位先行
    #data = self.buffer
    #self.buffer = bytearray(0)
    #return data
    
    print(self.count)
    self.count = 0
    
  # 测试
  def tim_callback(self,t):
    self.get_data()
    
  def channel_setting(self,power_down = False, gain_set = ADS_GAIN24,input_type = ADSINPUT_NORMAL, SRB2_set = True):
    setting = 0x00
    if power_down:  setting |= 0x80
    setting |= gain_set
    setting |= input_type
    if SRB2_set:    setting |= 0x08
    
    for i in range(8):  #对8个通道逐个进行增益和输入模式配置
      self.write_register(CH1SET + i,setting)
    
    # 注意 openbci中line:2583-2616未复现
    
  def write_register(self,address,value):
    # 写寄存器：wreg expects 010rrrrr, where rrrrr = address
    # 双字节命令，首先写入寄存器地址，然后写入寄存器值
    # 寄存器地址高3位固定为010
    opcode = address + 0x40   
    self.write_cmd(opcode)
    self.write_cmd(value)
    
  def reset(self):
    self.cs.value(0)
    self.rst.value(1)
    utime.sleep_us(100)
    self.rst.value(0)
    utime.sleep_us(100)
    self.rst.value(1)
    utime.sleep_us(100)
  
  def init(self):
    self.cs.value(0)
    self.rst.value(1)
    utime.sleep_us(100)
    self.rst.value(0)
    utime.sleep_us(100)
    self.rst.value(1)
    utime.sleep_us(100)
    
    # 进入配置模式
    self.write_cmd(SDATAC)
    
    # 配置寄存器1：菊花链、时钟、采样率等
    # 一旦启用CLOCK_EN，将可以从clk观察到2.048Mhz波形输出,可用于调试
    #self.write_register(CONFIG1,ADS1299_CONFIG1_DAISY_NOT | SAMPLE_RATE_8K | CLOCK_EN)
    self.write_register(CONFIG1,ADS1299_CONFIG1_DAISY_NOT | SAMPLE_RATE_250 | CLOCK_EN)
    #self.write_register(CONFIG1,ADS1299_CONFIG1_DAISY_NOT | SAMPLE_RATE_500)
    
    
    # 配置寄存器2：测试信号
    # 不配置
    
    # 配置通道：增益、输入模式等
    self.channel_setting()
    
    # 配置寄存器3：配置内部/外部参考以及bias等
    self.write_register(CONFIG3,0b11101100)
    
    # 完成配置，启动
    self.write_cmd(START)   #启动，注意START引脚接地
    self.write_cmd(RDATAC)  #进入读数据模式
    
def main():
  ads = Ads1299()
  #ads.powr_up()
  ads.init()































