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


def loadChannels():
    '''
    returns a list of all the channels in the channels.csv file
    '''
    with open("channels.csv") as channelFile:
        return channelFile.read().split(',')

def getClipPage(name):
    '''
    name: string, twitch username of a creator 
    returns: the url of the creator's clips page from the pas 7 days
    '''
    return "https://www.twitch.tv/"+ name +"/clips?filter=clips&range=7d"

def sanitizeViews(viewString):
    '''
    viewString: string, contains the raw viewString
    returns: an integer containing an approx to views
    '''
    viewPart = viewString.split()[0].replace('.', '')
    if viewPart[-1] == 'K':
        viewPart = viewPart[:-1] + '000'
    return int(viewPart)

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
        title = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xPath+'/div/div[2]/div[2]/div/a/h3'))).text
        lengthString = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xPath+'/div/div[1]/a/div[2]/div[1]/div/p'))).text
        viewString = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xPath+'/div/div[1]/a/div[2]/div[3]/div/p'))).text
        dayString = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xPath+'/div/div[1]/a/div[2]/div[4]/div/p'))).text
    except:
        return
    views = sanitizeViews(viewString)
    days = '-'.join(dayString.split())
    length = getSeconds(lengthString)
    return (link, title, length, views, days, name)
    
# head of clip tree vvv



def getVideosMetaData(driver, creatorName):
    '''
    driver: a webdriver object
    creatorName: string, the channel name to get clips from
    returns: a list of tuples containing the metadata for each video on the clips page
    format: (link, title, length, views, days, name of channel)
    '''
    dataList = []
    driver.get(getClipPage(creatorName))
    i = 1
    temp = ()

    while (temp != None):
        temp = getMetaData('//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div/div/div[2]/div/div/div[1]/div/div/div/div['+ str(i) +']', driver, creatorName) 
        if (temp != None):
            dataList.append(temp)
            i += 1
    return dataList




if __name__ == "__main__":
    # CREATORLIST = loadChannels()
    # driver = webdriver.Chrome()   
    # print(getVideosMetaData(driver, CREATORLIST[1]))
    # driver.close()
    print(getSeconds("1:30"))