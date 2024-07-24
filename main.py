"""Disco things."""

import argparse
import json
import os
import time

from disco import consts as disco_consts

from google.cloud import pubsub_v1
from google.oauth2 import service_account


SCOPES = ['https://www.googleapis.com/auth/pubsub']


class Disco:
  """Main App."""

  def __init__(self, project_id, topic_name, sub_name, creds_file):
    self.project_id = project_id
    self.topic_name = topic_name
    self.sub_name = sub_name
    self.cloud_creds = service_account.Credentials.from_service_account_file(
        creds_file, scopes=SCOPES
    )

  def parse_arguments(self):
    """This is actually the main method."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--action',
        help='Specify the action to perform',
        choices=['push', 'pull'],
        required=True,
    )
    parser.add_argument(
        '--program',
        help='Specify the action to perform',
        choices=disco_consts.DiscoProgram._member_names_,
        default=disco_consts.DiscoProgram.DEFAULT
    )
    args = parser.parse_args()
    if args.action == 'push':
      if args.program:
        self.run_program(args.program)
      else:
        print('Specify a program')
    elif args.action == 'pull':
      self.listen()

  def run_program(self, prog):
    """Initiates a disco program."""

    if prog == disco_consts.DiscoProgram.DEFAULT:
      message = {
          'device': disco_consts.DiscoDevice.BALL,
          'action': disco_consts.DiscoAction.BALL_TURN
      }

      self.publish(message)
      print('sleeping 10 sec')
      time.sleep(10)
      message = {
          'device': disco_consts.DiscoDevice,
          'action': disco_consts.DiscoAction.BALL_STOP
      }

      self.publish(message)

    else:
      print(f'Unknown program {program}')

  def publish(self, message):
    """Publishes a message to the topic."""

    publisher = pubsub_v1.PublisherClient(credentials=self.cloud_creds)
    topic_path = publisher.topic_path(self.project_id, self.topic_name)
    json_message = json.dumps(message, default=str).encode('utf-8')

    future = publisher.publish(topic_path, json_message)

    future.result()
    print(f'Sent message {json_message}')

  def message_callback(self, message):
    """Do the things."""
    print(f'Received message: {message.data}')
    message.ack()

    try:
      msg = json.loads(message.data.decode('utf-8'))
    except json.JSONDecodeError:
      print(f'Can not decode message {message.data}')
      return

    device = msg['device']
    action = msg['action']

    print(class(device))
    if device == disco_consts.DiscoDevice.BALL:
      from disco import ball as disco_ball
      ball = disco_ball.Ball()
      if action == disco_consts.DiscoAction.BALL_STOP:
        ball.stop()
      elif action == disco_consts.DiscoAction.BALL_TURN:
        ball.start()
      else:
        print(f'Unknown action for Ball: {action}')
        return

    elif device == disco_consts.DiscoDevice.LIGHT:
      print('Disco light not implemented yet')
    else:
      print(f'No such device: {device}')

  def listen(self):
    """Pulls messages from the subscription indefinitely."""

    subscriber = pubsub_v1.SubscriberClient(credentials=self.cloud_creds)
    subscription_path = subscriber.subscription_path(
        self.project_id, self.sub_name
    )

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=self.message_callback
    )

    print(f'Listening for messages on {subscription_path}...\n')

    with subscriber:
      try:
        streaming_pull_future.result()
      except KeyboardInterrupt:
        streaming_pull_future.cancel()


def main():

  if not os.path.isfile('config.json'):
    raise Exception('Please setup config.json. Use config.json_template')

  config = json.load(open('config.json'))

  disco_app = Disco(
      config['project_id'],
      config['topic_name'],
      config['sub_name'],
      config['creds_file'])

  disco_app.parse_arguments()

main()
