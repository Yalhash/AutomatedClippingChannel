from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# notes: 
# tw-tower is the class name of the thing that holds all of the clips
# we want to retrieve from each of the videos: 
#   - title
#   - length
#   - views
#   - number of days ago

# above are reffered to as video meta-data


def getClipPage(name):
    '''
    name: string, twitch username of a creator 
    returns: the url of the creator's clips page from the pas 7 days
    '''
    return "https://www.twitch.tv/"+ name +"/clips?filter=clips&range=7d"

def sanitizeViews(viewString):
    '''
    viewString: string, contains the raw view count
    returns: an integer containing an approx to views
    '''
    viewPart = viewString.split()[0].replace('.', '')
    if viewPart[-1] == 'K':
        viewPart = viewPart[:-1] + '000'
    return int(viewPart)

def sanitizeTitle(titleString):
    '''
    titleString: string, contains the raw title
    returns: string, same as given titles, but with the characters:
    '"\/|     all removed
    '''
    return titleString.replace('\'', '').replace('"', '').replace('\\', '').replace('/', '').replace('|', '')

def getSeconds(lengthString):
    '''
    lengthString: string, contains time in 'min:sec' format
    returns: int, total seconds of the time given
    '''
    splitStr = lengthString.split(':')
    return int(splitStr[0])*60 + int(splitStr[1])

def getMetaData(xPath, driver, name):
    '''
    xPath: string, xPath to the div containing the preview thing
    driver: a webdriver on a creators clips page
    return: a tuple:
        (link,
        title,
        length,
        views,
        days past,
        channel name)
    or None if the xPath doesn't lead to a div containing the information needed
    '''
    try:
        link = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xPath+'/div/div/a'))).get_attribute('href')
        titleString = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xPath+'/div/div[2]/div[2]/div/a/h3'))).text
        lengthString = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xPath+'/div/div[1]/a/div[2]/div[1]/div/p'))).text
        viewString = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xPath+'/div/div[1]/a/div[2]/div[3]/div/p'))).text
        dayString = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xPath+'/div/div[1]/a/div[2]/div[4]/div/p'))).text
    except:
        return
    title = sanitizeTitle(titleString)
    views = sanitizeViews(viewString)
    days = '-'.join(dayString.split())
    length = getSeconds(lengthString)
    return (link, title, length, views, days, name)
    
# head of clip tree vvv

def isCorrectGame(driver, correctGame, xPath):
    '''
    driver: a webdriver object
    correctGame: a string representing the game which you want to download
    used to avoid downloading clips from games that are not what we want
    returns True if the game matches, False otherwise
    Or None if the game cannot be found
    '''
    try: 
        return correctGame == WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.XPATH, xPath +'/div/div[2]/div[1]/div/a/div/div/img'))).get_attribute('alt')
    except:
        return
def getVideosMetaData(driver, creatorName, gameName):
    '''
    driver: a webdriver object
    creatorName: string, the channel name to get clips from
    gameName: string, the game to get clips from
    returns: a list of tuples containing the metadata for each video on the clips page
    format: (link, title, length, views, days, name of channel)
    '''
    dataList = []
    driver.get(getClipPage(creatorName))
    i = 1
    temp = ()

    while (temp != None):
        currXPath = '//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div/div/div[2]/div/div/div[1]/div/div/div/div['+ str(i) +']'
                    
        temp = getMetaData(currXPath, driver, creatorName) 
        if (temp != None):
            if isCorrectGame(driver, gameName, currXPath):
                dataList.append(temp)
        i += 1
    return dataList




if __name__ == "__main__":
    
    driver = webdriver.Chrome()
    print(getVideosMetaData(driver, 'leffen', 'Super Smash Bros. Melee'))
    
    
    driver.close()