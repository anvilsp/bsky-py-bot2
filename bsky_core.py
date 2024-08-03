# This script includes the components that interface with the Bluesky API, including the client connection and functions to read notifications and create posts.
# Program by Ava Vazquez

import os
from atproto import Client
from dotenv import load_dotenv 

# Initialize .env file
load_dotenv()

# initialize bluesky client connection - app login details must be set in '.env' file
client = Client(base_url='https://bsky.social')
client.login(os.environ.get("BSKY_IDENTIFIER"), os.environ.get("BSKY_APP_PASSWORD"))

def create_image_post(image, alt_text = None): # create an image post with no text
    post = client.send_image(image=image, image_alt=alt_text, text="")
    return post

def create_image_reply(image, uri, cid, root_uri = None, root_cid = None, text = None, alt_text = None):
    # set uri and cid if they aren't set
    if root_uri == None:
        root_uri = uri
    if root_cid == None:
        root_cid = cid

    # create the post with the given parameters
    post = client.send_image(
        text = text,
        image = image,
        image_alt = alt_text,
        reply_to = {
            "root": {
                "uri": root_uri,
                "cid": root_cid
            },
            "parent": {
                "uri": uri,
                "cid": cid
            }
        }
    )
    return post

def mark_as_read():
    # mark notification as read
    client.app.bsky.notification.update_seen(data = {
        "seenAt": client.get_current_time_iso()
    })

def get_notifications(mark_read = False):
    # get the 10 most recent notifications
    notifications = client.app.bsky.notification.list_notifications()['notifications'][:10]

    # lists for replies and mentions
    replies, mentions = [], []

    for notif in notifications:
        # sort unread notifications into two categories: replies and mentions
        if not notif.is_read:
            if notif.reason == "reply":
                replies.append(notif)
            elif notif.reason == "mention":
                mentions.append(notif)
        
    # mark as read if the parameter is set
    if mark_read:
        mark_as_read()
    return replies, mentions