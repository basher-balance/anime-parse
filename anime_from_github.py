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
    "Величайший Повелитель Демонов перерождается как",
]

url_base = "https://naruto-base.su"
link = f"{url_base}/novosti/drugoe_anime_ru"
# Количество страниц, которое будет просматривать код
pages = 3


def title_maches(title):
    for list_title in list_anime:
        if list_title in title:
            return True
    return False


async def get_html(client, url):
    response = await client.get(url)
    return response.text


async def get_name_and_id_anime():
    dict_name_id = {}
    async with httpx.AsyncClient() as client:
        tasks = (
            get_html(client, f'{link}?page{page}')
            for page in range(1, pages)
        )
        list_content = await asyncio.gather(*tasks)

        list_url_anime = []
        for content in list_content:
            anchors = BeautifulSoup(content, "lxml").select("h2 > a")

            links = filter(lambda tag: title_maches(tag.string), anchors)
            links = map(lambda tag: f'{url_base}{tag.get("href")}', links)

            list_url_anime.extend(links)

        tasks_two = (get_html(client, link) for link in list_url_anime)
        list_content_anime = await asyncio.gather(*tasks_two)
        for content_anime in list_content_anime:
            soup = BeautifulSoup(content_anime, 'lxml')
            name_anime = soup.find('h1', attrs={'itemprop': 'name'}).string
            id_video = str(soup.find('a', id='ep6')).split("'")[1]
            dict_name_id[name_anime] = id_video

    return dict_name_id


print(asyncio.run(get_name_and_id_anime()))
