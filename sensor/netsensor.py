#!/usr/bin/env python3

import argparse
import json
import socket
import sys


def send_ping(server, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(b'PING', (server, port))

def send_boot(server, port):
    with open('/proc/uptime', 'rb') as ut:
        uptime = ut.read()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(b'BOOT'+uptime, (server, port))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=argparse.FileType('r'))
    parser.add_argument('-s', '--server')
    parser.add_argument('-p', '--port', type=int)
    parser.add_argument('--boot', action='store_true', default=False)
    args = parser.parse_args()
    if args.config:
        config = json.load(args.config)
    elif args.server and args.port:
        config = {'server': args.server, 'port': args.port}
    else:
        print('Either --config or both --server and --port must specified.')
        sys.exit(1)
    if args.boot:
        send_boot(config.get('server'), config.get('port'))
    else:
        send_ping(config.get('server'), config.get('port'))
