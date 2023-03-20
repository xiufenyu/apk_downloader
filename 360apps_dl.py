'''
* Description:
* This script is used to download Chinese apps from 360 mobile assistant app store
* 此脚本是360手机助手自动下载应用软件
'''

from bs4 import BeautifulSoup
import requests
import urllib
import os
import time

CATEGORIES = {
    'newest': 'newest',
    'week': 'weekdownload',
    'download': 'download',
    'hotList': 'poll'
}

# Todo: This should be changed to Sajjad output dir
OUT_DIR = './'

header = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0"
}


class GetApp:
    def __init__(self):
        self.urllist = []
        self.count = 0
        self.baseurl = 'https://zhushou.360.cn/list/index/cid/1/order/'

    def get_urls(self, type, max_page):
        for index in range(1, max_page+1):
           self.urllist.append(self.baseurl+type+'/?' + 'page='+str(index))

    def download_app(self):
        for url in self.urllist:
            print(f'Browse {url}')
            response = requests.get(url, headers=header)
            soup = BeautifulSoup(response.content, 'html.parser')
            # print(soup.prettify())
            iconList = soup.find_all("ul", {"class": "iconList", "id":"iconList"})
            for li in iconList:
                a_elems = li.find_all("a", href=True)
                for a in a_elems:
                    href = a['href']
                    if '.apk' in href:
                        url = self._get_app_url(href)
                        apk_name = self._get_apk_name(url)
                        self._download_apk(url, apk_name)
                        self.count = self.count + 1
                        time.sleep(5)


    def _get_app_url(self, href):
        params = href.split('&')
        # remove 'url='
        url = params[-1][4:]
        print("apk url is: ", url)
        return url

    def _get_apk_name(self, url):
        result = ""
        items = url.split('/')
        for item in items:
            if '.apk?' in item:
                result = item.split('?')[0]
                break
        print("apk name: ", result)
        return result


    def _download_apk(self, url, apk_name):
        index = apk_name.find('.apk')
        download_folder = OUT_DIR + "/" + apk_name[0: index] + "/"
        print("download folder:" + download_folder)
        if not os.path.isdir(download_folder):
            os.mkdir(download_folder)
            os.system(f"aria2c -x8 '{url}' -d {download_folder}" + " -o base.apk")
            # remove additional file
            rm_file = download_folder + "*.aria2"
            if os.path.exists(rm_file):
                os.remove(download_folder + "*.aria2")


if __name__ == '__main__':
    a = GetApp()
    a.get_urls(CATEGORIES['download'], 2)
    a.download_app()
