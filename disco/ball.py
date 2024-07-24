"""Sets up the radio."""

import rpi_rf


class Ball():
  """Class to talk to a 433Mhz controlled motored disco ball."""

  STOP_CODE = 13281798
  START_CODE = 13281786

  GPIO = 17
  REPEAT = 5
  PULSE_LENGTH = 390
  PROTOCOL = 'default'
  LENGTH = 'default'

  def __init__(self):
    self.rf = rpi_rf.RFDevice(self.GPIO)
    self.rf.enable_tx()
    self.rf.tx_repeat = self.REPEAT

  def _send_code(self, code):
    self.rf.tx_code(code, self.PROTOCOL, self.PULSE_LENGTH, self.LENGTH)
    self.rf.cleanup()

  def start(self):
    self._send_code(self.START_CODE)

  def stop(self):
    self._send_code(self.STOP_CODE)
