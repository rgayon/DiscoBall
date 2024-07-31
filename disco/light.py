"""Control the light"""

import time

import RPi.GPIO as GPIO


class Light():
  """a Light."""

  def __init__(self, pin):
    self.pin = pin

    self.freq = 38000
    self.burst_length_usec = 560
    self.one_length_usec = 2250
    self.zero_length_usec = 1125

  def _setup(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.pin, GPIO.OUT)

  def _cleanup(self):
    # set up GPIO pin as input for safety
    GPIO.setup(self.pin, GPIO.IN)

  def _usleep(self, microsecs):
    time.sleep(microsecs/1000000.0)

  def _send_burst(self, duration_usec=None):

    if not duration_usec:
      duration_usec = self.burst_length_usec

    pulse_length_usec = (1.0/self.freq) * 1000000

    for _ in range(0, int(duration_usec/pulse_length_usec)):
      GPIO.output(self.pin, GPIO.HIGH)
      self.usleep(pulse_length_usec)
      GPIO.output(self.pin, GPIO.LOW)
      self.usleep(pulse_length_usec)

  def _send_one(self):
    self.send_burst()
    self.usleep(self.one_length_usec - self.burst_length_usec)

  def _send_zero(self):
    self.send_burst()
    self.usleep(self.zero_length_usec - self.burst_length_usec)

  def _send_sync(self):
#    print("send sync")
    self._send_burst(9000)
    self._usleep(4500)

  def send_byte(self, byte):
#    print(f"sending byte {byte}")

    for b in reversed('{:08b}'.format(byte)):
      if b == '1':
#        print('send one')
        self._send_one()
      else:
#        print('send zero')
        self._send_zero()

  def send_msg_extended(self, address, command):
    self._setup()
    self._send_sync()

    addr_low = address & 0xFF
    addr_high = (address >> 8) & 0xFF

    self.send_byte(addr_low)
    self.send_byte(addr_high)

    self.send_byte(command)
    self.send_byte(0xff ^ command)

    self._cleanup()


l = Light(27)
l.send_msg_extended(0xea41, 0x48)
