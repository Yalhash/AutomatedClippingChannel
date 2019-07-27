from sortParseDown import getAllVids
from editVideo import makeVideo
import os

def clearAssets():
    '''
    deletes all old videos from assets
    basically want to do rm *.mp4
    '''
    assets = 'assets'
    for file in os.listdir(assets):
        path = os.path.join(assets, file)
        try:
            if os.path.isfile(path) and (path[-4:] == '.mp4' or path[-4:] == '.txt' or path[-4:] == '.ass'):
                os.unlink(path)
        except Exception as e:
            print(e)





if __name__ == "__main__":
    clearAssets()
    fileNames = getAllVids()
    makeVideo(fileNames)
    clearAssets()
