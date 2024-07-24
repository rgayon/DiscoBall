"""Disco things."""

import argparse
import json

from disco import consts as disco_consts
from disco import ball as disco_ball

from google.cloud import pubsub_v1
from google.oauth2 import service_account

PROJECT_ID = 'yellow-place-disco-ball'
TOPIC_NAME = 'ypdb'
SUBSCRIPTION_NAME = 'ypdb-sub'

SCOPES = ['https://www.googleapis.com/auth/pubsub']


def pub(creds_file, message):
  """Publishes a message to the topic."""
  creds = service_account.Credentials.from_service_account_file(
      creds_file, scopes=SCOPES
  )

  publisher = pubsub_v1.PublisherClient(credentials=creds)
  topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
  json_message = json.dumps(message).encode('utf-8')
  future = publisher.publish(topic_path, json_message)
  future.result()


def message_callback(message):
  """Do the things."""
  print(f'Received message: {message.data}')
  message.ack()
  message_callback(message)

  msg = json.loads(message.data.decode('utf-8'))

  device = msg['device']

  action = msg['action']

  if device == disco_consts.DiscoDevice.BALL:
    ball = ball.Ball()
    if action == disco_consts.DiscoAction.BALL_STOP:
      ball.stop()
    elif action == disco_consts.DiscoAction.BALL_TURN:
      ball.turn()
    else:
      print(f'Unknown action for Ball: {action}')

  elif device == disco_consts.DiscoDevice.LIGHT:
    print('Disco light not implemented yet')
  else:
    print(f'No such device: {device}')


def pull(creds_file):
  """Pulls messages from the subscription indefinitely."""

  creds = service_account.Credentials.from_service_account_file(
      creds_file, scopes=SCOPES
  )
  subscriber = pubsub_v1.SubscriberClient(credentials=creds)
  subscription_path = subscriber.subscription_path(
      PROJECT_ID, SUBSCRIPTION_NAME
  )

  streaming_pull_future = subscriber.subscribe(
      subscription_path, callback=message_callback
  )

  print(f'Listening for messages on {subscription_path}...\n')

  with subscriber:
    try:
      streaming_pull_future.result()
    except KeyboardInterrupt:
      streaming_pull_future.cancel()


def main():

  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--creds', help='Specify the credentials file.json', required=True
  )
  parser.add_argument(
      '--action',
      help='Specify the action to perform',
      choices=['push', 'pull'],
      required=True,
  )
  parser.add_argument(
      '--program',
      help='Specify the action to perform',
      choices=disco_consts.DiscoProgram._member_names_
  )
  args = parser.parse_args()

  if args.action == 'push':
    if args.program:
      pub(args.creds, args.program)
    else:
      print('Specify a program')
  elif args.action == 'pull':
    pull(args.creds)

