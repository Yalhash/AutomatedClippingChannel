from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from parseChannels import get_videos_meta_data
from videoDownload import videoDownload

def load_channels(csv_file):
    '''
    returns a list of all the channels in the given csv file
    '''
    channels = []
    with open(csv_file, 'r', encoding='UTF-8') as channel_file:
        for line in channel_file.readlines():
            channels.extend(list(map(lambda x: x.strip(), line.split(','))))

    return channels


def is_unique_stream(candidate, final_list):
    '''
    candidate: a candidate for being included in video output
    final_list: a list of metadata objects
    The function returns true if the candidate is not from the same day and same channel
    used to avoid downloading the same clip under a different name
    '''
    for metadata in final_list:
        if metadata.channel_name == candidate.channel_name \
            and metadata.time_passed == candidate.time_passed:
            return False
    return True

def get_best_videos(metadata_list):
    '''
        metadata_list: list of all the metadata objects collects
        returns: list of metadata objects
        Gets 10+ minutes of video if the total length of the collected videos permits
        This should be the final list of videos to download
    '''
    # Sort by views to get the best vids first
    metadata_sorted = sorted(metadata_list, key=lambda t: t.views, reverse=True)

    ten_mins = 600
    total_time = 0

    index = 0
    final_list = []
    while total_time <= ten_mins and index < len(metadata_sorted):
        if is_unique_stream(metadata_sorted[index], final_list):
            final_list.append(metadata_sorted[index])
            total_time += metadata_sorted[index].length
        index += 1

    return final_list

def get_all_vids():
    '''
    gets all the links to video files
    returns: a list of video objects 
    '''
    #get all of the metadata
    ops = Options()
    # ops.add_argument("--headless")
    ops.add_argument("start-maximized")
    driver = webdriver.Chrome(options=ops)


    # Default csv is here, probably no need to change it
    channel_list = load_channels("channels.csv")
    all_meta_data = []
    print("Loading Metadata from:")
    for channel in channel_list:
        print("\t" + channel)
        all_meta_data.extend(get_videos_meta_data(driver, channel))

    # Make sure that we've found the video metadata
    # Twitch changes often which causes failures
    assert len(all_meta_data) != 0

    final_list = get_best_videos(all_meta_data)
    # Create the new file names and download them
    known_files = set()
    for meta_data in all_meta_data:
        file_name = meta_data.title + '_' + meta_data.channel_name + '_' \
            + str(meta_data.length) + '_' + str(meta_data.views) + '_'+ meta_data.time_passed
        meta_data.file_name = videoDownload(meta_data.link, file_name, driver, known_files)

    driver.close()
    return final_list

if __name__ == "__main__":
    get_all_vids()
