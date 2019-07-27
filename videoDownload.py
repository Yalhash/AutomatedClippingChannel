from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

def getClipURL(driver):
    '''
    driver: a webdriver object that is on a clip page
    returns: a string containing the url of the source of the clip
    or None if it can't find the url
    '''
    try:
        vidElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "video")))
        return vidElem.get_attribute("src")
    except:
        return



def downloadFile(url, fileName):
    '''
    url: string, link to file to download
    fileName: string, name of file downloaded
    '''
    try:
        with open(fileName, "wb") as fOut:
                response = requests.get(url)
                fOut.write(response.content)
    except:
        return


def videoDownload(url, fileName, driver):
    '''
    url: a string to the url of the clip page that is to be downloaded
    fileName: the fileName that the file will be saved to 
    driver: a webdriver object
    (Don't put an extention on the filename)

    '''
    #options = webdriver.ChromeOptions()
    #options.headless = True
    #can't figure out headless options that work with the website, stopping for now

    driver.get(url)
    videoLink = getClipURL(driver)
    downloadFile(videoLink,"assets/"+fileName + ".mp4")
    


if __name__ == "__main__":      
    driver = webdriver.Chrome('')
    videoDownload("https://www.twitch.tv/ppmd/clip/DignifiedFineNeanderthalTakeNRG?filter=clips&range=7d&sort=time", "test", driver)

