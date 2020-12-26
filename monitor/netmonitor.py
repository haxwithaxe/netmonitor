#!/usr/bin/env python3

import argparse
import datetime
import json
import re
import os
import smtplib
import socket
import ssl


SOCKET_TIMEOUT = 1  # Seconds
DOWN = 'down'
UP = 'up'

MSG_FORMAT = '''Subject: Network Outage\r
From: {username}\r
To: {alert_address}\r
Content-Type: text/plain; charset="ASCII"\r
{msg}'''


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def send_email(msg, config):
    msg = MSG_FORMAT.format(msg=msg, **config)
    tls_context = ssl.create_default_context()
    with smtplib.SMTP(config.get('smtp_server'),
                      config.get('smtp_port')) as server:
        server.ehlo()
        server.starttls(context=tls_context)
        server.ehlo()
        server.login(config.get('username'), config.get('password'))
        print('sending mail to:', config.get('alert_address'), 'message:', msg, '...', end='')
        server.sendmail(config.get('username'), config.get('alert_address'), msg.encode('ascii'))
        print('done')


class Client:

    def __init__(self, ip, config):
        self.ip = ip
        self.config = config
        self.state = DOWN
        self.last_up = now()
        self.alerted = False

    @property
    def is_down(self):
        return now() - self.last_up > datetime.timedelta(**self.config.get('down_interval'))

    def up(self):
        if self.state == DOWN:
            self.state = UP
            self.last_up = now()
            self.log()
        else:
            self.state = UP
            self.last_up = now()
        self.alerted = False
    
    def boot(self, uptime):
        self.state = UP
        self.last_up = now()
        self.alerted = False
        self.log(uptime)

    def down(self):
        if self.state == UP:
            self.state = DOWN
            self.log()

    def log(self, uptime=None):
        log_filename = os.path.join(self.config.get('client_log_dir'), '{}.json'.format(self.ip))
        if os.path.exists(log_filename):
            log = json.load(open(log_filename, 'r'))
        else:
            log = []
        line = {'state': self.state, 'last_up': self.last_up.timestamp(), 'now': now().timestamp()}
        if uptime:
            line['uptime'] = uptime
        print(line)
        log.append(line)
        json.dump(log, open(log_filename, 'w'))


class Server:
    """

    Message Format:
    client: PING|BOOT<uptime>
    """

    def __init__(self, config_file):
        self.config = json.load(config_file)
        self.address = config.get('listen_address')
        self.port = config.get('listen_port')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(SOCKET_TIMEOUT)
        self._clients = {}

    def read(self):
        buf = b''
        while b'PING' not in buf and b'BOOT' not in buf:
            data, src = self.sock.recvfrom(64)
            if data:
                buf += data
        return src, str(buf)

    def serve_forever(self):
        self.sock.bind((self.address, self.port))
        while True:
            try:
                client, msg = self.read()
                client_ip, _ = client
                if client_ip not in self._clients:
                    self._clients[client_ip] = Client(client_ip, self.config)
                if 'PING' in msg:
                    self._clients[client_ip].up()
                if 'BOOT' in msg:
                    match = re.match(r'BOOT(\d+)', msg)
                    if match:
                        self._clients[client_ip].boot(match.groups()[0])
                    else:
                        self._clients[client_ip].up()
            except socket.timeout:
                pass
            for c in self._clients.values():
                if c.is_down:
                    c.down()
                    self.alert(c)

    def alert(self, client):
        if client.alerted:
            return
        client.alerted = True
        send_email(
            '{} is down. {}'.format(
                client.ip, 
                client.last_up.strftime('%Y/%m/%d %H.%M %z')
                ),
            self.config
            )



def main(config_file):
    Server(config_file).serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=argparse.FileType('r'), required=True)
    args = parser.parse_args()
    main(args.listen, args.port, args.config)
