from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
from requests.exceptions import ConnectTimeout

def get_clip_url(driver):
    '''
    driver: a webdriver object that is on a clip page
    returns: a string containing the url of the source of the clip
    or None if it can't find the url
    '''
    try:
        vid_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )
        return vid_elem.get_attribute("src")
    except TimeoutException as ex:
        print("failed to get clip URL:", ex)
        return

def get_whitelisted_file_name(file_name):
    '''
        whitelist certain characters, replace all others w/ '_'
    '''
    whitelist = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')
    return ''.join(map(lambda c: c if c in whitelist else '_', file_name))

def get_clean_unique_file_name(file_name, known_files):
    '''
    file_name: name of file to clean and uniquify
    known_files: set of all known file names to avoid
    '''
    clean_name = get_whitelisted_file_name(file_name)

    ind = 1
    unique_name = clean_name
    while unique_name in known_files:
        unique_name =  clean_name + '_' + str(ind)
        ind = ind + 1

    return unique_name


def download_file(url, file_name):
    '''
    url: string, link to file to download
    file_name: string, name of file downloaded
    '''
    try:
        with open(file_name, "wb") as f_out:
            response = requests.get(url, timeout=10)
            f_out.write(response.content)
    except ConnectTimeout:
        print(f"timed out while downloading: {url}, {file_name}")


def videoDownload(url, file_name, driver, known_files):
    '''
    url: a string to the url of the clip page that is to be downloaded
    file_name: the file_name that the file will be saved to 
    driver: a webdriver object
    (Don't put an extention on the file_name)

    '''
    #options = webdriver.ChromeOptions()
    #options.headless = True
    #can't figure out headless options that work with the website, stopping for now

    driver.get(url)

    print("at url:", url)
    video_link = get_clip_url(driver)
    print("link:", video_link)
    clean_file = get_clean_unique_file_name(file_name, known_files)

    download_file(video_link,"assets/" + clean_file + ".mp4")
    return clean_file


if __name__ == "__main__":
    ops = Options()
    ops.add_argument("headless")
    driver = webdriver.Chrome(options=ops)
    known_files = set()
    videoDownload(
        "https://www.twitch.tv/leffen/clip/PlainCallousBearCharlietheUnicorn"\
        "-l446II6_7VfaeyPp?filter=clips&range=7d&sort=time", 
        "test", 
        driver,
        known_files
    )
    driver.close()
