

# UNTESTED

PREFIX ?= /usr/local


install: $(PREFIX)/bin/netsensor \
	$(PREFIX)/lib/systemd/system/netsensor.service \
	$(PREFIX)/lib/systemd/system/netsensor.timer \
	$(PREFIX)/lib/systemd/system/netsensor-boot.service
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
		$(PREFIX)/etc/netsensor.json \
		$(PREFIX)/lib/systemd/system/netsensor.service \
		$(PREFIX)/lib/systemd/system/netsensor.timer \
		$(PREFIX)/lib/systemd/system/netsensor-boot.service

$(PREFIX)/bin/netsensor: $(PREFIX)/etc/netsensor.json
	cp netsensor.py $(PREFIX)/bin/netsensor

$(PREFIX)/etc/netsensor.json:
	cp netsensor.json $@

$(PREFIX)/lib/systemd/system/netsensor.timer: $(PREFIX)/lib/systemd/system
	cp netsensor.timer $(PREFIX)/lib/systemd/system/

$(PREFIX)/lib/systemd/system/netsensor-boot.service: $(PREFIX)/lib/systemd/system
	cp netsensor-boot.service $(PREFIX)/lib/systemd/system/

$(PREFIX)/lib/systemd/system/netsensor.service: $(PREFIX)/lib/systemd/system
	cp netsensor.service $(PREFIX)/lib/systemd/system/

$(PREFIX)/lib/systemd/system:
	mkdir -p $(PREFIX)/lib/systemd/system
