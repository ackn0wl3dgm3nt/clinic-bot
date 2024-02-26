# clinic-bot
- Telegram-бот для регистрации и записи к врачу в поликлинике

## Setup (запуск и настройка проекта)
### ⚠️ Для запуска необходимо иметь Python 3.7+ и PostgreSQL 9.1+ ⚠️
1. _Изменить .env файл:_
- **BOT_TOKEN** (получить в @BotFather)
- **POSTGRES_USER** (указывается при установке PostgreSQL, по умолчанию = _postgres_)
- **POSTGRES_PASSWORD** (указывается при установке PostgreSQL, по умолчанию = _postgres_)
2. _Выполнить `python "src/migrations.py"` (миграции БД)_
3. _Выполнить `pip install -r requirements.txt` (установка зависимостей)_
3. _Запуск бота: `python "src/app.py"`_

## Структура проекта
- _src/_
  - _app.py_ - хендлеры (Dispatcher)
  - _config.py_ - конфигурация бота (токен бота, FSM хранилище, подключение к PostgreSQL)
  - _db.py_ - запросы к БД (Repository)
  - _keyboards.py_ - клавиатуры (ReplyMarkup)
  - _states.py_ - стейты (States)
  - _validators.py_ - валидаторы (проверки) пользовательских данных
  - _migrations.py_ - миграции БД
  - _wordings.py_ - текста бота
- _.env_ - переменные окружения

## Структура БД
1. **Patients: (Пациенты)**
- _telegram_id_ - Telegram ID (PRIMARY KEY)
- _fullname_ - ФИО
- _birthday_ - Дата Рождения
- _phone_ - Номер телефона
- _policy_ - Полис ОМС (16 символов)
- _passport_ (Серия и номер паспорта)

2. **Specialties: (Специальности)**
- _id_ - ID Специальности (PRIMARY KEY)
- _name_ - Название специальности

3. **Doctors: (Доктора)**
- _id_ - ID Доктора (PRIMARY KEY)
- _specialist_id_ - ID Специальности (FOREIGN KEY)
- _fullname_ - ФИО
- _experience_ - опыт
- _birthday_ - Дата Рождения
- _gender_ - пол
- _email_ - электронная почта

4. **Records: (Записи)**
- _id_ - ID Записи (PRIMARY KEY)
- _telegram_id_ - Telegram ID (FOREIGN KEY)
- _doctor_id_ - ID Доктора (FOREIGN KEY)
- _date_ - Дата
- _time_ - Время
