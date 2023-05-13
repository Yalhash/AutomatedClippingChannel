from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class MetaData:
    '''
        Metadata of videos, contains:
        title: a sanitized version of the title
        original_title: the original title for subtitles
        length: The video length in seconds as an int
        views: The number of views as an int
        time_passed: The time passed string
        channel_name: The channel name
        link: a link to the individual clip, not the video link
        file_name: The file name, which starts at nothing...
    '''

    def __init__(self, link, title, length, views, time_passed, channel_name):
        self.title = sanitize_title(title)
        self.original_title = title
        self.length = length
        self.views = views
        self.time_passed = time_passed
        self.channel_name = channel_name
        self.link = link
        self.file_name =  self.title + '_' + channel_name + '_' \
                            + str(length) + '_' + str(views) + '_' + time_passed

    def __str__(self):
        return self.channel_name + ":" + self.title

def sanitize_time_passed(time_passed_string):
    '''
    For now just joining the parts 
    '''
    return '-'.join(time_passed_string.split())

def sanitize_views(view_string):
    '''
    view_string: string, contains the raw view count
    returns: an integer containing an approx to views
    **Note: only parses strings with K's, any more or if it changes stuff breaks.
    '''
    view_part = view_string.split()[0].replace('.', '')
    if view_part[-1] == 'K':
        view_part = view_part[:-1] + '000'
    return int(view_part)

def sanitize_title(title_string):
    '''
    title_string: string, contains the raw title
    returns: string, same as given titles, but with the characters:
    '"\/|     all removed
    '''
    return ''.join(filter(lambda ch: ch not in '"\\/|', title_string))

def get_seconds(length_string):
    '''
    length_string: string, contains time in 'min:sec' format
    returns: int, total seconds of the time given
    '''
    split_str = length_string.split(':')
    return int(split_str[0])*60 + int(split_str[1])

def scroll_to_element(driver, element):
    '''
    driver: webDriver which is controlling a page
    element: an element on the page
    Scrolls to the element
    '''
    driver.execute_script("arguments[0].scrollIntoView(true);", element)


def get_meta_data(clip_selector, driver, name):
    '''
    clip_selector: string, css selector for the clip preview obj
    driver: a webdriver on a creators clips page
    return: a Metadata object
        or None if the selector doesn't lead to a div containing the metadata
    '''
    try:
        article = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, clip_selector))
        )
        scroll_to_element(driver, article)
        title = article.find_element_by_tag_name("h3").text
        link = article.find_element_by_css_selector(
            'a[data-a-target="preview-card-image-link"]'
        ).get_attribute("href")
        stats = list(map(
                lambda x: x.text, 
                article.find_elements_by_class_name("tw-media-card-stat")
            )
        )

        # Each article should have 3 stats
        assert len(stats) != 3

        view_string = None
        length_string = None
        time_passed_string = None
        for stat in stats:
            if "views" in stat:
                view_string = stat
            elif "ago" in stat or "day" in stat: # this covers hours, days or Yesterday
                time_passed_string = stat
            else:
                length_string = stat

        assert view_string is None
        assert time_passed_string is None
        assert length_string is None

    except TimeoutException:
        print("Unable to find an element!")
        return
    except AssertionError as ex:
        print("Assertion failed:", ex)
        return
    # print("title", title_string)
    # print("views", view_string)
    # print("days", time_passed_string)
    # print("length", length_string)
    views = sanitize_views(view_string)
    time_passed = sanitize_time_passed(time_passed_string)
    length = get_seconds(length_string)
    return MetaData(link, title, length, views, time_passed, name)

# NOTE: this function will likely be the cause on many issues
def get_clip_selector(index):
    '''
    index: the numerical index of the clip in question
    returns: the string which acts as a selector for the clip.
    THIS FUNCTION IS LIKELY TO BREAK.
    '''
    return '[data-a-target="clips-card-' + str(index) + '"] > article '

def get_clip_page(name):
    '''
    name: string, twitch username of a creator 
    returns: the url of the creator's clips page from the past day
    '''
    return "https://www.twitch.tv/"+ name +"/clips?filter=clips&range=7d"

def get_videos_meta_data(driver, channel_name):
    '''
    driver: a webdriver object
    channel_name: string, the channel name to get clips from
    returns: a list of MetaData objects for each video on the clips page
    '''
    # NOTE SOME RESTRICTION NEEDS TO BE PUT IN PLACE TO AVOID REPEAT CLIPS!
    data_list = []
    driver.get(get_clip_page(channel_name))
    i = 0
    # Goes through the list of videos by index and tries to find them, or until out of indices
    while True:
        clip_selector = get_clip_selector(i)
        temp_meta = get_meta_data(clip_selector, driver, channel_name)

        if temp_meta is None:
            print(f"Found {i} videos")
            break

        data_list.append(temp_meta)
        i += 1
    return data_list


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome()
    for mdata in get_videos_meta_data(driver, 'smallant'):
        print("\t\t" + str(mdata))
    driver.close()
