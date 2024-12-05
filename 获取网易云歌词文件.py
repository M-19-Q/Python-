# 导入库
import re
import json
import requests
import os
from lxml import etree

# 歌词下载函数
def download_lyric(song_name, song_id):
    url = f'http://music.163.com/api/song/lyric?id={song_id}&lv=-1&kv=-1&tv=-1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Referer': 'https://music.163.com/',
        'Host': 'music.163.com'
    }
    res = requests.get(url=url, headers=headers).text
    tree = etree.HTML(res)

    artist_name_tree = tree.xpath('//h2[@id="artist-name"]/text()')
    artist_name = str(artist_name_tree[0]) if artist_name_tree else None

    song_list_name_tree = tree.xpath('//h2[contains(@class,"f-ff2")]/text()')
    song_list_name = str(song_list_name_tree[0]) if song_list_name_tree else None

    try:
        res = requests.get(url, headers=headers).json()

        # 检查是否有歌词
        if 'lrc' not in res or 'lyric' not in res['lrc']:
            print(f"歌曲 '{song_name}' 没有歌词数据")
            return

        # 获取歌词
        lyric = res['lrc']['lyric']

        # 清理歌词中的时间戳
        reg = re.compile(r'\[.*\]')
        lrc_text = re.sub(reg, '', lyric).strip()

        folder_name='./'+song_name

        # 确保歌词文件夹存在
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)

            # 保存歌词到文件
            file_path = os.path.join(folder_name, f'{song_name}.lrc')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(lrc_text)
                print(f"歌词已保存到：{file_path}")

    except Exception as e:
        print(f"下载歌曲 '{song_name}' 时发生错误：{e}")


# 获取歌单中的歌曲ID
def get_playlist_songs(playlist_id):
    url = f'https://music.163.com/api/playlist/detail?id={playlist_id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Referer': 'https://music.163.com/',
        'Host': 'music.163.com'
    }

    res = requests.get(url, headers=headers).text
    json_obj = json.loads(res)

    # 获取歌单中的歌曲列表
    songs = json_obj['result']['tracks']
    return [(song['name'], song['id']) for song in songs]


# 下载整个歌单的歌词
def download_playlist_lyrics(playlist_id):

    songs = get_playlist_songs(playlist_id)

    for song_name, song_id in songs:
        download_lyric(song_name, song_id)


if __name__ == '__main__':
    playlist_id = 你的目标歌单id  # 这里是歌单ID，替换为你需要下载歌词的歌单ID
    download_playlist_lyrics(playlist_id)
