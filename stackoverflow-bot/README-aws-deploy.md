# Деплой бота в AWS

Инструкция, как задеплоить бота на арендованную машину Amazon Web Services (*AWS*).

## Настройка окружения в AWS

### [Запуск и настройка виртуальной машины](../trivia-bot/README-aws-deploy.md#запуск-и-настройка-виртуальной-машины) перейдите по ссылке и выполните все пункты

### Настройка ECR

На сайте [AWS](https://aws.amazon.com). Перейдите в `Elastic Container Registry` (`ECR`) и создайте репозиторий

## [Настройка локальной машины для деплоя](../trivia-bot/README-aws-deploy.md#настройка-локальной-машины-для-деплоя) перейдите по ссылке и выполните все пункты

## Деплой

1. [Загрузите контейнер бота в ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-pull-ecr-image.html)
	1. Выполните аутентификацию `Docker` в частном реестре `Amazon ECR` [Docker authentication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html)
	(пример: `aws ecr get-login-password --region us-east-2 | docker login username AWS --password-stdin 111663367461.dkr.ecr.us-east-2.amazonaws.com`)
	Она выдается на 12 часов.

	1. Перейдите в `/bots/stackoverflow-bot`, создайте `Docker` образ (пример `docker build -t stackoverflow_bot .`)

	1. Пометьте образ, чтобы его можно было отправить в созданный ранее репозиторий: `docker tag <image id> aws_account_id.dkr.ecr.region.amazonaws.com` (пример: `docker tag 61fa9099c9e3 111663367461.dkr.ecr.us-east-2.amazonaws.com/stackoverflow_bot`)

	1. Отправьте полученный образ на `aws-машину`: `docker push aws_account_id.dkr.ecr.region.amazonaws.com` (пример: `docker push 111663367461.dkr.ecr.us-east-2.amazonaws.com/stackoverflow_bot`)


1. Запустите контейнер на `AWS` машине
	1. Выполните аутентификацию `Docker` в частном реестре `Amazon ECR`[Docker authentication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html): `aws ecr get-login --region <ваш регион, где регистрировались> --no-include-email`(пример: `aws ecr get-login --region us-east-2 --no-include-email`). Затем полученный ключ скопируйте и введите в консоль, и нажмите `Enter`. Аутентификация выдается на 12 часов.
	1. Выполните команду: `docker pull aws_account_id.dkr.ecr.us-west-2.amazonaws.com/amazonlinux:latest` (пример `docker pull 111663367461.dkr.ecr.us-east-2.amazonaws.com/stackoverflow_bot:latest`)
	1. Запустите бота. Выполнив команду: `docker run --name so-bot --env BOT_TOKEN=<телеграм токен> 111663367461.dkr.ecr.us-east-2.amazonaws.com/stackoverflow_bot python bot.py`
	1. Проверить, что бот работает. Отправьте сообщение боту в `Telegram`, бот должен ответить