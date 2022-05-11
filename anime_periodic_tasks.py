import requests
import re

from bs4 import BeautifulSoup


import asyncio
import httpx


list_anime = [
    "Семья шпиона",
    "Мир отомэ-игр — это тяжёлый мир для мобов",
    "Госпожа Кагуя: в любви как на войне",
    "Рыцарь-скелет вступает в параллельный мир",
    "Восхождение героя щита 2 сезон",
    "Перестану быть героем",
    "Тусовщик Кунмин",
    "Величайший Повелитель Демонов перерождается как типичное ничтожество",
]

link = "https://naruto-base.su/novosti/drugoe_anime_ru"
url_base = "https://naruto-base.su/"
# Количество страниц, которое будет просматривать код
pages = 3



async def get_anime(client, url):
        response = await client.get(url)
        return response.text


async def main():

    async with httpx.AsyncClient() as client:
        tasks = []
        for number in range(1, pages):
            url = f'{link}?page{number}'
            tasks.append(asyncio.ensure_future(get_anime(client, url)))

        animes = await asyncio.gather(*tasks)
        return animes


async def get_an(client, url):
        response = await client.get(url)
        return response.text


async def foo():

    async with httpx.AsyncClient() as client:
        tas = []
        for ur in link_to_anime_list:
            tas.append(asyncio.ensure_future(get_an(client, ur)))

        videoid = await asyncio.gather(*tas)
        return videoid

link_to_anime_list = []
# Объединяю спаршеные страницы в одну
site = ''.join(asyncio.run(main()))
# Перевожу в объект для парсинга
soup = BeautifulSoup(site, "lxml")
# Ищу все теги h2
tag_h2_list = soup.find_all('h2')
# Перебираю теги
for tag_h2 in tag_h2_list:
    # Перебираю аниме из списка аниме
    for title in list_anime:
        # Ищу аниме в перебираемых тегах
        if title in tag_h2.get_text():
            print(f'Печатаю то, что будет записываться в "title_anime":\n\t{tag_h2.get_text()}')
            # Если аниме присутствует в название вывожу часть ссылки на страницу с аниме
            link_to_anime = f'{url_base}{tag_h2.find("a").get("href")}'
            print(f'Ссылка на страницу с выбором озвучки:\n\t{link_to_anime}')
            link_to_anime_list.append(link_to_anime)

print("ДО")
ket = ''.join(asyncio.run(foo()))
print(ket)
print("ПОСЛЕ")
 #           print(f'{tag_h2}\n')
#print(tag_h2)

#for ak in site:
#    k = BeautifulSoup(ak, "lxml")
#    for b in k.find_all('h2'):
#        for a in list_anime:
#            if a in b.get_text():
#                print(b)
#            continue
## Функция возвращающая ссылку на последнюю серию аниме по названию в заголовке файла, заданному в параметрах
#def data_last_element_anime(id=None):
#    for i in range(pages):
#        anime_ID = [
#            link["href"]
#            for link in (data_scrapping(url + "?page" + str(i + 1), "a"))
#            if id in link.get_text()
#        ]
#        if len(anime_ID) == 0:
#            pass
#        else:
#            link_anime = url_base + anime_ID[0]
#            # Поиск ссылки на последний эпизод аниме с сабами и без на портале Sibnet
#            last_episode_sub = data_scrapping(link_anime, "a", id="ep6")
#            # last_episode = data_scrapping(link_anime, 'a', id="ep14")
#            # result_sub = re.search(r'\d{7}', str(last_episode_sub))[0]
#            try:
#                result_dub = re.search(r"\d{7}", str(last_episode_sub))[0]
#            except TypeError:
#                pass
#            else:
#                link_name_and_element_anime = data_scrapping(link_anime, "h1")[0].text
#                # link_result_sub = 'https://video.sibnet.ru/shell.php?videoid=' + result_sub
#                link_result_dub = (
#                    "https://video.sibnet.ru/shell.php?videoid=" + result_dub
#                )
#                try:
#                    anime_title_anime = Anime.objects.create(
#                        title_anime=link_name_and_element_anime,
#                        link_anime=link_result_dub,
#                    )
#                except IntegrityError:
#                    pass
#                else:
#                    anime_title_anime.save(force_update=True)
#                # puk[link_name_and_element_anime] = link_result_dub
#                break
#
#
#def last_series_anime():
#    logging.warning("It is time to start the dramatiq task anime")
#    for anime in list_anime:
#        data_last_element_anime(id=anime)
