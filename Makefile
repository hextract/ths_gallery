.PHONY: pull
pull:
	git pull

.PHONY: update
update: pull
	sudo systemctl restart gunicorn