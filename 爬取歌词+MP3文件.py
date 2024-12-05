#导入库
import re
import json
import requests
import os
from lxml import etree #lxml是一个库，etree是其中的一个模块。

def download_songs(url=None): #定义叫做download_songs的函数，函数的目的是处理一个可选的URL参数。且调用该函数时若没有传入URL参数，则URL将自动赋值为None。
    #URL中文名叫统一资源定位符，是一种用于在互联网上定位和访问资源的地址。简单来说，URL 就是你在浏览器中输入的网址。
    #它指向一个具体的资源或服务，比如网页、图片、视频、文件等。
    #https://www.example.com：这是一个简单的网页 URL，通过这个地址，你可以访问 example.com 网站的首页。
    #https://www.example.com/search?q=python：这个 URL 用于在 example.com 网站上执行搜索操作，查询关键词是 python。
    #https://music.163.com/#/playlist?id=2384642500：这是网易云音乐的一个歌单页面，其中 id=2384642500 是查询参数，指向特定的歌单。
    if url is None:
        url = 'https://music.163.com/#/playlist?id=你的目标歌单id'

    url = url.replace('/#', '').replace('https', 'http')  # 对字符串进行去空格和转协议处理
    # 网易云音乐外链url接口：http://music.163.com/song/media/outer/url?id=xxxx，其中 xxxx 代表歌曲的 ID。当你替换这xxxx为实际的歌曲ID时，你就能生成一个可以直接播放该歌曲的URL。
    out_link = 'http://music.163.com/song/media/outer/url?id='
    # 请求头
    #User-Agent：设置浏览器的标识信息，通常用于模拟浏览器的请求头。
    #'Mozilla/5.0 ... Safari/537.36' 表示这是一个来自桌面版浏览器（如 Chrome）的请求，告诉服务器这是一个真实的浏览器请求。很多网站都会检查请求的 User-Agent，以防止自动化请求或爬虫程序。
    #Referer：表示从哪个页面发起的请求。在这个例子中，设置了 'https://music.163.com/'，即请求是从网易云音乐的主页发出的。某些网站会检查 Referer，以确保请求是从合法的页面发出的。
    #Host：表示请求的目标主机。这里是 music.163.com，即请求的是网易云音乐的网站。
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Referer': 'https://music.163.com/',
        'Host': 'music.163.com'
    }
    # 请求页面的源码
    res = requests.get(url=url, headers=headers).text
    #requests.get(url=url, headers=headers)：使用Python的requests库发起一个GET请求，访问指定的url并且在请求中传递了自定义的请求头headers。
    #headers包含了浏览器的用户代理、引用页面等信息（防止被识别为爬虫程序）。
    #.text：requests.get() 返回的响应对象包含网页的各种信息，其中.text属性提取出网页的HTML源代码，以文本格式返回。这是接下来用于解析的HTML内容。

    tree = etree.HTML(res) #etree.HTML(res) 解析一个 HTML 文本（假设 res 是 HTML 的字符串）并将其转化为一个 ElementTree 对象，tree 变量将存储这个对象。这使得后续代码可以通过 XPath 查询来提取 HTML 中的元素和数据。
    # 音乐列表
    song_list = tree.xpath('//ul[@class="f-hide"]/li/a')
    #//ul[@class="f-hide"]：查找 class 属性为 f-hide 的所有 <ul> 标签。
    #/li/a：从这个 <ul> 标签中，进一步查找每个 <li> 元素中的 <a> 标签（每个 <a> 标签通常包含一个链接，指向歌曲的具体页面或下载地址）。
    #这将返回一个包含所有 <a> 标签的列表，song_list 存储这些标签，通常每个标签包含歌曲的名称和链接。

    # 如果是歌手页面
    artist_name_tree = tree.xpath('//h2[@id="artist-name"]/text()')
    artist_name = str(artist_name_tree[0]) if artist_name_tree else None

    # 如果是歌单页面：
    #song_list_tree = tree.xpath('//*[@id="m-playlist"]/div[1]/div/div/div[2]/div[2]/div/div[1]/table/tbody')
    song_list_name_tree = tree.xpath('//h2[contains(@class,"f-ff2")]/text()')
    song_list_name = str(song_list_name_tree[0]) if song_list_name_tree else None

    # 设置音乐下载的文件夹为歌手名字或歌单名
    folder = './' + artist_name if artist_name else './' + song_list_name
    #folder = './' + artist_name if artist_name else './' + song_list_name 采用条件表达式（或称三元表达式）。如果 artist_name 存在，folder 就是 './' 加上歌手的名字；否则，folder 就是 './' 加上歌单的名字。

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


# 歌词下载函数
def download_lyric(song_name, song_id):
    url = f'http://music.163.com/api/song/lyric?id={song_id}&lv=-1&kv=-1&tv=-1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Referer': 'https://music.163.com/',
        'Host': 'music.163.com'
    }
    try:
        res = requests.get(url, headers=headers).json()
        lyric = res['lrc']['lyric']

        # 清理歌词中的时间戳
        reg = re.compile(r'\[.*\]')
        lrc_text = re.sub(reg, '', lyric).strip()

        # 打印歌词信息
        print(f"歌曲：{song_name}\n歌词：{lrc_text}\n")

        # 保存歌词到文件
        with open(f'./{song_name}.lrc', 'w', encoding='utf-8') as f:
            f.write(lrc_text)
    except Exception as e:
        print(f"下载歌词错误：{e}")


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
    download_songs(f'https://music.163.com/playlist?id={playlist_id}')
