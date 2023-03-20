import glob

import os
import time
from selenium import webdriver


OUT_DIR = '/home/cotton/Workspace/download/apks/'

header = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0"
}

'''
Question: This type of file can harm your computer, do you still want to keep it?
Solution:  "safebrowsing.enabled": True
'''

# https://d.apkpure.com/b/APK/org.vlada.droidtesla?version=latest


baseurl = 'https://d.apkpure.com/b/APK/'

def parse_pkg_names(fname):
    pkgs = set()
    with open(fname, 'r') as f:
        for line in f:
            name = line.split("/")[-2]
            pkgs.add(name)
    return pkgs


def download_wait(directory, timeout=300, nfiles=None):
    """
    Wait for downloads to finish with a specified timeout.

    Args
    ----
    directory : str
        The path to the folder where the files will be downloaded.
    timeout : int
        How many seconds to wait until timing out.
    nfiles : int, defaults to None
        If provided, also wait for the expected number of files.

    """
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        time.sleep(1)
        dl_wait = False
        files = os.listdir(directory)
        if nfiles and len(files) != nfiles:
            dl_wait = True

        for fname in files:
            if fname.endswith('.crdownload'):
                dl_wait = True

        seconds += 1
    return seconds
    

def download_app(fname):
    count = 0
    pkgs = parse_pkg_names(fname)
    for pkg in pkgs:
        dl = baseurl + pkg + "?version=latest"
        apk_folder = OUT_DIR + pkg
        if not os.path.isdir(apk_folder):
            os.mkdir(apk_folder)
        if glob.glob(apk_folder+"/*.apk"):
            print(f"{pkg} has been downloaded. Continue")
            continue
        count += 1
        print(f"Start to download {pkg}, count={count}")
        option = webdriver.ChromeOptions()
        pref = {
            "download.default_directory": apk_folder, 
            "safebrowsing.enabled": True
        }
        option.add_experimental_option("prefs", pref)
        driver = webdriver.Chrome(options=option)
        driver.get(dl)
        download_wait(apk_folder)
        driver.quit()
        time.sleep(5)


if __name__ == '__main__':
    download_app("./raw_urls.txt")
