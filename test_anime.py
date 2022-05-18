import aiohttp
import asyncio
import httpx 

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
        response = await client.get(url)
        await asyncio.sleep(0)
        return response.text


async def get_link_and_episode():

    async with httpx.AsyncClient() as client:
        tasks = []
        list_link_anime = []
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
        asdf = str(list_task_response)
        soup_str_list_task_response = BeautifulSoup(asdf, 'lxml')
        list_soup_tag_h2 = soup_str_list_task_response.find_all('h2')
        print(list_soup_tag_h2)
        for tag_h2 in list_soup_tag_h2:
            for title in list_anime:
                tag_h2_text = tag_h2.get_text()
                url_anime = str(tag_h2.find("a").get("href"))
                print(str(url_anime))
                if title in tag_h2_text:
                    print('название: ' + tag_h2_text)
                    link_anime = f'{url_base}{url_anime}'
                    print(link_anime)
                    list_link_anime.append(link_anime)
            break
        return list_link_anime



async def get_id_video(test):
    async with httpx.AsyncClient() as client:
        taskq = []
        for page in test:
            taskq.append(
                    asyncio.ensure_future(
                        get_response_txt(
                            client, page
                            )
                        )
                    )
        list_task_respons = await asyncio.gather(*taskq)
        print(list_task_respons)
        for task_response in list_task_respons:
            soup_str_list_respons_pages = BeautifulSoup(task_response, 'lxml')
            try:
                tag_a_and_id = soup_str_list_respons_pages.find('a', id='ep6').get('onclick')
            except AttributeError:
                pass
            else:
#            tag_a_and_id = soup_str_list_respons_pages.find('a', id='ep6').get('onclick').split("'")[1]
                print(tag_a_and_id)


#asyncio.run(get_link_and_episode())
asyncio.run(get_id_video(asyncio.run(get_link_and_episode())))
