import asyncio
import config
import logging
from aiogram import Bot, Dispatcher, executor, types

import requests
from bs4 import BeautifulSoup

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot)


async def send_message(channel_id: int, message: str):
    await bot.send_message(channel_id, message)


async def scheduled(wait_for):
    await asyncio.sleep(wait_for)
    last_to_history = 'start'
    while True:
        url = 'https://www.cybersport.ru/dota-2'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        # Парсинг последней статьи из списка
        new = soup.find('div', class_='grid__col--ipad-4 grid__col--phone-6 margin-bottom--20')
        # ..........................................................
        # Название статьи
        if new is not None:
            new_to = new.find('a', class_='inverse-color--black-00').text
            print(new_to)
            # Если название статьи не совпадает с названием последней  размещенной
            if new_to != last_to_history:
                text_message = ''
                last_to_history = new_to
                text_message = new_to + '\n\n'

                # Достать ссылку на статью
                new_url = new.find('a', class_='inverse-color--black-00')['href']
                new_url = 'https://www.cybersport.ru' + new_url

                # Чтение статьи
                new_response = requests.get(new_url)
                new_soup = BeautifulSoup(new_response.text, 'lxml')

                # Парсинг текста из статьи
                new_text = new_soup.find_all('div', class_='typography js-mediator-article')
                for text in new_text:
                    tex = text.find_all('p')

                    for t in tex:
                        text_message += t.text

                await bot.send_message(config.CHANNEL_ID, text_message + '\n\n' + new_url)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(10))
    executor.start_polling(dp, skip_updates=True)
