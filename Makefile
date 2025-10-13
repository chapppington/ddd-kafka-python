APP_CONTAINER = main-app
APP_FILE = docker/app.yaml
DC = docker compose
ENV_FILE = --env-file .env # это уже вместе с командой (все норм, не трогай)
EXEC = docker exec -it
LOGS = docker logs


.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV_FILE} up  --build -d

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} ash


.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down
