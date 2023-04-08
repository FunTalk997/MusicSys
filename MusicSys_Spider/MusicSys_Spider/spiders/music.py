import copy
import json
import re
import time
import requests
import scrapy
from MusicSys_Spider.items import MusicSysSpiderItem


class MusicSpider(scrapy.Spider):
    name = "music"
    allowed_domains = ["music.163.com", "1.12.238.164"]
    start_urls = ["https://music.163.com/", "http://1.12.238.164:30931/"]

    def __init__(self):
        self.table_name = 'music'
        self.table_fields = ['songName', 'singer', 'album', 'songTime', 'lyric', 'lyricist', 'picUrl', 'musicUrl']

    def parse(self, response):
        url = 'http://1.12.238.164:30931/playlist/detail?id=3778678'
        yield scrapy.Request(url=url, callback=self.second_parse)

    def second_parse(self, response):
        js = json.loads(response.text)
        songs = js['playlist']['tracks']
        item = MusicSysSpiderItem()
        for i in songs:
            item['songName'] = i['name']
            item['singer'] = ''
            for j in i['ar']:
                item['singer'] = item['singer'] + j['name'] + '/'
            item['album'] = i['al']['name']
            item['picUrl'] = self.upload('pic', i['al']['picUrl'])
            item['songTime'] = i['dt']
            lyric_url = 'https://music.163.com/api/song/lyric?id=%s&lv=-1' % (i['id'])
            yield scrapy.Request(url=lyric_url, callback=self.third_parse,
                                 meta={'item': copy.deepcopy(item), 'id': copy.deepcopy(i['id'])})

    def third_parse(self, response):
        js = json.loads(response.text)
        item = response.meta['item']
        id = response.meta['id']
        item['lyric'] = js['lrc']['lyric']
        try:
            lyricist = re.compile('作词.*?:(.*?)\n').findall(item['lyric'])[0].strip()
        except:
            lyricist = ''
        item['lyricist'] = lyricist
        music_url = 'https://music.163.com//api/song/enhance/player/url/v1?encodeType=flac&ids=[%s]&level=lossless' % (
            id)
        yield scrapy.Request(url=music_url, callback=self.fourth_parse, meta={'item': copy.deepcopy(item)})

    def fourth_parse(self, response):
        js = json.loads(response.text)
        item = response.meta['item']
        item['musicUrl'] = self.upload('music', js['data'][0]['url'])
        item['table_name'] = self.table_name
        item['table_fields'] = self.table_fields
        yield item

    def upload(self, file_type, url):
        file = requests.get(url)
        filename = str(round(time.time() * 1000))
        suffix = url.split('.')[-1]
        if file_type == 'pic':
            new_url = 'http://43.139.166.206/upload/music/picUrl/' + filename + '.' + suffix
        else:
            new_url = 'http://43.139.166.206/upload/music/musicUrl/' + filename + '.' + suffix
        response = requests.put(new_url, data=file.content)
        if response.status_code == 201:
            return new_url
        else:
            new_url = ''
            return new_url
