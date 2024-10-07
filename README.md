# test_task_ydisk

## Приложение для просмотра и скачивания файлов с Яндекс Диска

Версия python 3.12.5
### Инструкция по запуску приложения на Linux
Для запуска после клонирования репозитория необходимо создать виртуальное окружение и установить зависимости:
``` bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Далее необходимо создать яндекс приложение [тут](https://oauth.yandex.ru/) ([инструкция](https://yandex.ru/dev/id/doc/ru/register-client))

Потом создать файл .env и задать значения следующим переменным:
``` 
SECRET_KEY = любая_строка_в_качестве_секретного_ключа_приложения
CLIENT_ID = id_клиента_приложения_яндекс
CLIENT_SECRET = секрет_клиента_приложения_яндекс
```
После выполнения предыдущих шагов можно запускать приложение:
``` bash
python app.py
```

Публичный ключ для тестирования: **X44aaxgfnzWxMBbEzurLtppnk855RW36W5hc1o1J+aqY5MhhNqhAI8BoN9+/aqvyq/J6bpmRyOJonT3VoXnDag==**