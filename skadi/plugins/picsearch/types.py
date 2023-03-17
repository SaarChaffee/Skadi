from typing import Dict, List, Optional
from pydantic import BaseModel


class Index(BaseModel):
    status: Optional[int]
    parent_id: Optional[int]
    id: Optional[int]
    results: Optional[int]


class Header(BaseModel):
    user_id: str
    account_type: str
    short_limit: str
    long_limit: str
    long_remaining: int
    short_remaining: int
    status: int
    results_requested: int
    index: Dict[str, Index]
    search_depth: str
    minimum_similarity: float
    query_image_display: str
    query_image: str
    results_returned: int


class ResultHeader(BaseModel):
    similarity: str
    thumbnail: str
    index_id: int
    index_name: str
    dupes: int
    hidden: int


class Result(BaseModel):
    header: ResultHeader
    data: BaseModel
    
    def __init__(self, **data):
        index_id = data['header']['index_id']
        data_model = data_models[index_id]['model']
        if data_model:
            data['data'] = data_model(**data['data'])
        super().__init__(**data)


class JsonData(BaseModel):
    header: Header
    results: List[Result]


class DeliciousSauce(BaseModel):
    title: str
    author: str
    source: str


class PixivData(BaseModel):
    ext_urls: List[str]
    title: str
    pixiv_id: int
    member_name: str
    member_id: int


class YandeData(BaseModel):
    ext_urls: List[str]
    yandere_id: int
    creator: str
    material: str
    characters: str
    source: str


class DanbooruData(BaseModel):
    ext_urls: List[str]
    danbooru_id: int
    gelbooru_id: int
    creator: str
    material: str
    characters: str
    source: str


class AnimeData(BaseModel):
    ext_urls: List[str]
    source: str
    anidb_aid: int
    mal_id: int
    anilist_id: int
    part: str
    year: str
    est_time: str


class HAnimeData(BaseModel):
    ext_urls: List[str]
    source: str
    anidb_aid: int
    part: str
    year: str
    est_time: str


class GelbooruData(BaseModel):
    ext_urls: List[str]
    gelbooru_id: int
    creator: str
    material: str
    characters: str
    source: str


class Konachan(BaseModel):
    ext_urls: List[str]
    konachan_id: int
    creator: str
    material: str
    characters: str
    source: str


class AnimePicturesData(BaseModel):
    ext_urls: List[str]
    pictures_id: int
    creator: str
    material: str
    characters: str
    source: str
    
    def __init__(self, **data):
        if data.get('anime-pictures_id'):
            self.pictures_id = data.pop('anime-pictures_id')
        super().__init__(self, data)


class ArtStationData(BaseModel):
    ext_urls: List[str]
    title: str
    as_project: str
    author_name: str
    author_url: str


class TwitterData(BaseModel):
    ext_urls: List[str]
    tweet_id: int
    created_at: str
    twitter_user_id: str
    twitter_user_handle: str


class KemonoData(BaseModel):
    ext_urls: List[str]
    published: str
    title: str
    service: str
    service_name: str
    id: str
    user_id: str
    user_name: str


data_models: Dict = {
    5: {'model': PixivData, 'title': 'title', 'author': 'member_name'},
    9: {'model': DanbooruData, 'title': 'characters', 'author': 'creator'},
    12: {'model': YandeData, 'title': 'characters', 'author': 'creator'},
    21: {'model': AnimeData, 'title': 'source', 'author': 'est_time'},
    22: {'model': HAnimeData, 'title': 'source', 'author': 'est_time'},
    25: {'model': GelbooruData, 'title': 'characters', 'author': 'creator'},
    26: {'model': Konachan, 'title': 'characters', 'author': 'creator'},
    28: {'model': AnimePicturesData, 'title': 'characters', 'author': 'creator'},
    39: {'model': ArtStationData, 'title': 'title', 'author': 'author_name'},
    41: {'model': TwitterData, 'title': 'created_at', 'author': 'twitter_user_handle'},
    43: {'model': KemonoData, 'title': 'title', 'author': 'user_name'},
}

headers = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'saucenao.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}