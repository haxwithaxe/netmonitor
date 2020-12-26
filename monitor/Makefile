

# UNTESTED

PREFIX ?= /usr/local


install: $(PREFIX)/bin/netmonitor $(PREFIX)/etc/systemd/system/netmonitor.service $(PREFIX)/bin/netmonitor-report
	systemctl enable netmonitor.service
	systemctl start netmonitor.service

uninstall:
	systemctl stop netmonitor.service
	systemctl disable netmonitor.service
	rm $(PREFIX)/bin/netmonitor $(PREFIX)/etc/systemd/system/netmonitor.service $(PREFIX)/bin/netmonitor-report

$(PREFIX)/bin/netmonitor:
	cp netmonitor.py $(PREFIX)/bin/netmonitor

$(PREFIX)/etc/systemd/system/netmonitor.service: $(PREFIX)/etc/systemd/system
	cp netmonitor.service $(PREFIX)/etc/systemd/system/

$(PREFIX)/bin/netmonitor-report:
	cp report.py $(PREFIX)/bin/netmonitor-report

$(PREFIX)/etc/systemd/system:
	mkdir -p $(PREFIX)/etc/systemd/system
