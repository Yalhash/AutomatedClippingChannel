import os

from sortParseDown import get_all_vids
from editVideo import make_video

def clear_assets():
    '''
    deletes all old videos from assets
    basically want to do rm *.mp4
    '''
    assets = 'assets'
    for file in os.listdir(assets):
        path = os.path.join(assets, file)

        try:

            if os.path.isfile(path) and (
                path[-4:] == '.mp4' or path[-4:] == '.txt' or path[-4:] == '.ass'
            ):
                os.unlink(path)

        except Exception as ex:
            print("Failure during asset cleanup:", ex)

if __name__ == "__main__":

    clear_assets()

    meta_data_list = get_all_vids()
    assert len(meta_data_list) != 0
    finalVideoName = make_video(meta_data_list)
    # clear_assets()

    print("Final video:", finalVideoName)
