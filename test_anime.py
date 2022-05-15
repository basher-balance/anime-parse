import aiohttp
import asyncio

from bs4 import BeautifulSoup


list_anime = [
    "Семья шпиона",
    "Мир отомэ-игр — это тяжёлый мир для мобов",
    "Госпожа Кагуя: в любви как на войне",
    "Рыцарь-скелет вступает в параллельный мир",
    "Восхождение героя щита 2 сезон",
    "Перестану быть героем",
    "Тусовщик Кунмин",
    "Величайший Повелитель Демонов перерождается как",
]

link_drugoe_anime = "https://naruto-base.su/novosti/drugoe_anime_ru"
url_base = "https://naruto-base.su"
# Количество страниц, которое будет просматривать код
pages = 8



async def get_response_txt(client, url):
    async with client.get(url) as response:
        response_txt = await response.text()
        return response_txt


async def get_link_and_episode():

    async with aiohttp.ClientSession() as client:
        tasks = []
        for page in range(1, pages):
            page_link_drugoe_anime = f'{link_drugoe_anime}?page{page}'
            tasks.append(
                    asyncio.ensure_future(
                        get_response_txt(
                            client, page_link_drugoe_anime
                            )
                        )
                    )
        list_task_response = await asyncio.gather(*tasks)
        global list_link_anime
        list_link_anime = []
        for task_response in list_task_response:
            soup_response = BeautifulSoup(task_response, 'lxml')
            list_soup_tag_h2 = soup_response.find_all('h2')
            for tag_h2 in list_soup_tag_h2:
                for title in list_anime:
                    tag_h2_text = tag_h2.get_text()
                    link_b = tag_h2.find("a").get("href")
                    if title in tag_h2_text:
                        print('название: ' + tag_h2_text)
                        link_anime = f'{url_base}{link_b}'
                        print(link_anime)
                        list_link_anime.append(link_anime)



async def hochu():
    async with aiohttp.ClientSession() as client:
        taskq = []
        for pager in list_link_anime:
            taskq.append(
                    asyncio.ensure_future(
                        get_response_txt(
                            client, pager
                            )
                        )
                    )
        original_pokemonn = await asyncio.gather(*taskq)
        for pokemon in original_pokemonn:
            soup_str_list_respons_pages = BeautifulSoup(pokemon, 'lxml')
            asdf = soup_str_list_respons_pages.find('a', id='ep6').get('onclick')
            print(asdf)


asyncio.run(get_link_and_episode())
asyncio.run(hochu())
