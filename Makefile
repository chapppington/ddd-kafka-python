APP_CONTAINER = main-app
STORAGES_CONTAINER = chat-mongodb
APP_FILE = docker_compose/app.yaml
STORAGES_FILE = docker_compose/storages.yaml
MESSAGING_FILE = docker_compose/messaging.yaml
MESSAGING_CONTAINER = main-kafka
DC = docker compose
ENV_FILE = --env-file .env # это уже вместе с командой (все норм, не трогай)
EXEC = docker exec -it
LOGS = docker logs

.PHONY: all
all:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} -f ${MESSAGING_FILE} ${ENV_FILE} up --build -d

.PHONY: all-down
all-down:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} -f ${MESSAGING_FILE} ${ENV_FILE} down

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV_FILE} up  --build -d

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: storages-logs
storages-logs:
	${LOGS} ${STORAGES_CONTAINER} -f

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV_FILE} up  --build -d

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash


.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down


.PHONY: messaging
messaging:
	${DC} -f ${MESSAGING_FILE} ${ENV_FILE} up  --build -d

.PHONY: messaging-down
messaging-down:
	${DC} -f ${MESSAGING_FILE} down

.PHONY: messaging-logs
messaging-logs:
	${DC} -f ${MESSAGING_FILE} logs -f


# чтобы добавить это перед коммитом надо его установить
# poetry add pre-commit --group dev
# и запустить
# pre-commit install
# и будет он срабатывать перед каждым коммитом
# но можно и просто запустить make precommit
.PHONY: precommit 
precommit:
	pre-commit run --all-files

.PHONY: test
test:
	pytest -v