"""Bunch of things"""

import enum


class DiscoError(Exception):
  """DiscoError."""


class DiscoDevice(enum.IntEnum):
  BALL = 1
  LIGHT = 2


class DiscoAction(enum.IntEnum):
  """Disco actions."""

  BALL_STOP = 1
  BALL_TURN = 2


class DiscoProgram(enum.IntEnum):
  """Disco programs."""

  NOTHING = 1
  DEFAULT = 2
