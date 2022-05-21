import asyncio
import httpx
from bs4 import BeautifulSoup



favorite_anime = [
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
url_base = "https://naruto-base.su"
# Количество страниц, которое будет просматривать код
pages = 8
result = dict()

async def get_anime(client, url):
        response = await client.get(url)
        return response.text

async def get_sub_voice(client,url):
        sitemap = await get_anime(client,url)
        soup = BeautifulSoup(sitemap,'lxml')
        name_anime = soup.find('h1',attrs={'itemprop':'name'}).string
         # получаем название аниме
        for i in range(len(name_anime)):                              # вытягиваем позицию с которого налась цифра,для того чтобы вытащить имя аниме и эпизод
            if name_anime[i].isnumeric():
                name_anime,episode = name_anime[:i],name_anime[i:]
                break                                                 # дальше нету смысла искать
        
        for voice_sub in soup.find_all('a',id=True,onclick=True):     # ищем элемент с озвучкой и субтитрами
            string_voice_sub = voice_sub.string                       # вытаскиваем студию для для проверки на любимчиков
            if 'sibnet' in string_voice_sub.lower():
                global_key = voice_sub['onclick'].split('\'')[1]
                type_anime = ('voice','sub')[string_voice_sub.find('озвуч') < 1]
                named_key  = f'{name_anime}_{type_anime}'
                if named_key in result:     #   Проверка что больше то и самое новое
                    number_one = episode.replace('серия','').replace('сезон','').replace(' ','')
                    number_one = int(number_one)

                    number_two = result[named_key]['episode'].replace('серия','').replace('сезон','').replace(' ','')
                    number_two = int(number_two)

                    if number_one > number_two:
                        result[named_key] = {
                            'name':     name_anime,
                            'type':     type_anime,
                            'episode':  episode,
                            'url':      f'https://video.sibnet.ru/shell.php?videoid={global_key}'
                        }
                else:
                    result[named_key] = {
                        'name':     name_anime,
                        'type':     type_anime,
                        'episode':  episode,
                        'url':      f'https://video.sibnet.ru/shell.php?videoid={global_key}'
                    }
            
async def filter(sitemap,client):
    soup    = BeautifulSoup(sitemap,'lxml')
    animes  = soup.find_all('h2')
    for anime in animes:
        for title in favorite_anime:
            if title in anime.get_text():
                link_to_anime = f'{url_base}{anime.find("a").get("href")}' 
                await get_sub_voice(client,link_to_anime)


async def main_two():
    async with httpx.AsyncClient() as client:
        tasks    = (get_anime(client,f'{link}?page{number}') for number in range(1,pages))
        sitemaps = await asyncio.gather(*tasks)
        sitemaps = (filter(i,client) for i in sitemaps)
        await asyncio.gather(*sitemaps)

asyncio.run(main_two())
