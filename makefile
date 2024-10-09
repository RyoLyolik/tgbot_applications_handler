ENVIRONMENT ?= development

up:
ifeq ($(ENVIRONMENT), production)
	@echo "Running in production..."
	-docker compose down
	-docker stop bot
	-docker stop redis
	-docker rm bot
	-docker rm redis
	export tgbot_application_redis_image="ryoly0/tg_bot_application_redis:latest" && \
	export tgbot_application_image="ryoly0/tg_bot_application:latest" && \
	docker compose up -d --build
else
	@echo "Running in development..."
	-docker compose down
	-docker stop bot
	-docker stop redis
	-docker rm bot
	-docker rm redis
	docker build ./redis --tag tg_bot_application_redis:latest
	docker build ./src --tag tg_bot_application:latest
	export tgbot_application_redis_image="tg_bot_application_redis:latest" && \
	export tgbot_application_image="tg_bot_application:latest" && \
	docker compose up -d --build
endif

down:
	docker compose down
