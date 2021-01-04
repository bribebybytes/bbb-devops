# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import sys

from PIL import Image, ImageDraw, ImageFilter
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests # to get image from the web
import shutil # to save it locally
from googleapiclient.http import MediaFileUpload

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def extractthumbnails(youtube):
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
        video_id = video['snippet']['resourceId']['videoId']
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
        filename = "old_thumbnails/" + video_id + ".jpg"
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
        
        print('Image sucessfully Downloaded: ',filename)

def inityt():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    print("import init..")
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    api_key = os.environ["API_KEY"]


    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)
    
    return youtube
    # extract_thumbnails (youtube)

def initmyyt():
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    print("import init..")
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    api_key = os.environ["API_KEY"]
    client_secrets_file = "client_secret_1002389841116-38gd581bddjmvgrhv5o7sf0ljro9qjn3.apps.googleusercontent.com.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version,  credentials=credentials)
    
    return youtube

def image_paste_over (layer1_img, layer2_img, where="top_left"):
    x = 0
    y = 0
    img1 = Image.open(layer1_img)
    img2 = Image.open(layer2_img)
    back_im = img1.copy()
    img2_copy = img2.copy()
    if (where == "top_left"):
        back_im.paste(img2_copy.resize((int(img2_copy.width / 2), int(img2_copy.height / 2))), (x, y))
    elif (where == "bottom_left"):
        y = (int(back_im.height) - int(img2_copy.height / 2))
        back_im.paste(img2_copy.resize((int(img2_copy.width / 2), int(img2_copy.height / 2))), (x, y))
    elif (where == "top_right"):
        x = (int(back_im.width) - int(img2_copy.width / 2))
        back_im.paste(img2_copy.resize((int(img2_copy.width / 2), int(img2_copy.height / 2))), (x, y))
    elif (where == "bottom_right"):
        y = (int(back_im.height) - int(img2_copy.height / 2))
        x = (int(back_im.width) - int(img2_copy.width / 2))
        back_im.paste(img2_copy.resize((int(img2_copy.width / 2), int(img2_copy.height / 2))), (x, y)) 
    else :
        print ("So where do want it? Choose between top_left, bottom_left")

    new_path = "new_thumbnails/" + img1.filename 
    back_im.save(new_path, quality=95)


def patch_contest(where):
    
        print ("processing " + where)
        directory_in_str = "old_thumbnails/" + where
        directory = os.fsencode(directory_in_str)

        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            print ("processing file " + filename)
            filename = "old_thumbnails/" + where + "/" + filename
            image_paste_over(filename, "new_layer/contest_2021.png", where)

def update_thumbnail(youtube, where):
    print ("processing " + where)
    directory_in_str = "new_thumbnails/old_thumbnails/" + where
    directory = os.fsencode(directory_in_str)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        print ("processing file " + filename)
        video_id = filename.split(".")[0]
        filename = "new_thumbnails/old_thumbnails/" + where + "/" + filename
        request = youtube.thumbnails().set(
        videoId=video_id,
        
        # TODO: For this request to work, you must replace "YOUR_FILE"
        #       with a pointer to the actual file you are uploading.
        media_body=MediaFileUpload(filename)
        )
        response = request.execute()

def update_description(youtube, where):
    print ("processing " + where)
    directory_in_str = "new_thumbnails/old_thumbnails/" + where
    directory = os.fsencode(directory_in_str)
    prefix = "Join the India's Largest Tech Cult!\n\n🏆 Enter 2021 contest here - https://gleam.io/aEOQ8/giveaway-free-amazon-alexa-tshirts-and-laptop-sticker-swags-chennai-tech-radar-bribe-by-bytes\n\nWinners will get:\n\n🧫 Alexa Echo Dot 4th Generation\n\n👕 Cool T-Shirts \n\n💻 Laptop Stickers\n\n"

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        print ("processing file " + filename)
        video_id = filename.split(".")[0]
        filename = "new_thumbnails/old_thumbnails/" + where + "/" + filename
        try: 
            request = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            response = request.execute()
            
            for video in response['items']:
                curr_title = video['snippet']['title']
                curr_desc = video['snippet']['description']
                new_desc = prefix + curr_desc

                request = youtube.videos().update(
                    part="snippet,status,localizations",
                    body={
                    "id": video_id,
                    "snippet": {
                        "categoryId": 27,
                        "description": new_desc,
                        "title": curr_title
                    }
                    }
                )
                response = request.execute()
        except:
            print("Unexpected error:", sys.exc_info()[0])

def main():
    youtube = inityt()
    myyoutube = initmyyt()
    #  extractthumbnails(youtube)
    # patch_contest("top_left")
    # patch_contest("top_right")
    # patch_contest("bottom_left")
    # patch_contest("bottom_right")
    #update_thumbnail(initmyyt(),"nowhere")
    #update_description(initmyyt(),"nowhere")
    
    # update_thumbnail(myyoutube,"top_left")
    # update_thumbnail(myyoutube,"top_right")
    # update_thumbnail(myyoutube,"bottom_left")
    # update_thumbnail(myyoutube,"bottom_right")
    
    update_description(myyoutube,"top_left")
    update_description(myyoutube,"top_right")
    update_description(myyoutube,"bottom_left")
    update_description(myyoutube,"bottom_right")





if __name__ == "__main__":
    main()