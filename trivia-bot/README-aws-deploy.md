# Деплой бота в AWS

Инструкция, как задеплоить бота на арендованную машину Amazon Web Services (*AWS*).

## Настройка окружения в AWS

### Запуск и настройка виртуальной машины

1. Запустите виртуальную машину в `EC2` и скачайте пару ключей от нее (далее `key-pair.pem`)
1. Настройка машины
	1. Зайдите на машину с помощью `ssh`: `ssh -i <machine-key-pair> <user>@<address>`. Например `ssh -i "key_pair.pem" ec2-user@ec2-3-15-202-70.us-east-2.compute.amazonaws.com`
	1. Установите [Docker](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html) (раздел *Installing Docker*)
  	1. Установите [Docker Compose](https://docs.docker.com/compose/install/#install-compose-on-linux-systems)
	1. На сайте [AWS](https://aws.amazon.com). Перейдите в раздел `EC2` -> `Security groups`. В `securety group` откройте порт 22 (для подключения через `ssh`), 443(`HTTPS` порт на котором слушает бот) в `Inbound rules`. (пример: `HTTPS	TCP	443	0.0.0.0/0`)

### Настройка ECR

На сайте [AWS](https://aws.amazon.com). Перейдите в `Elastic Container Registry` (`ECR`) и создайте репозиторий

## Настройка локальной машины для деплоя

1. Установите  [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html)

1. Настройте `aws credentials` [configuration aws credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)( раздел `Configuration and credential file settings`)
	1. Получите ключ
	1. Запустите `aws configure`  и введите полученный ключи [Security Credentials](https://console.aws.amazon.com/iam/home?region=us-east-2#/security_credentials>)

## Деплой

### По необходимости:

1.  Получите https сертификат для бота [Certificate](https://stackoverflow.com/questions/10175812/how-to-generate-a-self-signed-ssl-certificate-using-openssl)
	1. Обязательно нужно поставить `-subj '/CN=localhost`. Обратите внимение, что `CN` должен совпадать с `DNS` именем вашей `aws` машины
	(пример	`openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=ec2-3-15-202-70.us-east-2.compute.amazonaws.com'`)
	1. Скопируйте `key.pem` и `cert.pem` на `aws-машину`: `scp -i <path/to/key-pair.pem> path/to/key.pem <user>@<machine>:~/`(пример `ssh -i "/home/vambat/Downloads/trivia_bot_key_pair.pem" key.pem ec2-user@ec2-3-15-202-70.us-east-2.compute.amazonaws.com `). 
	1.  Оба шага должны выпоняться в случае, если сертификата на `aws` машине еще нет или его нужно обновить.

1. Скопируйте необходимые файлы на `aws-машину`
	1. Перейдити в репозиторий бота `/bots/trivia-bot`. В текущей директории
		1. Создайте файл переменных окружений на основе`bot-sample.env`
			1. Выполните команду: `cp bot-sample.env bot.env`
			1. Заполните `bot.env`
	1. Скопируйте `bot.env` и `docker-compose-aws.yml` :`scp -i <path/to/key-pair.pem> path/to/bot.env <user>@<machine>:~/` (пример: `ssh -i "/home/vambat/Downloads/trivia_bot_key_pair.pem" bot.env ec2-user@ec2-3-15-202-70.us-east-2.compute.amazonaws.com:~/`)
	1. Скопируйте файл с вопросами на `aws-машину`: `scp -i <path/to/key-pair.pem> path/to/questions.json <user>@<machine>:~/`
	(пример: `scp -i "/home/vambat/Downloads/trivia_bot_key_pair.pem" questions.json ec2-user@ec2-3-15-202-70.us-east-2.compute.amazonaws.com:~/`)	

### Каждый деплой:

1. [Загрузите контейнер бота в ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-pull-ecr-image.html)
	1. Выполните аутентификацию `Docker` в частном реестре `Amazon ECR` [Docker authentication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html): `aws ecr get-login-password --region region | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com` 
	(пример: `aws ecr get-login-password --region us-east-2 | docker login username AWS --password-stdin 111663367461.dkr.ecr.us-east-2.amazonaws.com`)
	Она выдается на 12 часов.

	1. Перейдите в `bots/trivia-bot`, создайте `Docker` образ: `docker build -t trivia_bot .`

	1. Пометьте образ, чтобы его можно было отправить в созданный ранее репозиторий: `docker tag <image id> aws_account_id.dkr.ecr.region.amazonaws.com` (пример: `docker tag 61fa9099c9e3 111663367461.dkr.ecr.us-east-2.amazonaws.com/trivia_bot`)

	1. Отправьте полученный образ в `ECR`: `docker push aws_account_id.dkr.ecr.region.amazonaws.com` (пример: `docker push 111663367461.dkr.ecr.us-east-2.amazonaws.com/trivia_bot`)


1. Запустите контейнер на `AWS` машине
	1. Выполните аутентификацию `Docker` в [Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html): `aws ecr get-login --region region --no-include-email`(пример: `aws ecr get-login --region us-east-2 --no-include-email`). Затем полученный ключ скопируйте и введите в консоль, и нажмите `Enter`. Аутентификация выдается на 12 часов.
	1. Загрузите на машину: `docker pull aws_account_id.dkr.ecr.us-west-2.amazonaws.com/amazonlinux:latest` (пример `docker pull 111663367461.dkr.ecr.us-east-2.amazonaws.com/trivia_bot:latest`)
	1. Запустите бота, выполнив команду: `docker-compose -f docker-compose-aws.yml up`
	1. Проверить, что бот работает:
		- при запуске `docker-compose` не должно быть ошибок
		- отправьте сообщение боту в `Telegram`, бот должен ответить
