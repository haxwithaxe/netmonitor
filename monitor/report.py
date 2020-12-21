#!/usr/bin/env python3

import argparse
import datetime
import json
import os

import yaml


DOWN = 'down'
UP = 'up'


def report(log):
    down_since = None
    last_up = None
    for line in log:
        last_up = datetime.datetime.fromtimestamp(line.get('last_up'),
                                         datetime.timezone.utc)
        print('Entry:', last_up.ctime(), line.get('state'))
        if line.get('state') == UP and down_since:
            print(
                    'Outage on {} lasted {} (+/- 30sec)'.format(
                        last_up.ctime(),
                        last_up - down_since
                    )
                )
            down_since = None
        if line.get('state') == DOWN:
            down_since = last_up
    if down_since and last_up:
        print(
                'Ongoing outage on {} has lasted {} (+/- 30sec)'.format(
                    last_up.ctime(),
                     datetime.datetime.now(datetime.timezone.utc)- down_since
                )
            )


def main(config_file):
    log_dir = yaml.load(config_file, yaml.Loader).get('client_log_dir')
    for log_file in os.listdir(log_dir):
        with open(os.path.join(log_dir, log_file), 'r') as log:
            print('Report for', os.path.splitext(log_file)[0])
            report(json.load(log))
            print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=argparse.FileType('r'), required=True)
    args = parser.parse_args()
    main(args.config)
