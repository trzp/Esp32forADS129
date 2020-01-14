#coding:utf-8
#author:mrtang
#date:2020.1.7

# log:
# 2020.1.11 0:15am 调试完成，注意任何代码的修改在workspace中，
# 避免直接在device中修改代码，防止代码丢失

#


import network
import time
import esp
from machine import Pin

esp.osdebug(None)

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
  









