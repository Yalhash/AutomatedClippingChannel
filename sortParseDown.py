from selenium import webdriver
from parseChannels import getVideosMetaData
from videoDownload import videoDownload




#Goal is to get 10:00 worth of content sorted by number of views
#also try to avoid repeats -> avoid clips from the same stream

def loadGame():
    '''
    returns a string of the game we want to download from the game.txt file
    '''
    with open("game.txt") as gameFile:  
        return gameFile.read()

def loadChannels():
    '''
    returns a list of all the channels in the channels.csv file
    '''
    with open("channels.csv") as channelFile:
        return channelFile.read().split(',')



def differentStream(metaList, metaTuple):
    '''
    metaList: a list of metadata tuples
    metaTuple: an instance of metadata
    the function returns False if the channel name and date of the clip are equal,
    and True if they are not, 
    used to avoid downloading the same clip under a different name
    '''
    for i in metaList:
        if i[4] == metaTuple[4] and i[5] == metaTuple[5]:
            return False
    
    return True




def getAllVids():
    '''
    downloads 10 minutes worth of content, or until content runs out
    into the assets folder
    returns: a list of strings designating the filenames of each downloaded file, 
    sorted from most to least views
    '''
    #get all of the metadata
    driver = webdriver.Chrome()   
    ChannelList = loadChannels()
    gameName = loadGame()
    allMetaData = []



    for channel in ChannelList:
        allMetaData.extend(getVideosMetaData(driver, channel, gameName))

    #sort by views
    allMetaData.sort(key=lambda t: t[3], reverse=True)

    # take up to ten minutes of content
    # i.e the first x videos that add to 10 minutes 
    # or until content runs out
    TENMINS = 600
    totalTime = 0
    index = 0
    downloadList = []
    while(totalTime <= TENMINS and index < len(allMetaData)):
        if differentStream(downloadList, allMetaData[index]):
            downloadList.append(allMetaData[index])
            totalTime += allMetaData[index][2]
        index += 1
    fileList = []
    for i in range(len(downloadList)):
        
        fName = downloadList[i][1] + '_' + downloadList[i][5] + '_'+str(downloadList[i][2]) + '_'+str(downloadList[i][3]) + '_'+downloadList[i][4] 
        fileList.append(fName)
        videoDownload(downloadList[i][0], fName, driver)
    
    driver.close()  
    return fileList


if __name__ == "__main__":
    getAllVids()
  