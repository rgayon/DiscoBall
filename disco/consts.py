"""Bunch of things"""

import enum


class DiscoError(Exception):
  """DiscoError."""


class DiscoDevice(enum.Enum):
  BALL = 'ball'
  LIGHT = 'light'


class DiscoAction(enum.Enum):
  """Disco actions."""

  BALL_STOP = 'ballstop'
  BALL_TURN = 'ballmove'


class DiscoProgram(enum.Enum):
  """Disco programs."""

  DEFAULT = 'default'
