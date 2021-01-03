# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests # to get image from the web
import shutil # to save it locally

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def extract_thumbnails(youtube):
    bbb_channel_id = "UC5CwAZoYHlI4isp0llzZCIA"
    uploads_playlist_id = "UU5CwAZoYHlI4isp0llzZCIA"

    request = youtube.playlistItems().list(
        part="id, snippet",
        playlistId=uploads_playlist_id,
        maxResults=50
    )
    
    # request = youtube.playlists().list(
    #     part="id, contentDetails, snippet",
    #     channelId=bbb_channel_id,
    #     maxResults=50
    # )
    
    # request = youtube.channels().list(
    #     part="snippet,contentDetails,statistics",
    #     id=bbb_channel_id
    # )
    response = request.execute()

    for video in response['items']:
        video_id = video['id']
        video_title = video['snippet']['title']
        print (video_id)
        print (video_title)
        try:
            video_thumbnail_url = video['snippet']['thumbnails']['maxres']['url']
            print ('maxres')
        except:
            video_thumbnail_url = video['snippet']['thumbnails']['high']['url']
            print ('high')

        print (video_thumbnail_url)
        image_url = video_thumbnail_url
        r = requests.get(image_url, stream = True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
         # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
    
        # Open a local file with wb ( write binary ) permission.
        filename = video_id + ".jpg"
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
        
        print('Image sucessfully Downloaded: ',filename)

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    api_key = os.environ["API_KEY"]


    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)

    extract_thumbnails (youtube)





if __name__ == "__main__":
    main()