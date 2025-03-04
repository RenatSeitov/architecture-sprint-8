## Клонировать репозиторий

```git clone https://github.com/anqorithm/fastapi-keycloak.git
cd fastapi-keycloak
Копировать файл переменных среды
```
## Перейдите в srcкаталог и скопируйте .env.exampleфайл в .env:
```
cd src
mv .env.example .env
```

## Настроить переменные среды

Откройте .envфайл и обновите следующие переменные в соответствии с вашей конфигурацией Keycloak:

KEYCLOAK_SERVER_URL: URL-адрес, на котором запущен ваш сервер Keycloak (например, http://keycloak:8080/).
KEYCLOAK_REALM: Имя вашей области Keycloak (например, fastapi-realm).
KEYCLOAK_CLIENT_ID: Идентификатор клиента, который вы настроили в Keycloak (например, fastapi-client).
KEYCLOAK_CLIENT_SECRET: Секрет клиента, полученный от Keycloak.


## Запустите приложение с помощью Docker Compose:

```
docker-compose up --build
```