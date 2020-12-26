

# UNTESTED

PREFIX ?= /usr/local


install: $(PREFIX)/bin/netmonitor \
	$(PREFIX)/lib/systemd/system/netmonitor.service \
	$(PREFIX)/bin/netmonitor-report
	systemctl enable netmonitor.service
	systemctl start netmonitor.service

uninstall:
	systemctl stop netmonitor.service
	systemctl disable netmonitor.service
	rm $(PREFIX)/bin/netmonitor \
		$(PREFIX)/etc/netmonitor.json \
		$(PREFIX)/lib/systemd/system/netmonitor.service \
		$(PREFIX)/bin/netmonitor-report

$(PREFIX)/bin/netmonitor: $(PREFIX)/etc/netmonitor.json
	cp netmonitor.py $(PREFIX)/bin/netmonitor

$(PREFIX)/etc/netmonitor.json:
	cp netmonitor.json $@

$(PREFIX)/lib/systemd/system/netmonitor.service: $(PREFIX)/lib/systemd/system
	cp netmonitor.service $(PREFIX)/lib/systemd/system/

$(PREFIX)/bin/netmonitor-report:
	cp report.py $(PREFIX)/bin/netmonitor-report

$(PREFIX)/lib/systemd/system:
	mkdir -p $(PREFIX)/lib/systemd/system
