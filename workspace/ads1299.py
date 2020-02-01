#coding:utf-8
#author:mrtang
#date:2020.1.7

# log:
# 2020.1.11 0:15am 调试完成，注意任何代码的修改在workspace中，
# 避免直接在device中修改代码，防止代码丢失

# 引脚连接说明
# drdy <---> 11
# miso <---> 12 (spi id: 1  baudrate=40000000)
# sclk <---> 14
# cs   <---> 16
# clk  <---> 17
# reset<---> 18
# mosi <---> 13


import time
from machine import Pin
from machine import SPI
from machine import PWM
from ads1299_locals import *


class Ads1299:
  def __init__(self,drdy = 11, miso = 12, sclk = 14, cs = 16, clk = 17, reset = 18, mosi = 13):
    # GPIO init
    _DRDY = Pin(drdy,Pin.IN,Pin.PULL_UP)
    _DRDY.irq(trigger=Pin.IRQ_FALLING,handler=self._data_ready_callback)
    self._RESET = Pin(reset,Pin.OUT,value=0)
    self._CS = Pin(cs,Pin.OUT,value=1)
  
    # SPI init
    self.spi = SPI(1,baudrate=4000000,sck=Pin(sclk),mosi=Pin(mosi),miso=Pin(miso))
    
    # master clock init,配合clksel引脚置高，选择使用外部时钟2.048MHz
    self.pwm = PWM(Pin(clk,Pin.OUT),freq=2048000,duty=512)
    self._tclk = 0.5  #us
    self.buffer = bytearray(0)
    self.status = bytearray(3)

    time.sleep_ms(50)

  def _data_ready_callback(self,pin):
    buf = bytearray(27)
    self.spi.read_into(buf)
    self.status = buf[:3]
    databuffer = buf[3:]
    self.buffer += databuffer
    
  def get_data(self):
    # int24高位先行
    data = self.buffer
    self.buffer = bytearray(0)
    return data
    
  def channel_setting(self,power_down = False, gain_set = ADS_GAIN24,input_type = ADSINPUT_NORMAL, SRB2_set = True):
    setting = 0x00
    if power_down:  setting |= 0x80
    setting |= gain_set
    setting |= input_type
    if SRB2_set:    setting |= 0x08
    
    for i in range(8):
      self.write_register(CH1SET + i,setting)
    
    # openbci中line:2583-2616未复现
    time.sleep_us(10*self._tclk)
    
  def write_register(self,address,value):
    opcode = address + 0x40   # 写寄存器：wreg expects 010rrrrr, where rrrrr = address
    self.spi.write(opcode)    # 写地址
    self.spi.write(0x00)
    self.spi.write(value)     # 写入配置值
  
  def init(self):
    # recommended power up sequence requiers >Tpor (2*18*0.5us @2.048MHz)
    time.sleep_ms(150)
    # reset the device
    self._RESET.value(0)
    time.sleep_us(4)
    self._RESET.value(1)
    time.sleep_us((18+10)*self._tclk)
    
    # reset the on-board ADS registers and stop datacontiuous mode 
    self._CS.value(0)     #片选
    time.sleep_us((18+10)*self._tclk)  #wait for 18tclk
    
    # enter the configure mode
    self.spi.write(SDATAC)
    time.sleep_ms(10)
    
    # turn off clk output and set sampling rate 500Hz
    # 寄存器1主要配置DAISY_EN,CLK_EN,采样率
    self.write_register(CONFIG1,ADS1299_CONFIG1_DAISY_NOT | SAMPLE_RATE_500)
    
    # 配置各个通道,使用默认配置
    self.channel_setting()
    
    # 配置寄存器3
    self.write_register(CONFIG3,0b11101100)
    time.sleep_ms(1)  # enable internal reference drive and etc.
    
    # When using the START command to control conversions, hold the START pin low
    self.spi.write(START)
    time.sleep_us(4*self._tclk)
    self.spi.write(RDATAC)
    time.sleep_us(4*self._tclk)













