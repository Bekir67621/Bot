import asyncio
import logging
from telethon import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest, GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)



API_ID = 29727784  # Ваш API ID
API_HASH = "4a46b20265eeba63ee169f71dd7a5500"  
PHONE_NUMBER = "+992801649292"  


CHANNEL_ID = -1002353583010


USERS_TO_ADD = [
    "TooncinatorBot",
    "mahmudzodaa",

]



REQUEST_DELAY = 1


async def get_all_participants(client, channel):
    """Получает всех участников канала с использованием пагинации."""
    all_participants = []
    offset = 0
    limit = 200  

    while True:
        participants = await client(
            GetParticipantsRequest(
                channel,
                filter=ChannelParticipantsSearch(""),
                offset=offset,
                limit=limit,
                hash=0,
            )
        )
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += limit
        logger.info(f"Получено {len(participants.users)} участников. Всего: {len(all_participants)}")

    return all_participants


async def add_users_to_channel(client, channel, users_to_add, existing_user_ids):
    """Добавляет пользователей в канал, если они еще не являются участниками."""
    for user in users_to_add:
        try:
            user_entity = await client.get_entity(user)
            if user_entity.id not in existing_user_ids:
                await client(InviteToChannelRequest(channel, [user_entity]))
                logger.info(f"Пользователь {user} успешно добавлен в канал {channel.title}.")
            else:
                logger.info(f"Пользователь {user} уже в канале {channel.title}.")
        except Exception as e:
            logger.error(f"Ошибка при добавлении пользователя {user}: {e}")
        finally:
            await asyncio.sleep(REQUEST_DELAY)  # Задержка между запросами


async def main():
    """Основная функция для запуска клиента и выполнения операций."""
    client = TelegramClient("session_name", API_ID, API_HASH)

    try:
        await client.start(PHONE_NUMBER)
        logger.info("Клиент успешно авторизован.")

        
        channel = await client.get_entity(CHANNEL_ID)
        logger.info(f"Канал '{channel.title}' успешно получен.")

        # Получаем всех участников канала
        all_participants = await get_all_participants(client, channel)
        existing_user_ids = {user.id for user in all_participants}
        logger.info(f"Всего участников в канале {channel.title}: {len(existing_user_ids)}")

    
        await add_users_to_channel(client, channel, USERS_TO_ADD, existing_user_ids)

    except Exception as e:
        logger.error(f"Ошибка в основной функции: {e}")
    finally:
        await client.disconnect()
        logger.info("Клиент отключен.")


if __name__ == "__main__":
    asyncio.run(main())