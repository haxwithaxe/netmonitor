#!/usr/bin/env python3

import argparse
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
    parser.add_argument('-s', '--server', required=True)
    parser.add_argument('-p', '--port', type=int, required=True)
    parser.add_argument('--boot', action='store_true', default=False)
    args = parser.parse_args()
    if args.boot:
        send_boot(args.server, args.port)
    else:
        send_ping(args.server, args.port)
