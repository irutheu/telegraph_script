## Установка
- `python -m venv venv`
- `venv\Scripts\activate`
- `pip install -r requirements.txt`
- Создать файл credentials.yaml в который поместить строчку: `telegraph_token: "Ваш токен"` 

## Использование
В cmd:
- `venv\Scripts\activate`
- `python main.py -d "Путь до папки с изображениями" -t "Название поста"`
