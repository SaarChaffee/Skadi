import asyncio
import aiohttp
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, Message
from nonebot.rule import to_me
from functools import partial
from pydantic import parse_obj_as
from bs4 import BeautifulSoup
import cloudscraper

from skadi import config
from .types import *
from .test import data

resp = on_command("search", rule=to_me(), aliases={"搜图"}, priority=5)


@resp.handle()
async def get_pic(event: MessageEvent):
    for msg in event.reply.message["image"] if event.reply else event.message["image"]:
        pic_url = msg.data["url"]
        await send_data_of_saucenao(pic_url)


async def send_data_of_saucenao(pic_url: str):
    back: Message = Message()
    back += Message.template("{str}").format(str="SauceNao")
    _data = parse_obj_as(JsonData, await search_from_saucenao(pic_url)).results[0]
    
    back += Message.template("{link:image}\n").format(link=_data.header.thumbnail)
    back += Message.template("title : {title}\n").format(title=_data.data.dict()[data_models[_data.header.index_id]['title']])
    back += Message.template("author : {author}\n").format(author=_data.data.dict()[data_models[_data.header.index_id]['author']])
    for url in _data.data.dict()['ext_urls']:
        back += Message.template("url : {url}\n").format(url=url)
    await resp.send(back)
    if float(_data.header.similarity) < config.threshold:
        await resp.send(Message.template("{str}").format(str="相似度过低，尝试使用ascii2d特征搜索"))
        await send_data_of_ascii2d(pic_url)


async def send_data_of_ascii2d(pic_url: str):
    back: Message = Message()
    back += Message.template("{str}").format(str="Ascii2d")
    datas = await search_from_ascii2d(pic_url)
    _data = datas[0]
    back += Message.template("{link:image}\n").format(link=_data['thumbnail'])
    for __data in _data['datas']:
        back += Message.template("title : {title}\n").format(title=__data['title'])
        back += Message.template("source : {source}\n").format(source=__data['source'])
        back += Message.template("author : {author}\n").format(author=__data['author'])
    await resp.send(back)


async def search_from_saucenao(url: str) -> dict:
    api_key = config.SAUCENAO_KEY
    proxies = config.proxies
    
    sau_url = "https://saucenao.com/search.php"
    async with aiohttp.ClientSession() as session:
        async with session.get(
                sau_url + "?output_type=2&api_key=" + api_key + "&dbs[]=5&dbs[]=9&dbs[]=12&dbs[]=21&dbs[]=22&dbs[]=25&dbs[]=26&dbs[]=28&dbs[]=39&dbs[]=41&dbs[]=43&numres=1&url=" + url,
                headers=sauHeaders, proxy=proxies.get("http")) as response:
            return await response.json()


async def search_from_ascii2d(url: str) -> list:
    proxies = config.proxies
    sp = cloudscraper.create_scraper()
    
    _resp = sp.get("https://ascii2d.net/search/url/" + url, timeout=15, proxies=proxies)
    _resp = await asyncio.get_running_loop().run_in_executor(None, partial(sp.get, "https://ascii2d.net/search/url/" + url, timeout=15, proxies=proxies))
    ascUrl: str = _resp.url
    if ascUrl.find("color") != -1:
        await resp.finish(Message.template("{str}").format(str="ascii2d被cloudflare五秒盾单防了，你加油"))
    ascUrl = ascUrl.replace("color", "bovw")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(ascUrl, headers=ascHeaders, proxy=proxies.get("http")) as response:
            html = await response.text()
    
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    for item in soup.select('.item-box')[1:]:
        
        thumbnail = "https://ascii2d.net" + item.select('.image-box img')[0]['src']
        datas = []
        info = item.select_one('.info-box .detail-box')
        if info.find('h6') is None:
            datas.append({
                'source': info.select_one('.external a')['href'],
                'title': info.select_one('.external').text,
                'author': info.select_one('.external a').text
            })
        else:
            for _info in info.select('h6'):
                datas.append({
                    'source': _info.select('a')[0]['href'],
                    'title': _info.select('a')[0].text,
                    'author': _info.select('a')[1].text
                })
        
        results.append({
            'thumbnail': thumbnail,
            'datas': datas
        })
    
    return results
