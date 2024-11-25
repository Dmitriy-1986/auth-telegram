from telethon import TelegramClient

# Замените на свой API ID и API Hash, полученные при регистрации приложения
api_id = '21002229'
api_hash = 'ef86b3d8721805538b11a9ce26626c91'

# Имя сессии (файл сессии должен быть в текущей директории)
session_name = 'telegram_auth'

# Создаем клиент
client = TelegramClient(session_name, api_id, api_hash)


async def main():
    # Начинаем работу с клиентом
    await client.start()

    # Укажите ID чата напрямую
    chat_id = 'Вынос мозга'

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
        print(f"\nСообщения из чата {chat.title}:")
    else:
        print(f"\nСообщения из чата (User ID {chat.id}):")

    # Получаем последние сообщения из этого чата
    messages = await client.get_messages(chat, limit=350)

    for message in messages:
        # Получаем отправителя
        sender = await message.get_sender()

        # Получаем имя отправителя
        sender_name = f"{sender.first_name} {sender.last_name}" if sender.last_name else sender.first_name
        if sender.username:
            sender_name += f" (@{sender.username})"

        # Вывод текста сообщения
        text = message.text or "Нет текста"
        print(f"[{sender_name}] {message.date} - {text}")

        # Проверяем, содержит ли сообщение фото
        if message.photo:
            # Сохраняем фото в текущей директории
            file_path = await message.download_media(file=f"./photo_{message.id}.jpg")
            print(f"Фото сохранено: {file_path}")

        # Проверяем, содержит ли сообщение документ
        if message.document and not message.photo:  # Исключаем фото, которые тоже являются документами
            file_path = await message.download_media(file=f"./document_{message.id}")
            print(f"Документ сохранен: {file_path}")


# Запускаем
with client:
    client.loop.run_until_complete(main())

