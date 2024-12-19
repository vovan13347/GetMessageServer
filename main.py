import asyncio
import aiohttp
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
SERVER_URL = config["SERVER"]["URL"]

async def fetch_albums(session):
    """
    Асинхронно получает список альбомов с сервера.
    :param session: асинхронная сессия aiohttp.
    """
    try:
        async with session.get(SERVER_URL) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        print(f"Ошибка при получении данных с сервера: {e}")
        return []

async def monitor_new_albums(poll_interval=5):
    """
    Следит за добавлением новых альбомов на сервер асинхронно.
    :param poll_interval: интервал между запросами в секундах.
    """
    print("Начинаем асинхронный мониторинг новых альбомов...")
    known_albums = {}

    async with aiohttp.ClientSession() as session:
        # Первоначальная загрузка альбомов
        albums = await fetch_albums(session)
        known_albums = {album['id']: album for album in albums}

        while True:
            await asyncio.sleep(poll_interval)  # Асинхронная пауза
            albums = await fetch_albums(session)

            # Проверяем новые альбомы
            for album in albums:
                if album['id'] not in known_albums:
                    print(f"Новый альбом добавлен: {album['title']} - {album['band']}")
                    known_albums[album['id']] = album  # Добавляем новый альбом в известные

if __name__ == "__main__":
    # Запуск асинхронного мониторинга
    asyncio.run(monitor_new_albums(poll_interval=5))
