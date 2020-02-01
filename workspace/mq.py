
from esp32ap import *
from umqtt.simple import MQTTClient
import time

import esp
esp.osdebug(None)

def main():
  ap = Esp32Ap()
  while not ap.isconnected():
    time.sleep(0.5)
  c = MQTTClient("esp32_mqtt", "192.168.66.2",keepalive = 600)
  c.connect()
  for i in range(100):
    c.publish("esp32topic", str(i))
    print(str(i))
    time.sleep(1)
  c.disconnect()

if __name__ == '__main__':
    main()









