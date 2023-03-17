import aiohttp
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, Message
from nonebot.log import logger
from nonebot.rule import to_me
from pydantic import parse_obj_as
from bs4 import BeautifulSoup

from skadi import config
from .types import *
from .test import data

resp = on_command("search", rule=to_me(), aliases={"搜图"}, priority=5)


@resp.handle()
async def get_pic(event: MessageEvent):
    back: Message = Message()
    back += Message.template("{str}").format(str="SauceNao")
    
    for msg in event.reply.message["image"] if event.reply else event.message["image"]:
        pic_url = msg.data["url"]
        _data = parse_obj_as(JsonData, await search_from_saucenao(pic_url)).results[0]
        back += Message.template("{link:image}\n").format(link=_data.header.thumbnail)
        for url in _data.data.dict()['ext_urls']:
            back += Message.template("url : {url}\n").format(url=url)
        back += Message.template("title : {title}\n").format(title=_data.data.dict()[data_models[_data.header.index_id]['title']])
        back += Message.template("author : {author}\n").format(author=_data.data.dict()[data_models[_data.header.index_id]['author']])
        
    await resp.finish(back)


async def search_from_saucenao(url: str) -> dict:
    api_key = config.SAUCENAO_KEY
    proxys = config.proxies
    # result_num = str(config.SAUCENAO_RESULT_NUM) if type(config.SAUCENAO_RESULT_NUM) == int else "5"
    sau_url = "https://saucenao.com/search.php"
    async with aiohttp.ClientSession() as session:
        async with session.get(
                sau_url + "?output_type=2&api_key=" + api_key + "&dbs[]=5&dbs[]=9&dbs[]=12&dbs[]=21&dbs[]=22&dbs[]=25&dbs[]=26&dbs[]=28&dbs[]=39&dbs[]=41&dbs[]=43&numres=1&url=" + url,
                headers=headers, proxy=proxys.get("http")) as response:
            return await response.json()


async def search_from_ascii2d(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        # 构造请求的URL
        search_url = 'https://ascii2d.com/search/uri/{}'.format(url)
        async with session.get(search_url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')

            results = []
            for item in soup.select('.detail-box'):
                result = {
                    'title': item.select_one('.detail-title').text.strip(),
                    'url': item.select_one('.detail-link-box a')['href'],
                    'thumbnail': item.select_one('.detail-box-img img')['src'],
                    'similarity': item.select_one('.detail-point').text.strip()
                }
                results.append(result)
            return results
