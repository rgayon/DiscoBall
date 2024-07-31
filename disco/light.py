"""Control the light only via lirc + ir-ctl."""


import subprocess


class Light():
  """The strobe light."""

  BUTTONS = {
      'BLACK_OUT':    '00',
      'AUTO':         '01',
      'SOUND':        '02',
      'STROBE':       '03',
      'SPEED':        '04',
      'SENSITIVITY':  '05',
      'DMX_PCT':      '06',
      'MANUAL':       '07',
      'FADE_UNIT':    '08',
      'RED':          '09',
      'GREEN':        '0A',
      'BLUE':         '0B',
      'AAAA':         '18',
      'UV_P':         '19',
      'WHITE':        '1A',
      'PLUS':         '0C',
      'ZERO':         '0D',
      'MINUS':        '0E',
      'ONE':          '0F',
      'TWO':          '10',
      'THREE':        '11',
      'FOUR':         '12',
      'FIVE':         '13',
      'SIX':          '14',
      'SEVEN':        '15',
      'EIGHT':        '16',
      'NINE':         '17'
  }

  def __init__(self):
    self.address = '0AF1'

  def send_button(self, button):
    if button not in self.BUTTONS:
      raise Exception(f'Unknown button {button}')

    cmd = ['ir-ctl', '-S', 'necx:0x:'+self.address+self.BUTTONS[button]]
    subprocess.run(cmd)

l = Light()
l.send_button('BLACK_OUT')
