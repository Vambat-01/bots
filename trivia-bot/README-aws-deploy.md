# Деплой бота в AWS

Инструкция, как задеплоить бота на арендованной машине Amazon Web Services (*AWS*).

## Настройка окружения в AWS

### Запуск и настройка виртуальной машины

1. Запустите виртуальную машину в `EC2` и скачайте пару ключей от нее (далее `key-pair.pem`)
1. Настройка машины
	1. Зайдите на машину с помощью `ssh`: `ssh -i <machine-key-pair> <user>@<address>`. Например `ssh -i "key_pair.pem" ec2-user@ec2-3-15-202-70.us-east-2.compute.amazonaws.com`
	1. Установите [Docker](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html) (раздел *Installing Docker*)
  	1. Установите [Docker Compose](https://docs.docker.com/compose/install/#install-compose-on-linux-systems)


### Настройка ECR

На сайте [AWS](https://aws.amazon.com)
1. Перейдите в `Elastic Container Registry` (`ECR`) создайте репозиторий, выберите его и нажмите на `View push commands` (выполните все команды)

1. Перейдите в раздел `EC2` -> `Security groups`. В `securety group` откройте порт 22, 443 в `Inbound rules`. (пример `HTTPS	TCP	443	0.0.0.0/0`)

## Настройка локальной машины для деплоя
1.Установите  [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html)

1. Настройте `aws credentials` [configuration aws credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)( раздел `Configuration and credential file settings`)
	1. `aws configure`  и введите ключи [Security Credentials](https://console.aws.amazon.com/iam/home?region=us-east-2#/security_credentials>),  тут получите ключ

1.  Получите сертификат [Certificate](https://stackoverflow.com/questions/10175812/how-to-generate-a-self-signed-ssl-certificate-using-openssl)
	1. Обязательно нужно поставить `-subj '/CN=localhost`. Обратите внимение `CN` должен совпадать с `DNS` именем вашей `aws-машины`
	(пример	`openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=ec2-3-15-202-70.us-east-2.compute.amazonaws.com'`)
	1. Скопируйте `key.pem` и `cert.pem` на `aws-машину`. Перейдите в папку куда они скачались и выполнить командy, (пример	`scp -i <путь к файлу key-pair> <файл, который хотите скопировать> ec2-user@ec2-3-15-202-70.us-east-2.compute.amazonaws.com:~/`). Если, сертификат уже создан, в дальнейшем можно это пропустить.

## Деплой

1. Скопируйте необходимые файлы на `aws-машину`
	1. Перейдити в репозиторий бота `bots` -> `trivia-bot`. В текущей директории
		1. В файле `bot.env` исправьте значение `SERVER_URL` на ваше. Пример `SERVER_URL=https://ec2-3-15-202-70.us-east-2.compute.amazonaws.com`
	1. Скопируйте `bot.env` и `docker-compose-aws.yml` (пример `scp -i <путь к файлу key-pair.pem> <файл, который хотите скопировать> ec2-user@ec2-3-15-202-70.us-east-2.compute.amazonaws.com:~/`)
	- Скопируйте ваш `json` файл на `aws-машину`. Пример файла, можно найти перейдя `bots` -> `trivia-bot` -> `resources` -> `bot_questions_mini.json`
	(пример `scp -i <путь к файлу key-pair.pem> <файл, который хотите скопировать> ec2-user@ec2-3-15-202-70.us-east-2.compute.amazonaws.com:~/`)
1. [Загрузите контейнер бота в ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-pull-ecr-image.html)
	1. Выполните аутентификацию `Docker` в частном реестре `Amazon ECR` [Docker authentication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html)
	(пример `aws ecr get-login-password --region us-east-2 | docker login username AWS --password-stdin 111663367461.dkr.ecr.us-east-2.amazonaws.com`)
	Она выдается на 12 часов.

	1. Перейдите в `bots` -> `trivia-bot`, создайте `Docker` образ (пример 
	`docker build -t trivia_bot .`)

	1. Затем выполните команду (пример `docker tag <image id> 111663367461.dkr.ecr.us-east-2.amazonaws.com/trivia_bot`)

	1. Отправьте полученный образ на `aws-машину` (пример `docker push 111663367461.dkr.ecr.us-east-2.amazonaws.com/trivia_bot`)


1. Запустите контейнер на `AWS` машине
	1. Выполните аутентификацию `Docker` в частном реестре `Amazon ECR`[Docker authentication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html)(пример `aws ecr get-login --region <ваш регион, где регистрировались> --no-include-email`). Затем полученный ключ скопируйте и введите в консоль, и нажмите `Enter`. Аутентификация выдается на 12 часов.

	1. Выполните команду (пример `docker pull 111663367461.dkr.ecr.us-east-2.amazonaws.com/trivia_bot:latest`)
	1. Запустите бота. Выполнить команду `docker-compose -f docker-compose-aws.yml up`
