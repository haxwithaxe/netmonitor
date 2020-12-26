Th:is is a quick and dirty (to the extent I can tolerate that) network monitor I'm using to alert me when my home internet connection goes down so I can work with my ISP to get my current intermittent outages fixed.

This works by sending a UDP packet to my cloud server. The server logs the time it gets packets that change the up/down state and if it's been more than a specified amount of time since the last `PING` or `BOOT` it sends an email. I'm using my cell provider's email to SMS gateway to get SMS messages when an outage occurs.

# Monitor

`monitor/report.py` outputs a log with outages called out.

```
Report for 1.2.3.4
Entry: Sun Dec 20 14:51:19 2020 up
Entry: Sun Dec 20 15:08:30 2020 down
Entry: Sun Dec 20 15:11:56 2020 up
Outage on Sun Dec 20 15:11:56 2020 lasted 0:03:26.611862 (+/- 30sec)
Entry: Sun Dec 20 16:07:14 2020 down
Ongoing outage on Sun Dec 20 16:07:14 2020 has lasted 0:21:18.922098 (+/- 30sec)
```

It does not distinguish between outages due to reboot (`BOOT` payload) and outages due to anything else.

## Config

The config is a json file consisting of a dictionary with the following keys.
- username - The email address used to authenticate to smtp_server.
- password - The password used to authenticate to smtp_server.
- smtp_server - The domain name of the SMTP server (eg 'smtp.gmail.com').
- smtp_port (integer) - The port number the SMTP server is listening on (probably 587).
- alert_address - The email address to send alerts too.
- client_log_dir - The directory where client logs are stored.
- listen_port (integer) - The port that netmonitor will listen on.
- listen_address - The address netmonitor will listen on (eg 0.0.0.0).
- down_interval - A dictionary of [datetime.timedelta()](https://docs.python.org/3/library/datetime.html#datetime.timedelta) keyword arguments.

### Example
```
{
	"username": "mailbot@example.com",
	"password": "super secret smtp password",
	"smtp_server": "smtp.example.com",
	"smtp_port": 587 ,
	"alert_address": "oncall@example.com",
	"client_log_dir": "/var/log/netmonitor",
	"listen_port": 7777,
	"listen_address": "0.0.0.0",
	"down_interval": {
		"minutes": 3
	}
}
```

# Sensor

There are two types of message the sensor sends.
1. `PING` - This is just a heartbeat telling the monitor the sensor is connected.
1. `BOOT<uptime>` - This tells the monitor that the sensor has just booted up and has a network connection (systemd service dependencies). The uptime is there for the user to see if the sensor was up but couldn't get out for a while.

I included a `BOOT` payload to help weed out outages caused by reboots and power cycling.

## Config

The config is a json file consisting of a dictionary with the following keys.
- server - The IP address or domain name of the netmonitor server.
- port (integer) - The port the netmonitor server is listening on.

### Example
```
{
    "server": "1.2.3.4",
    "port": 7777
}
```

# Warning

This is single threaded. It won't handle many sensor nodes. It almost certainly wouldn't be a good idea to use this in production.

This is unauthenticated so anyone can send a packet every minimum downtime plus 1 second and spam your email.
