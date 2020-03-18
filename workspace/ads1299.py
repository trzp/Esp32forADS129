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

EEGACQUIRE = 0x01
LOFFDETECT = 0x02


class Ads1299:
  def __init__(self,pinconfig = PINCONFIG,fs = 250):
    self.virgin = True
    self.mode = EEGACQUIRE
    
    # test
    self.co = 0
    self.data_num = 0
    self.max_data_num = 500
    
    data_ready = Pin(pinconfig['drdy'],Pin.IN,Pin.PULL_UP) # 内部上拉，默认高电平，捕捉下降沿
    data_ready.irq(trigger=Pin.IRQ_FALLING,handler=self._data_ready_callback)
    
    self.rst = Pin(pinconfig['reset'],Pin.OUT)
    self.cs = Pin(pinconfig['cs'],Pin.OUT) #使能
    self.pown = Pin(pinconfig['pown'],Pin.OUT,value=0)  #默认低功耗设置
    
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
    # 数据格式
    # 24bits status + ch1(24bits) + ch2(24bits) + ...
    # status: 1100 + LOFF_STATP(8 bits) + LOFF_STATN(8 bits) + bits[4:7] of GPIO
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
    
  def channel_setting(self,power_down = False, gain_set = ADS_GAIN24,input_type = ADSINPUT_NORMAL, SRB2_set = True):
    # 这里从N-side输入信号，将所有P-side连接至srb2
    setting = 0x00
    if power_down:  setting |= 0x80
    setting |= gain_set
    setting |= input_type
    if SRB2_set:    setting |= 0x08
    
    for i in range(8):  #对8个通道逐个进行增益和输入模式配置
      self.write_register(CH1SET + i,setting)

  def write_register(self,address,value):
    # 写寄存器步骤
    # stp1:写寄存器地址
    # stp2:写n,代表下面要写入n+1个寄存器值
    # stp3:连续写入n+1个寄存器值
    addr = address + 0x40
    self.spi.write(BYTESMAP[addr])
    self.spi.write(BYTESMAP[0])     #默认只写入一个值
    self.spi.write(BYTESMAP[value])
    utime.sleep_us(20)
    
  def start_loff_detect(self):
    self.mode = LOFFDETECT
    self.reset()
    
    # 进入配置模式
    self.write_cmd(SDATAC)
    
    # 配置寄存器1：菊花链、时钟、采样率等
    self.write_register(CONFIG1,ADS1299_CONFIG1_DAISY_NOT | self.samplingrate | CLOCK_EN)
    
    # 配置通道：增益、输入模式等
    self.channel_setting()
    
    # 配置寄存器LOFF
    # bit3:2 ILEAD_OFF: 0b00->6nA 0b01->24nA 0b10->6uA 0b11->24uA
    # bit1:0 FLEAD_OFF: 0b00->DC 0b01->AC 7.8Hz 0b10->AC 31.2Hz 0b11->AC fdr/4
    # 配置为6nA 31.2Hz激励
    self.write_register(LOFF,0x02)

    # 配置N-side通道连接上测试电流源
    self.write_register(LOFF_SENSP,0x00)
    self.write_register(LOFF_SENSN,0xFF)
    
    # 激励电流的方向，翻转，将AVDD连接到N-side，从N-side灌入电流
    self.write_register(LOFF_FLIP,0xFF)
    
    # config4 开启lead-off comparators
    self.write_register(CONFIG4,0x02)

    # 完成配置，启动
    self.write_cmd(START)
    self.write_cmd(RDATAC)  #进入读数据模式
    utime.sleep_ms(25)

  def reset(self):
    self.cs.value(0)      #片选
    self.pown.value(1)    #唤醒
    self.rst.value(1)     #复位,所有寄存器的设置
    utime.sleep_us(50)
    self.rst.value(0)
    utime.sleep_us(100)
    self.rst.value(1)
    
    if self.virgin:       #初次，等待vcap1充电
      utime.sleep_ms(500)
      self.virgin = False
    else:
      utime.sleep_us(100)
    
  def start_data_acquire(self):
    self.mode = EEGACQUIRE
    self.reset() 
    
    # 进入配置模式
    self.write_cmd(SDATAC)
    
    # 配置寄存器1：菊花链、时钟、采样率等
    # 一旦启用CLOCK_EN，将可以从clk观察到2.048Mhz波形输出,可用于调试
    #self.write_register(CONFIG1,ADS1299_CONFIG1_DAISY_NOT | SAMPLE_RATE_8K | CLOCK_EN)
    self.write_register(CONFIG1,ADS1299_CONFIG1_DAISY_NOT | self.samplingrate | CLOCK_EN)
    #self.write_register(CONFIG1,ADS1299_CONFIG1_DAISY_NOT | self.samplingrate)
    
    
    # 配置寄存器2：测试信号
    # 相当于内部产生一个信号，便于从后端观察系统运行情况
    
    # 配置通道：增益、输入模式等
    self.channel_setting()
    
    self.write_register(BIAS_SENSP,0xff)
    self.write_register(BIAS_SENSN,0xff)
    
    # 配置寄存器3：配置内部/外部参考以及bias等
    self.write_register(CONFIG3,0b11101100)
    
    # 完成配置，启动
    self.write_cmd(START)
    self.write_cmd(RDATAC)  #进入读数据模式
    utime.sleep_ms(25)
    
  def stop(self):
    self.write_cmd(SDATAC)
    self.write_cmd(STOP)    #停止
    self.pown.value(0)      #进入省电模式
    self.buffer = bytearray(0)  #将可能残余的数据清除
    
    
def main():
  ads = Ads1299()
  ads.reset()
  ads.start()
  for i in range(240):
    print(ads.co)
    ads.co = 0
    utime.sleep(1)
  
  ads.stop()










































