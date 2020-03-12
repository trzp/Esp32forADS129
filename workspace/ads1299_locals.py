#coding:utf-8
#author:mrtang
#date:2020.1.7

BYTESMAP = [
    b'\x00', b'\x01', b'\x02', b'\x03', b'\x04', b'\x05', b'\x06', b'\x07', b'\x08', 
    b'\t', b'\n', b'\x0b', b'\x0c', b'\r', b'\x0e', b'\x0f', b'\x10', b'\x11', b'\x12',
    b'\x13', b'\x14', b'\x15', b'\x16', b'\x17', b'\x18', b'\x19', b'\x1a', b'\x1b',
    b'\x1c', b'\x1d', b'\x1e', b'\x1f', b' ', b'!', b'"', b'#', b'$', b'%', b'&', b"'",
    b'(', b')', b'*', b'+', b',', b'-', b'.', b'/', b'0', b'1', b'2', b'3', b'4', b'5',
    b'6', b'7', b'8', b'9', b':', b';', b'<', b'=', b'>', b'?', b'@', b'A', b'B', b'C',
    b'D', b'E', b'F', b'G', b'H', b'I', b'J', b'K', b'L', b'M', b'N', b'O', b'P', b'Q',
    b'R', b'S', b'T', b'U', b'V', b'W', b'X', b'Y', b'Z', b'[', b'\\', b']', b'^', b'_',
    b'`', b'a', b'b', b'c', b'd', b'e', b'f', b'g', b'h', b'i', b'j', b'k', b'l', b'm',
    b'n', b'o', b'p', b'q', b'r', b's', b't', b'u', b'v', b'w', b'x', b'y', b'z', b'{',
    b'|', b'}', b'~', b'\x7f', b'\x80', b'\x81', b'\x82', b'\x83', b'\x84', b'\x85',
    b'\x86', b'\x87', b'\x88', b'\x89', b'\x8a', b'\x8b', b'\x8c', b'\x8d', b'\x8e',
    b'\x8f', b'\x90', b'\x91', b'\x92', b'\x93', b'\x94', b'\x95', b'\x96', b'\x97',
    b'\x98', b'\x99', b'\x9a', b'\x9b', b'\x9c', b'\x9d', b'\x9e', b'\x9f', b'\xa0',
    b'\xa1', b'\xa2', b'\xa3', b'\xa4', b'\xa5', b'\xa6', b'\xa7', b'\xa8', b'\xa9',
    b'\xaa', b'\xab', b'\xac', b'\xad', b'\xae', b'\xaf', b'\xb0', b'\xb1', b'\xb2',
    b'\xb3', b'\xb4', b'\xb5', b'\xb6', b'\xb7', b'\xb8', b'\xb9', b'\xba', b'\xbb',
    b'\xbc', b'\xbd', b'\xbe', b'\xbf', b'\xc0', b'\xc1', b'\xc2', b'\xc3', b'\xc4',
    b'\xc5', b'\xc6', b'\xc7', b'\xc8', b'\xc9', b'\xca', b'\xcb', b'\xcc', b'\xcd',
    b'\xce', b'\xcf', b'\xd0', b'\xd1', b'\xd2', b'\xd3', b'\xd4', b'\xd5', b'\xd6',
    b'\xd7', b'\xd8', b'\xd9', b'\xda', b'\xdb', b'\xdc', b'\xdd', b'\xde', b'\xdf',
    b'\xe0', b'\xe1', b'\xe2', b'\xe3', b'\xe4', b'\xe5', b'\xe6', b'\xe7', b'\xe8',
    b'\xe9', b'\xea', b'\xeb', b'\xec', b'\xed', b'\xee', b'\xef', b'\xf0', b'\xf1',
    b'\xf2', b'\xf3', b'\xf4', b'\xf5', b'\xf6', b'\xf7', b'\xf8', b'\xf9', b'\xfa',
    b'\xfb', b'\xfc', b'\xfd', b'\xfe', b'\xff']


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
  '\xf0', '\xf1', '\xf2', '\xf3', '\xf4', '\xf5', '\xf6', '\xf7', '\xf8', '\xf9', '\xfa', '\xfb', '\xfc', '\xfd', '\xfe', '\xff']

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




