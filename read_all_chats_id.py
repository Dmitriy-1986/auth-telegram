from telethon import TelegramClient

# Замените на свои значения API ID и API Hash
api_id = '**********'
api_hash = '********************************'

# Имя сессии (файл сессии должен быть в текущей директории)
session_name = 'telegram_auth'  # имя файла сессии

# Создаем клиент
client = TelegramClient(session_name, api_id, api_hash)

async def main():
    # Начинаем работу с клиентом
    await client.start()

    # Получаем список чатов
    chats = await client.get_dialogs()

    print("Список чатов:")
    for chat in chats:
        # Выводим только название чата и его ID
        print(f"Название чата: {chat.name}, ID: {chat.id}")

# Запускаем
with client:
    client.loop.run_until_complete(main())
