Платформа для онлайн-обучения "Smart lessons"

Цель проекта заключается в создании LMS-системы, в которой каждый желающий может размещать свои полезные материалы или курсы.


Установка и использование

Для работы программы необходимо заполнить файл .env своими данными (на примере файла .env.sample). 

Установить Docker и запустить следующие команды:

#создание образа django

docker build -t smart_lessons_django .

#создание сети для связи контейнеров

docker network create --driver bridge smart_lessons_network

#создание и запуск контейнера postgres
#my_password - заменить на пароль Postgres
#<directory_db> - заменить на директорию на вашем компьютере, где будут храниться базы данных

docker run --name smart_lessons_db -e POSTGRES_PASSWORD=my_password -e POSTGRES_DB=smart_lessons -d -v <directory_db>:/var/lib/postgresql/data --network smart_lessons_network postgres:15

#запуск миграций

docker run --network smart_lessons_network smart_lessons_django python manage.py migrate 

#создание и запуск контейнера django

docker run --name smart_lessons_django --network smart_lessons_network -p 8000:8000 -d smart_lessons_django

#создание superuser

docker exec smart_lessons_django python manage.py csu 


Описание приложений

 - main - отвечает за создание и управление курсами, уроками, подписками и платежами

 - users - отвечает за регистрацию, авторизации и управление профилем пользователей сайта


Дополнительная информация

 - fill_payments.py - содержит кастомную команду для заполнения данными по платежам в базу данных

 - tasks.py(main) - содержит отложенную задачу по рассылке пользователям, у которых есть подписка, писем об обновлении материалов курса

 - tasks.py(users) - содержит периодическую задачу по деактивации пользователей, которые не входили в приложение больше 30 дней


К приложению подключена возможность оплаты курсов через stripe.com.
Настроен вывод документации.