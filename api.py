
# -*- coding: utf-8 -*-

import os
import json

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "oauthkey.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    data = ""
    first = True
    counter = 0
    while True:
        if first:
            request = youtube.videos().list(
                part="id, snippet",
                myRating="like",
                maxResults = 50
            )
            first = False
        else:
            request = youtube.videos().list(
                part="id, snippet",
                myRating="like",
                maxResults = 50,
                pageToken = nextPage
            )

        data = request.execute()
        #data = json.dumps(request.execute(), indent = 2)
        
        for video in data["items"]:
            video_json = json.dumps(video, indent = 2)
            #print(video_json)
            counter += 1
            
            if video["snippet"]["categoryId"] == "22":
                print("https://youtu.be/" + video["id"], "-", video["snippet"]["title"])
        try:
            nextPage = data["nextPageToken"]
        except Exception as e:
            #print(json.dumps(data, indent = 2))
            print(e, "wahrscheinlich keine nächste Seite. Exit.")
            print("Es gab insgesamt", counter, "Videos in der Playlist.")
            break
if __name__ == "__main__":
    main()