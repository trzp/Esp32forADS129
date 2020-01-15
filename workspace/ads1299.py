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


import network
import time
import esp
from machine import Pin
from machine import SPI
from machine import PWM
from ads1299_locals import *


# ADS1299 COMMANDS
# SYSTEM COMMANDS
WAKEUP = 0x02
STANDBY = 0x04
RESET = 0x06
START = 0x08
STOP = 0x0A

# DATA READ COMMANDS
RDTATAC = 0x10
SDATAC = 0x11
RDATA = 0x12

# REGISTER READ COMMANDS
RREG = None
WREG = None

class Ads1299:
  def __init__(self,drdy = 11, miso = 12, sclk = 14, cs = 16, clk = 17, reset = 18, mosi = 13):
    # GPIO init
    _DRDY = Pin(drdy,Pin.IN,Pin.PULL_UP)
    _DRDY.irq(trigger=Pin.IRQ_FALLING,handler=self.data_ready)
    self._RESET = Pin(reset,Pin.OUT,value=0)
    self._CS = Pin(cs,Pin.OUT,value=1)
  
    # SPI init
    self.spi = SPI(1,baudrate=4000000,sck=Pin(sclk),mosi=Pin(mosi),miso=Pin(miso))
    
    # master clock init,配合clksel引脚置高，选择使用外部时钟2.048MHz
    self.pwm = PWM(Pin(clk,Pin.OUT),freq=2048000,duty=512)
    self._tclk = 0.5  #us
    self.buf = bytearray(27)
    
    time.sleep_ms(50)
    
  def _data_ready(self,pin):
    self.spi.read_into(self.buf)
    
  def read_data(self):
    return 0
    
  def write_register(self,address,value):
    opcode = address + 0x40   # wreg expects 010rrrrr, where rrrrr = address
    self.spi.write(opcode)
    self.spi.write('0x00')
    self.spi.write(value)
  
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
    self.write_register(CONFIG1,ADS1299_CONFIG1_DAISY_NOT | SAMPLE_RATE_500)
    
    # DEFAULT CHANNEL SETTINGS FOR ADS line:2727
    # 老复杂的寄存器配置
    
    
    time.sleep_us(4)
    self.write_register(CONFIG3,0b11101100)
    time.sleep_ms(1)  # enable internal reference drive and etc.
    
    
    
    
    
    
    
    
    
    time.sleep_us(4*self._tclk)
    self.spi.write(START)
    time.sleep_us(3)
    self.spi.write(RDTATAC)
   
  def deinit(self):
    self._RESET.value(0)
    time.sleep(0.1)
    
    
    
    
    
    
    
    
    
    
  
    
    




class Esp32Ap:
  def __init__(self,essid='ESP32',myip='192.168.66.1'):
    self.essid = essid
    self.myip = myip
    tem = myip.split('.')
    tem[2]='0'
    tem[3]='1'
    self.gateway = '.'.join(tem)
     
    self.ap = network.WLAN(network.AP_IF)
    self.ap.active(True)
    self.ap.ifconfig((self.myip, '255.255.255.0', self.gateway, '255.255.255.255'))
    self.ap.config(essid=self.essid,password='12345')
    
    print('[Esp32] board initilized!')
    print('[Esp32] essid: %s'%(self.essid))
    print('[Esp32] ip: %s'%(self.myip))
    
  def isconnected(self):
    return self.ap.isconnected()
    
class SockDataSender():
  def __init__(self,myip,clientip,clientport):
    self.sock = usocket.socket(usocket.AF_INET,usocket.SOCK_DGRAM)
    self.toaddr = (clientip,clientport)
  
  def send(buf):
    if self.ap.isconnected():
      self.
    
    
    
class ADS1299:
  def __init__(self):
    self.data_buf = ''
   
  def init(self):
    pass
    
  def deinit(self):
    pass
  
  def read_data(self):
    # operation read data
    return data
  
  
  
# ads DRDY <---> Pin25
DRDYPIN = 25
MYIP = '192.168.66.1'
CLIENTIP = '192.168.66.2'
CLIENTPORT = 9000
  
class EEGamp:
  def __init__(self):    
    self.ads1299 = ADS1299()
    self.ads1299.init()
    self.data_buf = ''
    
    # 外部中断，接受ADS data ready信号
    drdyp = Pin(DRDYPIN,Pin.IN,Pin.PULL_UP)
    drdyp.irq(trigger=Pin.IRQ_FALLING,handler=self.data_ready)
    
    self.ap = Esp32Ap()
    while self.ap.isconnected():
      time.sleep(0.25)
    
    self.data_buf = ''
    self.sock = usocket.socket(usocket.AF_INET,usocket.SOCK_DGRAM)
    self.toaddr = (CLIENTIP,CLIENTPORT)
      
  def data_ready(self,pin):
    self.data_buf += self.ads1299.read_data()
    
  def mainloop(self):
    count = 0
    while True:
      if self.ap.isconnected():
        self.sock.sendto(self.data_buf,self.toaddr)
        self.data_buf = ''
        count = 0
      else:                 # 断线超过10秒，数据清空
        count += 1
        if count > 100:
          self.data_buf = ''
      
      time.sleep(0.1)
  
    
if __name__ == '__main__':
  amp = EEGamp()
  amp.mainloop()
  














