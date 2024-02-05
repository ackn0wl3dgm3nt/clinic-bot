# clinic-bot

## Setup (запуск и настройка проекта):
1. Изменить config.py:
- Postgres: host, user, password (подключение к БД)
- BOT_TOKEN: токен телеграмм бота (получать в @BotFather)
2. Установить PostgreSQL (16.1)
3. Запустить migrations.py для настройки БД
4. Запустить app.py (бот)
5. Заполнить таблицы Specialties и Doctors (см. Заполнение таблиц)

## Структура проекта:
- app.py - хендлеры (Dispatcher)
- config.py - конфигурация бота (токен бота, FSM хранилище)
- db.py - обращения к БД
- keyboards.py - клавиатуры (ReplyMarkup)
- states.py - стейты
- validators.py - валидаторы (проверки) пользовательских данных
- migrations.py - миграции БД
- wordings.py - текста бота

## Структура БД:
1. Patients: (Пациенты)
- telegram_id - Telegram ID (PRIMARY KEY)
- fullname - ФИО
- birthday - Дата Рождения
- phone - Номер телефона
- policy - Полис ОМС (16 символов)
- passport (Серия и номер паспорта)

2. Specialties: (Специальности)
- id - ID Специальности (PRIMARY KEY)
- name - Название специальности

3. Doctors: (Доктора)
- id - ID Доктора (PRIMARY KEY)
- specialist_id - ID Специальности (FOREIGN KEY)
- fullname - ФИО
- experience - опыт
- birthday - Дата Рождения
- gender - пол
- email - электронная почта

4. Records: (Записи)
- id - ID Записи (PRIMARY KEY)
- telegram_id - Telegram ID (FOREIGN KEY)
- doctor_id - ID Доктора (FOREIGN KEY)
- date - Дата
- time - Время

## Заполнение таблиц:
### Подключишься к БД через pgAdmin, выполните следующие SQL-запросы:
1. Таблица Специальности

INSERT INTO Specialties (name)
VALUES ('Хирург'),
('Терапевт'),
('Стоматолог'),
('Уролог'),
('Гинеколог'),
('Нарколог'),
('Психиатр'),                  
('Дерматолог'),                                                                                          
('Отоларинголог'),                      
('Эндокринолог');
2. Таблица Доктора

INSERT INTO Doctors (specialist_id, fullname, experience, birthday, gender, email)
VALUES 
    (1, 'Смелов Владимир Владиславович', 15, '1983-09-23', 'Мужской', 'smelov.v@mail.ru'),
    (2, 'Акунович Станислав Иванович', 20, '1991-03-17', 'Мужской', 'stan@mail.ru'),
    (3, 'Колесников Виталий Леонидович', 3, '1992-03-28', 'Мужской', 'Kolesnikov@mail.ru'),
    (4, 'Бракович Андрей Игоревич', 12, '1987-10-17', 'Мужской', 'brakovich@gmail.ru'),
    (2, 'Дятко Александр Аркадьевич', 10, '1993-02-24', 'Мужской', 'alex.dyatko@mail.ru'),
    (5, 'Урбанович Павел Павлович', 8, '1994-04-16', 'Мужской', 'urban.pavel@mail.ru'),
    (6, 'Гурин Николай Иванович', 9, '1996-06-18', 'Мужской', 'gyrin@mail.ru'),
    (7, 'Жиляк Надежда Александровна', 16, '1982-04-25', 'Женщина', 'zhilyak@gmail.ru'),                  
    (8, 'Мороз Елена Станиславовна', 7, '1996-08-14', 'Женщина', 'elena.morozova@mail.ru'),                                                                                          
    (9, 'Барташевич Святослав Александрович', 25, '1997-11-27', 'Мужской', 'bartash@gmail.ru'),
    (3, 'Арсентьев Виталий Арсентьевич', 19, '1982-04-23', 'Мужской', 'ars.vitali@mail.ru'),                      
    (10, 'Барановский Станислав Иванович', 2, '1991-07-19', 'Мужской', 'baran@mail.ru'),
    (1, 'Насковец Михаил Трофимович', 17, '1984-02-28', 'Мужской', 'mih.trofimovich@gmail.ru');
