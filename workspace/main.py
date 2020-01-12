#coding:utf-8
#author:mrtang
#date:2020.1.7

# log:
# 2020.1.11 0:15am 调试完成，注意任何代码的修改在workspace中，
# 避免直接在device中修改代码，防止代码丢失


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
  
  
  
# 数据ok ads 
class EEGamp:
  def __init__(self):    
    self.ads1299 = ADS1299()
    self.ads1299.init()
    self.ap = Esp32Ap()
    
    self.data_buf = ''
    
    p = Pin(25,Pin.OUT)
    p.irq(callback=self.data_ready)

    self.sock_stream = SockStream()
    
  def data_ready(self,pin):
    self.data_buf += self.ads1299.read_data()
    
  def mainloop(self):
    while True:
      self.sock_stream.push(self.data_buf)
      self.data_buf = ''
      time.sleep(0.1)   
  
    
if __name__ == '__main__':
  amp = EEGamp()
  amp.mainloop()
  






