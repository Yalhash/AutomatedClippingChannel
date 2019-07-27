import httplib2
import os

from googleapiclient.discovery import build
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload


# from apiclient.discovery import build
# from apiclient.errors import HttpError
# from apiclient.http import MediaFileUpload
# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.file import Storage
# from oauth2client.tools import argparser, run_flow

httplib2.RETRIES = 1
MAX_RETRIES = 10
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)
RETRIABLE_CODES = (500,  502, 503, 504)

CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")
MISSING_CLIENT_SECRETS_MSG = "missing client secrets :("
#mostly copied from youtube API example epic gamer style





def uploadVideo(file, title, description, category, keywords, privacyStatus):
      
    '''
    file: string, a valid file path
    title: string, the title of the video to upload (default => Test Title)
    category: int, the numeric video category
    keywords: string, keywords comma separated (ex: "a, b, c, d, ...")
    privacyStatus: idk (whether or not the video is privated)
    '''
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = 'something'
    
    youtube  = build('youtube', 'v3',credentials= credentials)

    return youtube
      
