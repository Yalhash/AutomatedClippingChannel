import os
import urllib.request, urllib.parse, urllib.error
import http.client
import httplib2
import random
import time
import google.oauth2.credentials
import google_auth_oauthlib.flow #?

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload


#https://www.geeksforgeeks.org/youtube-data-api-for-handling-videos-set-3/
#^^ Tutorial to continue

#consts:
CLIENT_SECRETS = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

httplib2.RETRIES = 1
MAX_RETRIES = 1
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, 
                        IOError,
                        http.client.NotConnected,
                        http.client.IncompleteRead,
                        http.client.ImproperConnectionState,
                        http.client.CannotSendHeader,
                        http.client.CannotSendRequest,
                        http.client.ResponseNotReady,
                        http.client.BadStatusLine)
#server errors
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS, SCOPES)
    credentials = flow.run_console()
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)


def resumable_upload(request, resource, method):
    response = None
    error = None
    retry = 0

    while response is None:
        try: 
            print("Uploading...")
            status, response = request.next_chunk()

            if response is not None:
                if method == "insert" and 'id' in response:
                    print(response)
                elif method != "insert" or 'id' not in response:
                    print(response)
                else:
                    exit("The file upload failed with an unexpected repsponse: %s" % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occured:\n%s" % (e.resp.status, e.content)
            else:
                raise 
        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occured: %s" % e

        if error is not None:
            print(error)
        retry += 1

        if retry > MAX_RETRIES:
            exit("No longer attempting to retry.")
        max_sleep = 2**retry

        sleep_seconds = random.random() * max_sleep

        print("Sleeping", sleep_seconds, "seconds and then retrying...")

        time.sleep(sleep_seconds)
    
def print_response(response):
    print(response)

def build_resource(properties):
    resource = {}
    for p in properties:

        prop_array = p.split('.')
        ref = resource
        for pa in range(0, len(prop_array)):
            is_array = False
            key = prop_array[pa]
            if key[-2:] == '[]':
                key = key[0:len(key-2):]
                is_array = True
            
            if pa == (len(prop_array) -1):
                if properties[p]:
                    if is_array:
                        ref[key] = properties[p].split(', ')
                    else:
                        ref[key] = properties[p]
            elif key not in ref:
                ref[key] = {}
                ref = ref[key]
            else:
                ref = ref[key]
        return resource


def remove_empty_kwargs(**kwargs): 
    good_kwargs = {} 
      
    if kwargs is not None: 
        for key, value in list(kwargs.items()): 
            if value: 
                good_kwargs[key] = value 
    return good_kwargs 


def videos_insert(client, properties, media_file, **kwargs):
    resource = build_resource(properties)
    kwargs = remove_empty_kwargs(**kwargs)
    request = client.videos().insert(body = resource,
                                    media_body = MediaFileUpload(
                                                media_file,
                                                chunksize = -1,
                                                resumable = True), **kwargs)
    return resumable_upload(request, 'video', 'insert')





#not needed for upload
def video_details(vid_id):
    #calls videos.list method
    list_videos_byid = youtube.videos().list(id = vid_id,
        part = "id, snippet, contentDetails, statistics").execute()
    results = list_videos_byid.get("items", [])

    print(results)




if __name__ == "__main__":        
    # When running locally, disable OAuthlib's 
    # HTTPs verification. When running in production 
    # * do not * leave this option enabled. 
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    client = get_authenticated_service() 
    media_file = 'assets/l0l_ppmd_5_22_21-hours-ago.mp4'
      
    if not os.path.exists(media_file): 
        exit('Please specify the complete valid file location.') 
      
    videos_insert(client,  
        {'snippet.categoryId': '27', 
        'snippet.defaultLanguage': '', 
        'snippet.description': 'deskciprtion', 
        'snippet.tags[]': '', 
        'snippet.title': 'YEEEETEST', 
        'status.embeddable': '', 
        'status.license': '', 
        'status.privacyStatus': 'private', 
        'status.publicStatsViewable': ''}, 
        media_file, 
        part ='snippet, status') 

