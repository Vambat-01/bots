1) Арендуем виртуальную машину *EC2* на `https://aws.amazon.com`

2) Запускаю ее, и в процессе скачаваем ***key-pair***

3) Подключаемся к *aws-машине* через свой терминал используя ***key-pair*** скаченную ранее (пример: **ssh -i "/home/vambat/Downloads/trivia_bot_key_pair.pem" ec2-user@ec2-3-15-202-70.us-east-2.compute.amazonaws.com** ) 

4) На `https://aws.amazon.com` переходит в раздел *EC2* -> *Security groups*. В *securety group* открываем порт 8000, 443 в *Inbound rules*. (пример: **HTTP	TCP	8000	0.0.0.0/0**)

5) В *aws-машине* устанавливаем *Docker*. `https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html` (раздел *Installing Docker*)

6) Настраиваем *aws credentials* на своей-машине  (`https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html` секция *Configuration and credential file settings*)
	a) *aws configure*  и вводить ключи (пример: `https://console.aws.amazon.com/iam/home?region=us-east-2#/security_credentials`  тут получим ключ)

7) Затем на `https://aws.amazon.com` переходим в *Elastic Container Registry* (*ECR*) создаем репозиторий, выбираем его и нажимаем на *View push commands* (выполняем все команды)

8) Для аутентификации *Docker* в частном реестре *Amazon ECR* на *своей-машине* `https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html` 
	Пример: **aws ecr get-login-password --region us-east-2 | docker login username AWS --password-stdin 111663367461.dkr.ecr.us-east-2.amazonaws.com**
	а) Если не установлен *AWS CLI* `https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html` установить

9) 1) Получаем сертификат `https://stackoverflow.com/questions/10175812/how-to-generate-a-self-signed-ssl-certificate-using-openssl`
	а) Обязательно нужно поставить *-subj '/CN=localhost`*. *CN* должен совпадать с *DNS* именем вашей aws-машины
	Пример:	**openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=ec2-3-15-202-70.us-east-2.compute.amazonaws.com'**
	б) Скопируем ***key.pem*** и ***cert.pem*** на aws-машину. Перейти в папку куда вы их скачали и выполнить командy: 
	**scp -i <путь к файлу key-pair> <файл, который хотите скопировать> ec2-user@ec2-3-15-202-70.us-east-2.compute.amazonaws.com:~/**

10) Отправляем образ со своей-машины на *aws-машину* `https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-pull-ecr-image.html`
	а) На своей-машине создаем образ вводит в терминал. Пример: **docker build -t trivia_bot .**
	b) Далее docker **tag a0273253e51b 111663367461.dkr.ecr.us-east-2.amazonaws.com/trivia_bot**
	в) Отправляем полученный образ на *aws-машину*. Пример: **docker push 111663367461.dkr.ecr.us-east-2.amazonaws.com/trivia_bot**

11) На *aws-машине* создаем ***docker-compose.yml*** и ***bot.env*** с нужными вам парамметрами.

12) На *aws-машине* выполняем:
	a) Выполняем аутентификацию *Docker* в частном реестре *Amazon ECR* `https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html` Пример: **aws ecr get-login --region us-east-2 --no-include-email**
	Затем полученный ключ копируем вводим в консоль и нажимаем *Enter*
	б) Дальше делаем: **docker pull 111663367461.dkr.ecr.us-east-2.amazonaws.com/trivia_bot:latest**
	в) Выполняем: **docker-compose up**
