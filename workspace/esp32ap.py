#coding:utf-8
#author:mrtang
#date:2020.1.7

# log:
# 2020.1.11 0:15am 调试完成，注意任何代码的修改在workspace中，
# 避免直接在device中修改代码，防止代码丢失

#


import network
import utime

class Esp32Ap:
  def __init__(self,essid='ESP32',myip='192.168.66.1'):
    self.essid = essid
    self.myip = myip
    tem = myip.split('.')
    tem[2]='0'
    tem[3]='1'
    self.gateway = '.'.join(tem)
     
    self.ap = network.WLAN(network.AP_IF)
    self.ap.active(False)
    utime.sleep(0.5)
    self.ap.active(True)
    self.ap.ifconfig((self.myip, '255.255.255.0', self.gateway, '255.255.255.255'))
    self.ap.config(essid=self.essid,password='12345')
    
    print('[Esp32] board initilized!')
    print('[Esp32] essid: %s'%(self.essid))
    print('[Esp32] ip: %s'%(self.myip))
    
  def isconnected(self):
    return self.ap.isconnected()
    
def test():
  ap = Esp32Ap()



