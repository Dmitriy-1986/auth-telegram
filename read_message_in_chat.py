from telethon import TelegramClient

# Замените на свой API ID и API Hash, полученные при регистрации приложения
api_id = '21002229'
api_hash = 'ef86b3d8721805538b11a9ce26626c91'

# Имя сессии (файл сессии должен быть в текущей директории)
session_name = 'telegram_auth'  # имя файла сессии

# Создаем клиент
client = TelegramClient(session_name, api_id, api_hash)


async def main():
    # Начинаем работу с клиентом
    await client.start()

    # Укажите ID чата напрямую
    chat_id = 391145992  # ID чата

    try:
        # Пытаемся получить чат по ID
        chat = await client.get_entity(chat_id)
    except ValueError as e:
        print(f"Ошибка: {e}")
        return
    except Exception as e:
        print(f"Не удалось найти чат с ID {chat_id}: {e}")
        return

    # Выводим информацию о чате
    if hasattr(chat, 'title'):  # Проверка на наличие атрибута title
        print(f"\nПоследние 20 сообщений из чата {chat.title}:")
    else:
        print(f"\nПоследние 20 сообщений из чата (User ID {chat.id}):")

    # Получаем последние 20 сообщений из этого чата
    messages = await client.get_messages(chat, limit=20)

    for message in messages:
        # Получаем отправителя
        sender = await message.get_sender()

        # Получаем имя отправителя
        sender_name = f"{sender.first_name} {sender.last_name}" if sender.last_name else sender.first_name
        if sender.username:
            sender_name += f" (@{sender.username})"

        print(f"[{sender_name}] {message.date} - {message.text}")


# Запускаем
with client:
    client.loop.run_until_complete(main())
