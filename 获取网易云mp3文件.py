#导入库
import re
import json
import requests
import os
from lxml import etree #lxml是一个库，etree是其中的一个模块。

def download_songs(url=None):
    if url is None:
        url = 'https://music.163.com/#/playlist?id=你的目标歌单id'

    url = url.replace('/#', '').replace('https', 'http')  # 对字符串进行去空格和转协议处理

    out_link = 'http://music.163.com/song/media/outer/url?id='
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Referer': 'https://music.163.com/',
        'Host': 'music.163.com'
    }
    # 请求页面的源码
    res = requests.get(url=url, headers=headers).text

    tree = etree.HTML(res)
    # 音乐列表
    song_list = tree.xpath('//ul[@class="f-hide"]/li/a')

    # 如果是歌手页面
    artist_name_tree = tree.xpath('//h2[@id="artist-name"]/text()')
    artist_name = str(artist_name_tree[0]) if artist_name_tree else None

    # 如果是歌单页面：
    #song_list_tree = tree.xpath('//*[@id="m-playlist"]/div[1]/div/div/div[2]/div[2]/div/div[1]/table/tbody')
    song_list_name_tree = tree.xpath('//h2[contains(@class,"f-ff2")]/text()')
    song_list_name = str(song_list_name_tree[0]) if song_list_name_tree else None

    # 设置音乐下载的文件夹为歌手名字或歌单名
    folder = './' + artist_name if artist_name else './' + song_list_name


    if not os.path.exists(folder):
        os.mkdir(folder)
        #这一步目的是检查指定的文件夹folder是否存在。如果文件夹不存在，则使用os.mkdir()创建该文件夹。

    for i, s in enumerate(song_list):
        href = str(s.xpath('./@href')[0])
        song_id = href.split('=')[-1]
        src = out_link + song_id  #将 ut_link和 ong_id拼接，形成实际的歌曲下载链接src。
        title = str(s.xpath('./text()')[0]) #提取歌曲名
        filename = title + '.mp3' #构造文件名，将歌曲名称加上 .mp3 后缀，作为文件名保存。
        filepath = folder + '/' + filename #将 folder（文件夹路径）和 filename（歌曲文件名）拼接起来，形成完整的文件路径。
        print(f'开始下载第{i + 1}首音乐：{filename}\n')
        #这个循环用于遍历song_list中的每一首歌曲，并为每首歌曲构造下载链接、文件名和文件路径。



        try:  # 下载音乐

            data = requests.get(src).content  # 音乐的二进制数据

            with open(filepath, 'wb') as f:
                f.write(data)
        except Exception as e:
            print(f"下载错误：{e}")
            #这部分代码负责下载每首歌曲，并将其保存到指定路径。

    print(f'{len(song_list)}首全部歌曲已经下载完毕！')

if __name__ == '__main__':
    playlist_id = 你的目标歌单id  # 这里是歌单ID，替换为你需要下载歌词的歌单ID
    download_songs(f'https://music.163.com/playlist?id={playlist_id}')
