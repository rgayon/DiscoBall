"""Control the light only via Python. Does not work"""

import logging
import sys
import time

from RPi import GPIO

class Formatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            # support %z and %f in datefmt (struct_time doesn't carry ms or tz)
            datefmt = datefmt.replace("%f", "%03d" % int(record.msecs))
            datefmt = datefmt.replace('%z', time.strftime('%z'))
            s = time.strftime(datefmt, ct)
        else:
            t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
            s = "%s,%03d" % (t, record.msecs)
        return s


class Light():
  """a Light."""

  def __init__(self, pin):
    raise Exception('Do not use this')
    self.pin = pin

    self.freq = 38000
    self.burst_length_usec = 560
    self.one_length_usec = 2250
    self.zero_length_usec = 1125
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(Formatter("%(asctime)s %(message)s", "%a, %d %b %Y %H:%M:%S.%f %z"))
    self.l = logging.getLogger(__name__)
    self.l.setLevel(logging.INFO)
    self.l.addHandler(console)

#    self.tot_slept = 0

  def _setup(self):
#    self.l.info('setup')
    pass
#    GPIO.setmode(GPIO.BCM)
#    GPIO.setup(self.pin, GPIO.OUT)

  def _cleanup(self):
    # set up GPIO pin as input for safety
    pass
#    GPIO.setup(self.pin, GPIO.IN)

  def _usleep(self, microsecs):
#    self.l.info(f'sleep for {microsecs}')
    time.sleep(microsecs/1000000.0)
#    self.tot_slept += microsecs

  def _send_burst(self, duration_usec=None, duty_cycle=33):

    if not duration_usec:
      duration_usec = self.burst_length_usec

    self.l.info(f'sending a burst for {duration_usec}')
    pulse_length_usec = (1.0/self.freq) * 1000000

    for _ in range(0, int(duration_usec/pulse_length_usec)):
#      GPIO.output(self.pin, GPIO.HIGH)
      self._usleep(pulse_length_usec * (duty_cycle/100.0))
#      GPIO.output(self.pin, GPIO.LOW)
      self._usleep(pulse_length_usec * ((100-duty_cycle) / 100.0))

  def _send_one(self):
    self.l.info("sending a one")
    self._send_burst()
    self.l.info(f'sleeping for {self.one_length_usec - self.burst_length_usec}')
    self._usleep(self.one_length_usec - self.burst_length_usec)

  def _send_zero(self):
    self.l.info("sending a zero")
    self._send_burst()
    self.l.info(f'sleeping for {self.zero_length_usec - self.burst_length_usec}')
    self._usleep(self.zero_length_usec - self.burst_length_usec)

  def _send_sync(self):
    self.l.info("sending AGC")
    self._send_burst(9000)
    self.l.info("sleeping for 4500")
    self._usleep(4500)

  def send_byte(self, byte):
    self.l.info(f"sending byte {byte}")

    for b in reversed('{:08b}'.format(byte)):
      if b == '1':
#        print('send one')
        self._send_one()
      else:
#        print('send zero')
        self._send_zero()

  def send_msg_extended(self, address, command):
#    self.l.info('about to send burst')
    self._setup()
    self._send_sync()
#    self.l.info('sent burst')

    addr_low = address & 0xFF
    addr_high = (address >> 8) & 0xFF

    self.send_byte(addr_low)
    self.send_byte(addr_high)

    self.send_byte(command)
    self.send_byte(0xff ^ command)

    self._send_burst()
    self._cleanup()


l = Light(27)
l.send_msg_extended(0xea41, 0x48)
