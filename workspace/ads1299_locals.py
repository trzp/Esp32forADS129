#coding:utf-8
#author:mrtang
#date:2020.1.7

HEXCODE = [
  '\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\x09', '\x0a', '\x0b', '\x0c', '\x0d', '\x0e', '\x0f', 
  '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\x1a', '\x1b', '\x1c', '\x1d', '\x1e', '\x1f', 
  '\x20', '\x21', '\x22', '\x23', '\x24', '\x25', '\x26', '\x27', '\x28', '\x29', '\x2a', '\x2b', '\x2c', '\x2d', '\x2e', '\x2f',
  '\x30', '\x31', '\x32', '\x33', '\x34', '\x35', '\x36', '\x37', '\x38', '\x39', '\x3a', '\x3b', '\x3c', '\x3d', '\x3e', '\x3f',
  '\x40', '\x41', '\x42', '\x43', '\x44', '\x45', '\x46', '\x47', '\x48', '\x49', '\x4a', '\x4b', '\x4c', '\x4d', '\x4e', '\x4f', 
  '\x50', '\x51', '\x52', '\x53', '\x54', '\x55', '\x56', '\x57', '\x58', '\x59', '\x5a', '\x5b', '\x5c', '\x5d', '\x5e', '\x5f', 
  '\x60', '\x61', '\x62', '\x63', '\x64', '\x65', '\x66', '\x67', '\x68', '\x69', '\x6a', '\x6b', '\x6c', '\x6d', '\x6e', '\x6f', 
  '\x70', '\x71', '\x72', '\x73', '\x74', '\x75', '\x76', '\x77', '\x78', '\x79', '\x7a', '\x7b', '\x7c', '\x7d', '\x7e', '\x7f', 
  '\x80', '\x81', '\x82', '\x83', '\x84', '\x85', '\x86', '\x87', '\x88', '\x89', '\x8a', '\x8b', '\x8c', '\x8d', '\x8e', '\x8f', 
  '\x90', '\x91', '\x92', '\x93', '\x94', '\x95', '\x96', '\x97', '\x98', '\x99', '\x9a', '\x9b', '\x9c', '\x9d', '\x9e', '\x9f', 
  '\xa0', '\xa1', '\xa2', '\xa3', '\xa4', '\xa5', '\xa6', '\xa7', '\xa8', '\xa9', '\xaa', '\xab', '\xac', '\xad', '\xae', '\xaf', 
  '\xb0', '\xb1', '\xb2', '\xb3', '\xb4', '\xb5', '\xb6', '\xb7', '\xb8', '\xb9', '\xba', '\xbb', '\xbc', '\xbd', '\xbe', '\xbf', 
  '\xc0', '\xc1', '\xc2', '\xc3', '\xc4', '\xc5', '\xc6', '\xc7', '\xc8', '\xc9', '\xca', '\xcb', '\xcc', '\xcd', '\xce', '\xcf', 
  '\xd0', '\xd1', '\xd2', '\xd3', '\xd4', '\xd5', '\xd6', '\xd7', '\xd8', '\xd9', '\xda', '\xdb', '\xdc', '\xdd', '\xde', '\xdf', 
  '\xe0', '\xe1', '\xe2', '\xe3', '\xe4', '\xe5', '\xe6', '\xe7', '\xe8', '\xe9', '\xea', '\xeb', '\xec', '\xed', '\xee', '\xef', 
  '\xf0', '\xf1', '\xf2', '\xf3', '\xf4', '\xf5', '\xf6', '\xf7', '\xf8', '\xf9', '\xfa', '\xfb', '\xfc', '\xfd', '\xfe', '\Xff']

# gainCode choices
ADS_GAIN01 = 0b00000000
ADS_GAIN02 = 0b00010000
ADS_GAIN04 = 0b00100000
ADS_GAIN06 = 0b00110000
ADS_GAIN08 = 0b01000000
ADS_GAIN12 = 0b01010000
ADS_GAIN24 = 0b01100000

# sampling rate
# 手册44页，在主频为2.048MHz时
SAMPLE_RATE_16K = 0b10010000
SAMPLE_RATE_8K = 0b10010001
SAMPLE_RATE_4K = 0b10010010
SAMPLE_RATE_2K = 0b10010011
SAMPLE_RATE_1K = 0b10010100
SAMPLE_RATE_500 = 0b10010101
SAMPLE_RATE_250 = 0b10010110

WAKEUP =  0x02 # Wake-up from standby mode
STANDBY =  0x04 # Enter Standby mode
RESET =  0x06 # Reset the device registers to default
START =  0x08 # Start and restart synchronize conversions
STOP =  0x0A # Stop conversion
RDATAC =  0x10 # Enable Read Data Continuous mode default mode at power-up
SDATAC =  0x11 # Stop Read Data Continuous mode
RDATA =  0x12 # Read data by command supports multiple read back

ID_REG =   0x00	# this register contains ADS_ID
CONFIG1 =  0x01
CONFIG2 =  0x02
CONFIG3 =  0x03
LOFF =  0x04
CH1SET =  0x05
CH2SET =  0x06
CH3SET =  0x07
CH4SET =  0x08
CH5SET =  0x09
CH6SET =  0x0A
CH7SET =  0x0B
CH8SET =  0x0C
BIAS_SENSP =  0x0D
BIAS_SENSN =  0x0E
LOFF_SENSP =  0x0F
LOFF_SENSN =  0x10
LOFF_FLIP =  0x11
LOFF_STATP =  0x12
LOFF_STATN =  0x13
GPIO =  0x14
MISC1 =  0x15
MISC2 =  0x16
CONFIG4 =  0x17

ADSINPUT_NORMAL =      0b00000000
ADSINPUT_SHORTED =     0b00000001
ADSINPUT_BIAS_MEAS =   0b00000010
ADSINPUT_MVDD =        0b00000011
ADSINPUT_TEMP =        0b00000100
ADSINPUT_TESTSIG =     0b00000101
ADSINPUT_BIAS_DRP =    0b00000110
ADSINPUT_BIAL_DRN =    0b00000111
ADSTESTSIG_AMP_1X =  0b00000000
ADSTESTSIG_AMP_2X =  0b00000100
ADSTESTSIG_PULSE_SLOW =  0b00000000
ADSTESTSIG_PULSE_FAST =  0b00000001
ADSTESTSIG_DCSIG =  0b00000011
ADSTESTSIG_NOCHANGE =  0b11111111
ADS1299_CONFIG1_DAISY =  0b10110000
ADS1299_CONFIG1_DAISY_NOT =  0b10010000
LOFF_MAG_6NA =         0b00000000
LOFF_MAG_24NA =        0b00000100
LOFF_MAG_6UA =         0b00001000
LOFF_MAG_24UA =        0b00001100
LOFF_FREQ_DC =         0b00000000
LOFF_FREQ_7p8HZ =      0b00000001
LOFF_FREQ_31p2HZ =     0b00000010
LOFF_FREQ_FS_4 =       0b00000011
CLOCK_EN = 0b10110000



