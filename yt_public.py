# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import googleapiclient.discovery

from utils.comments import process_comments,make_csv

def main(Ytlink):
    comments_list=[]

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "#####"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)


    Ytlink=Ytlink[32:43]

    request = youtube.commentThreads().list(
        part="id,snippet",
        videoId=Ytlink
    )
    response = request.execute()

    #print(response)
    comments_list.extend(process_comments(response['items']))
    #print(len(response['items']))
    #print(comments_list)

#Next Page Token
    while response.get('nextPageToken',None):
        request = youtube.commentThreads().list(
            part = "id,snippet",
            videoId = Ytlink,
            pageToken = response['nextPageToken']
        )
        response = request.execute()
        comments_list.extend(process_comments(response['items']))

    print(f'Finished fetching comments,{len(comments_list)} comments Found')

#make list into csv
    if True:
        make_csv(comments_list)

if __name__ == "__main__":
    main('https://www.youtube.com/watch?v=C2Ua3b32UOw')
