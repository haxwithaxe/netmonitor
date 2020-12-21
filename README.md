This is a quick and dirty (to the extent I can tolerate that) network monitor I'm using to alert me when my home internet connection goes down so I can work with my ISP to get my current intermittent outages fixed.

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

# Sensor

There are two types of message the sensor sends.
1. `PING` - This is just a heartbeat telling the monitor the sensor is connected.
1. `BOOT<uptime>` - This tells the monitor that the sensor has just booted up and has a network connection (systemd service dependencies). The uptime is there for the user to see if the sensor was up but couldn't get out for a while.

I included a `BOOT` payload to help weed out outages caused by reboots and power cycling.

# Warning
This is single threaded. It won't handle many sensor nodes. It almost certainly wouldn't be a good idea to use this in production.
