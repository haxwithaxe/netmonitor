

# UNTESTED

PREFIX ?= /usr/local


install: $(PREFIX)/bin/netsensor \
	$(PREFIX)/etc/systemd/system/netsensor.timer \
	$(PREFIX)/etc/systemd/system/netsensor-boot.service \
	$(PREFIX)/etc/systemd/system/netsensor.service \
	$(PREFIX)/bin/netmonitor-report
	systemctl enable netsensor.timer
	systemctl start netsensor.timer
	systemctl enable netsensor-boot.service
	systemctl start netsensor-boot.service

uninstall:
	systemctl stop netsensor.timer
	systemctl disable netsensor.timer
	systemctl stop netsensor-boot.service
	systemctl disable netsensor-boot.service
	rm $(PREFIX)/bin/netsensor \
		$(PREFIX)/etc/systemd/system/netsensor.timer \
		$(PREFIX)/etc/systemd/system/netsensor-boot.service \
		$(PREFIX)/bin/netmonitor-report

$(PREFIX)/bin/netsensor:
	cp netsensor.py $(PREFIX)/bin/netsensor

$(PREFIX)/etc/systemd/system/netsensor.timer: $(PREFIX)/etc/systemd/system
	cp netsensor.timer $(PREFIX)/etc/systemd/system/

$(PREFIX)/etc/systemd/system/netsensor-boot.service: $(PREFIX)/etc/systemd/system
	cp netsensor-boot.service $(PREFIX)/etc/systemd/system/

$(PREFIX)/etc/systemd/system/netsensor.service: $(PREFIX)/etc/systemd/system
	cp netsensor.service $(PREFIX)/etc/systemd/system/

$(PREFIX)/etc/systemd/system:
	mkdir -p $(PREFIX)/etc/systemd/system
