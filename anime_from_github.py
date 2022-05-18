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
pages = 8


async def get_html(client, url):
        response = await client.get(url)
        return response.text


async def get_sub_voice(client,url):
        sitemap = await get_html(client,url)
        soup = BeautifulSoup(sitemap,'lxml')
        name_anime = soup.find('h1',attrs={'itemprop':'name'}).string
        id_video = str(soup.find('a', id='ep6')).split("'")[1]
        asdf = [name_anime, id_video]
        return asdf


async def main_two():
    async with httpx.AsyncClient() as client:
        tasks    = (get_html(client,f'{link}?page{number}') for number in range(1,pages))
        sitemaps = await asyncio.gather(*tasks)
        list_last_episode = []
        for sitemap in sitemaps:
            soup_sitemap = BeautifulSoup(sitemap, "lxml")
            tags_h2 = soup_sitemap.find_all('h2')
            for tag_h2 in tags_h2:
                tag_t = tag_h2.get_text()
                tag_href = tag_h2.find('a').get('href')
                for tit in list_anime:
                    if tit in tag_t:
                        print(tag_t)
                        link_to_anime = f'{url_base}{tag_href}'
                        list_last_episode.append(link_to_anime)
                        list_anime.remove(tit)
                    else:
                        pass
        tasks_two    = (get_html(client,link) for link in list_last_episode)
        sits = await asyncio.gather(*tasks_two)
        ll = []
        ii = []
        for sit in sits:
            soup = BeautifulSoup(sit, 'lxml')
            name_anime = soup.find('h1',attrs={'itemprop':'name'}).string
            id_video = str(soup.find('a', id='ep6')).split("'")[1]
            ll.append(name_anime)
            ii.append(id_video)
        

        return ii



#klek = asyncio.run(main_two())
#
#async def main():
#    async with httpx.AsyncClient() as client:
#        tasks    = (get_html(client,link) for link in klek)
#        sits = await asyncio.gather(*tasks)


print(asyncio.run(main_two()))
