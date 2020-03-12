from machine import SPI,Pin
import struct
import utime

def main0():
  en = Pin(25,Pin.OUT,value=1)
  hspi = SPI(1,baudrate=1000,polarity=0,phase=1,bits=8,firstbit=SPI.MSB,sck=Pin(14),mosi=Pin(13),miso=Pin(12))
  while True:
    for i in range(16):
      d = i << 4
      d = d | 0x0f
      #en.value(0)
      #utime.sleep_us(20)
      b = struct.pack('B',d)
      hspi.write(b)
      #utime.sleep_us(20)
      #en.value(1)
      utime.sleep_ms(50)


def main1():
  rst = Pin(33,Pin.OUT)
  en = Pin(25,Pin.OUT,value=1)
  hspi = SPI(1,baudrate=400000,polarity=0,phase=1,bits=8,firstbit=SPI.MSB,sck=Pin(14),mosi=Pin(13),miso=Pin(12))
  rst.value(0)
  utime.sleep_ms(200)
  rst.value(1)
  en.value(0)
  hspi.write(struct.pack('B',65))
  utime.sleep_us(50)
  hspi.write(struct.pack('B',240))
  utime.sleep_us(50)
  
  
def main(): #测试struct和‘\x’字符发送的区别
  vspi = SPI(2,baudrate=1000,polarity=0,phase=1,bits=8,firstbit=SPI.MSB,sck=Pin(18),mosi=Pin(23),miso=Pin(19))
  while True:
    vspi.write(struct.pack('B',194))
    utime.sleep_ms(50)
    vspi.write('\xc2')
    utime.sleep_ms(50)
    vspi.write('\xc2'.encode())
    utime.sleep_ms(150)

  









