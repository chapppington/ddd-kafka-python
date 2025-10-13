APP_CONTAINER = main-app
APP_FILE = docker_compose/app.yaml
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


# чтобы добавить это перед коммитом надо его установить
# poetry add pre-commit --group dev
# и запустить
# pre-commit install
# и будет он срабатывать перед каждым коммитом
# но можно и просто запустить make precommit
.PHONY: precommit 
precommit:
	pre-commit run --all-files
