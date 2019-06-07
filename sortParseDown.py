from selenium import webdriver
from parseChannels import getVideosMetaData
from parseChannels import loadChannels
from videoDownload import videoDownload




#Goal is to get 10:00 worth of content sorted by number of views
#also try to avoid repeats -> avoid clips from the same stream

def differentStream(metaList, metaTuple):
    for i in metaList:
        if i[4] == metaTuple[4] and i[5] == metaTuple[5]:
            return False
    
    return True




def getAllVids():
    '''
    downloads 10 minutes worth of content, or until content runs out
    into the assets folder
    '''
    #get all of the metadata
    driver = webdriver.Chrome()   
    ChannelList = loadChannels()
    allMetaData = []



    for channel in ChannelList:
        allMetaData.extend(getVideosMetaData(driver, channel))

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
    
    for i in range(len(downloadList)):
        
        fName = downloadList[i][1] + '_' + downloadList[i][5] + '_'+str(downloadList[i][2]) + '_'+str(downloadList[i][3]) + '_'+downloadList[i][4] 
        
        videoDownload(downloadList[i][0], fName, driver)
    
    driver.close()    


if __name__ == "__main__":
    getAllVids()
  