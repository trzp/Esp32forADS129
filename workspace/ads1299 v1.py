#coding:utf-8
#author:mrtang
#date:2020.1.7

# log:
# 2020.1.11 0:15am 调试完成，注意任何代码的修改在workspace中，
# 避免直接在device中修改代码，防止代码丢失

# 2020.3.8 连接上位机显示曲线联调成功

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
from ads1299_locals import *
import struct

PINCONFIG = {'drdy':27, 'miso':12, 'sclk':14, 'mosi':13, 'cs':26, 'reset':33, 'pown':32}


# 硬件连接说明
# reset 引脚拉高，使用命令复位，节省io
# pown 连接一路io,用于在闲置时省电（5uW）,恢复需要150ms
# 默认启用in1N - in8N引脚，将srb2连接至所有通道的正输入端即in1P - in8P. srb1断开


class Ads1299:
  def __init__(self,pinconfig = PINCONFIG,fs = 250):
    self.virgin = True
    
    #test
    # self.co = 0
    # self.data_num = 0
    # self.max_data_num = 500
    
    data_ready = Pin(pinconfig['drdy'],Pin.IN,Pin.PULL_UP) # 内部上拉，默认高电平，捕捉下降沿
    data_ready.irq(trigger=Pin.IRQ_FALLING,handler=self._data_ready_callback)

    self.cs = Pin(pinconfig['cs'],Pin.OUT)      #使能
    self.pown = Pin(pinconfig['pown'],Pin.OUT)  #低功耗引脚

    
    # SPI init
    self.spi = SPI(1,baudrate=4000000,polarity=0,phase=1,firstbit=SPI.MSB,sck=Pin(pinconfig['sclk']),mosi=Pin(pinconfig['mosi']),miso=Pin(pinconfig['miso']))

    self.buffer = bytearray(0)
    self.status = bytearray(3)
    
    if fs == 2000:
      self.samplingrate = SAMPLE_RATE_2K
    elif fs == 1000:
      self.samplingrate = SAMPLE_RATE_1K
    elif fs == 500:
      self.samplingrate = SAMPLE_RATE_500
    elif fs == 250:
      self.samplingrate = SAMPLE_RATE_250
    else:
      self.samplingrate = SAMPLE_RATE_250
    
    
    
  def _data_ready_callback(self,pin):
    buf = bytearray(27)
    self.spi.readinto(buf)
    self.status = buf[:3]
    databuffer = buf[3:]
    self.buffer += databuffer
    
    # 超时未读取，自动清空
    self.data_num += 1
    if self.data_num > self.max_data_num:
      self.buffer = bytearray(0)
      self.data_num = 0
      
    self.co += 1
      
  def read_data(self):  # output interface
    # int24高位先行
    buf = self.buffer
    self.buffer = bytearray(0)
    self.data_num = 0
    return buf
  
  def write_cmd(self,data):
    self.spi.write(BYTESMAP[data])
    utime.sleep_us(20)
    
  def channel_setting(self,gain_set = ADS_GAIN24,input_type = ADSINPUT_NORMAL):
    setting |= 0x80          # power_down false
    setting |= gain_set      # 增益 
    setting |= input_type    # 模式
    setting |= 0x08          # 连接srb2,即将该通道的正端连接到srb2(所有通道的正端连接到srb2作为共同参考电极输入)

    for i in range(8):  #对8个通道逐个配置
      self.write_register(CH1SET + i,setting)
      
    # BIAS_SENSN, BIAS_SENSP寄存器用于将通道连接到BIAS放大器反馈给其他通道用于抑制工模等噪声，相比较直接使用电极
    # 作为bias_in，可能有更好的效果。默认不开启。以后可以尝试

  def write_register(self,address,value):
    # 写寄存器步骤
    # stp1:写寄存器地址
    # stp2:写n,代表下面要写入n+1个寄存器值
    # stp3:连续写入n+1个寄存器值
    addr = address + 0x40
    self.spi.write(BYTESMAP[addr])
    self.spi.write(b'\x00')     #默认只写入一个值
    self.spi.write(BYTESMAP[value])
    utime.sleep_us(20)
    
  def start(self):
    if self.virgin:       #初次，等待vcap1充电
      utime.sleep_ms(50)
      self.virgin = False

    utime.sleep_ms(1)
    self.cs.value(0)      #片选
    self.pown.value(1)    #唤醒
    utime.sleep_ms(150)   #需要150ms唤醒
    self.write_cmd(RESET) #复位
    utime.sleep_us(12)

    # 进入配置模式
    self.write_cmd(SDATAC)
    
    # 配置寄存器1：菊花链、时钟、采样率等
    # 一旦启用CLOCK_EN，将可以从clk观察到2.048Mhz波形输出,可用于调试
    #self.write_register(CONFIG1,ADS1299_CONFIG1_DAISY_NOT | self.samplingrate | CLOCK_EN)
    self.write_register(CONFIG1,ADS1299_CONFIG1_DAISY_NOT | self.samplingrate)

    # 配置通道：增益、输入模式等
    self.channel_setting()
    
    # 配置右腿驱动，将所有信号通道（包括正负）都用于产生共模信号来输出到右腿驱动信号 bias_out
    self.write_register(BIAS_SENSP,0xff)
    self.write_register(BIAS_SENSN,0xff)
    
    # 配置寄存器3：配置内部/外部参考以及bias等
    self.write_register(CONFIG3,0b11101100)
    
    # 完成配置，启动
    self.write_cmd(RDATAC)  #进入读数据模式
    self.write_cmd(START)

    
  def stop(self):
    self.write_cmd(SDATAC)
    self.write_cmd(STOP)    #停止
    self.pown.value(0)      #进入省电模式
    self.buffer = bytearray(0)  #将可能残余的数据清除
    
    
def main():
  ads = Ads1299()
  ads.start()
  for i in range(240):
    print(ads.co)
    ads.co = 0
    utime.sleep(1)
  
  ads.stop()









































