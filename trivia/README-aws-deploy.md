Инсрукция, как развернуть бота на на арендованной машине Amazon Web Servicer (*AWS*).

Скачать репозиторий на *свою-машину*. 
Создать аккаунт на *AWS*  [https://aws.amazon.com](https://aws.amazon.com)


## Аренда и подключение к *aws-машине*
Сразу после регистрации на сервисе вы попадете в консоль *AWS EC2*. Там можно выбрать *EC2* и тип машины, на которой будет развернут бот. 
Важный момент: нас интересует *t2micro* (помечен зелёным стикером), т.к. всё остальное будет платным. 

- Создать виртуальную машину.
Чтобы создать виртуальную машину, щелкнуть *Launch Instance* на панели управления [Amazon EC2](https://console.aws.amazon.com/ec2/v2/home). Выполнить все шаги. В процессе скачается *key-pair*

- Подключение к *aws-машине*.
 Через терминал *своей-машины* используя *key-pair* скаченную ранее (пример: **ssh -i "key_pair.pem" ec2-user@ec2-3-15-202-70.us-east-2.compute.amazonaws.com** )


## Настройка *AWS EC2*
- Установить *Docker* на *aws-машину* [Install Docker](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html) (раздел *Installing Docker*)

- Установить *Docker Compose* на *aws-машину* [Install Docker Compose](https://docs.docker.com/compose/install/#install-compose-on-linux-systems)


## Настройка *ECR*

На сайте [https://aws.amazon.com](https://aws.amazon.com)
- Перейти в *Elastic Container Registry* (*ECR*) создать репозиторий, выбрать его и нажимать на *View push commands* (выполнить все команды)

- Перейти в раздел *EC2* -> *Security groups*. В *securety group* открыть порт 8000, 443 в *Inbound rules*. (пример: **HTTP	TCP	8000	0.0.0.0/0**)


## Наcтройка *своей-машины*
- Должен быть установлен *Docker*. Если не установлен, установить [Install Docker](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html) (раздел *Installing Docker*)

- Должен быть установлен *Docker Compose*. Если не установлен, установить [Install Docker Compose](https://docs.docker.com/compose/install/#install-compose-on-linux-systems)

- Должен быть установлен *AWS CLI*. Если нет, установить  [Isstall AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html)

- Настроить *aws credentials* [configuration aws credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)(раздел *Configuration and credential file settings*)
	- *aws configure*  и ввости ключи [Security Credentials](https://console.aws.amazon.com/iam/home?region=us-east-2#/security_credentials>),  тут получить ключ

- Получить сертификат [Certificate](https://stackoverflow.com/questions/10175812/how-to-generate-a-self-signed-ssl-certificate-using-openssl)
	- Обязательно нужно поставить *-subj '/CN=localhost`*. *CN* должен совпадать с *DNS* именем вашей aws-машины
	(пример:	**openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=ec2-3-15-202-70.us-east-2.compute.amazonaws.com'**)
	- Скопировать *key.pem* и *cert.pem*** на *aws-машину*. Перейти в папку куда они скачались и выполнить командy, (пример	**scp -i <путь к файлу key-pair> <файл, который хотите скопировать> ec2-user@ec2-3-15-202-70.us-east-2.compute.amazonaws.com:~/**)


## Отправить необходимые файлы со *своей-машины* на *aws-машину*

- Перейти в репозиторий бота *bots* -> *trivia*. В текущей директории.
	- В файле *bot.env* исправить значение *SERVER_URL* на ваше.
	- Скопировать *bot.env* и *docker-compose-aws.yml* на *aws-машину* (пример: **scp -i <путь к файлу key-pair> <файл, который хотите скопировать> ec2-user@ec2-3-15-202-70.us-east-2.compute.amazonaws.com:~/**)
	- Скопировать ваш json файл на *aws-машину*. Пример файла, можно найти перейдя *bots* -> *trivia* -> *resources* -> *bot_questions_mini.json*
	(пример: **scp -i <путь к файлу key-pair> <файл, который хотите скопировать> ec2-user@ec2-3-15-202-70.us-east-2.compute.amazonaws.com:~/**)


## Отправить образ со *своей-машины* на *aws-машину* [Pull erc image](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-pull-ecr-image.html)

-  Выполнить аутентификацию *Docker* в частном реестре *Amazon ECR* [Docker authentication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html)
	(пример: **aws ecr get-login-password --region us-east-2 | docker login username AWS --password-stdin 111663367461.dkr.ecr.us-east-2.amazonaws.com**)
	Она выдается на 12 часов.

- Перейти в *bots* -> *trivia*, создать *Docker* образ (пример: 
	**docker build -t trivia_bot .**)

- Затем выполнить команду (пример **docker tag <image id> 111663367461.dkr.ecr.us-east-2.amazonaws.com/trivia_bot**)

- Отправить полученный образ на *aws-машину* (пример: **docker push 111663367461.dkr.ecr.us-east-2.amazonaws.com/trivia_bot**)


## Запустить бота на *AWS-машине*

- Выполнить аутентификацию *Docker* в частном реестре *Amazon ECR*[Docker authentication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html)(пример: **aws ecr get-login --region <ваш регион, где регистрировались> --no-include-email**)
Затем полученный ключ скопировать и ввести в консоль, и нажимаем *Enter*
Аутентификация выдается на 12 часов.

- Выполнить команду (пример **docker pull 111663367461.dkr.ecr.us-east-2.amazonaws.com/trivia_bot:latest**)
	в) Запустить бота. Выполнить команду: **docker-compose -f docker-compose-aws.yml up**